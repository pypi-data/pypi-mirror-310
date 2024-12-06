"""Copyright 2020 Sarus SAS.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Sarus library to leverage sensitive data without revealing them

This lib contains classes and method to browse,
learn from & explore sensitive datasets.
It connects to a Sarus server, which acts as a gateway, to ensure no
results/analysis coming out of this lib are sensitive.
"""

from __future__ import annotations  # noqa: F407

import base64
import datetime
import decimal
import getpass
import hashlib
import io
import json
import logging
import os
import pprint
import re
import sys
import tarfile
import tempfile
import textwrap
import time
import typing as t
import warnings
import webbrowser
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Dict, List, Optional

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import sarus_data_spec
from requests import Session
from sarus_data_spec.attribute import attach_properties

import sarus
import sarus.typing as srt
from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.manager.dataspec_api import (
    get_dataspec,
    pull_dataspec_graph,
    push_dataspec_graph,
    raise_response,
)
from sarus.manager.typing import SDKManager
from sarus.pandas.dataframe import DataFrame

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import sarus_data_spec.protobuf as sp
    import sarus_data_spec.typing as st
    from sarus_data_spec.constants import BIG_DATA_TASK, SCHEMA_TASK
    from sarus_data_spec.context import push_global_context
    from sarus_data_spec.dataspec_validator.privacy_limit import (
        DeltaEpsilonLimit,
    )
    from sarus_data_spec.protobuf.utilities import dict_deserialize
    from sarus_data_spec.status import DataSpecErrorStatus
    from sarus_data_spec.transform import select_sql, transform_to_small_data
    from sarus_data_spec.variant_constraint import pup_constraint

    from sarus.context.local_sdk import LocalSDKContext

    try:
        import tensorflow as tf

        import sarus.legacy.tensorflow as sltf
    except ModuleNotFoundError:
        pass  # error message in sarus_data_spec.typing

logger = logging.getLogger(__name__)


def sdk_excepthook(
    exc_cls: t.Type[BaseException],
    exc: BaseException,
    tb: Optional[TracebackType],
) -> Any:
    if isinstance(exc, DataSpecErrorStatus):
        last_exc_msg = exc.extract_last_exc()

        if last_exc_msg:
            sys.stderr.write("Remote dataspec error: ")
            sys.stderr.write(last_exc_msg)
            sys.stderr.write("\n")

            return

    sys.__excepthook__(exc_cls, exc, tb)


sys.excepthook = sdk_excepthook


class MessageToUserException(Exception):
    """An exception meant to print a message to the user when printed by the REPL after being raised."""

    args: t.Tuple[str]

    def __str__(self) -> str:
        indented_msg = "\n"
        indented_msg += textwrap.indent(self.args[0], "  ")

        return indented_msg


@dataclass
class Synthetic:
    """Simple class to represent synthetic data."""

    data: Optional[pa.Table] = None
    rows: Optional[int] = None


class DatasetList(list):
    """Custom class to lazily fetch a Dataset when indexing."""

    def __init__(
        self, iterable: t.Iterable[ShallowDataset], client: Client
    ) -> None:
        super().__init__(iterable)
        self.client = client

    def __getitem__(self, i: int) -> Dataset:
        shallow_dataset = super().__getitem__(i)
        slugname = shallow_dataset.name
        return self.client.dataset(slugname=slugname)

    def __setitem__(self, i: int, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def append(self, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def insert(self, i: int, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def extend(self, other: DatasetList) -> None:
        raise NotImplementedError("A DatasetList is immutable.")


class ShallowDataset:
    """Shallow dataset that is merely used as a placeholder for slugname."""

    def __init__(self, id: int, slugname: str):
        self.id = id
        self.name = slugname

    def __repr__(self) -> str:
        return f"<Sarus Dataset slugname={self.name} id={self.id}>"

    @classmethod
    def _from_dict(cls, data: dict) -> ShallowDataset:
        # `data` is the JSON returned by calling GET /datasets/
        return cls(data.get("id"), data.get("name"))


class DataConnectionList(list):
    """Custom class to lazily fetch a Dataset when indexing."""

    def __init__(self, iterable: t.Iterable[ShallowDataConnection]) -> None:
        super().__init__(iterable)

    def __setitem__(self, i: int, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def append(self, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def insert(self, i: int, value: t.Any) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    def extend(self, other: DatasetList) -> None:
        raise NotImplementedError("A DatasetList is immutable.")

    @classmethod
    def _from_list(cls, data: list) -> DataConnectionList:
        # `data` is the JSON returned by calling GET /dataconnection/
        return cls(
            [ShallowDataConnection._from_dict(datacon) for datacon in data]
        )


class ShallowDataConnection:
    """Shallow dataset that is merely used as a placeholder for slugname."""

    def __init__(
        self,
        id: int,
        slugname: str,
        connector_type: str,
        table_names: List[str],
    ):
        self.id = id
        self.name = slugname
        self.connector_type = connector_type
        self.destination_table_names = table_names

    def __repr__(self) -> str:
        return f"<Sarus DataConnection name={self.name} id={self.id} connector_type={self.connector_type}, destination_table_names={self.destination_table_names}>>"

    @classmethod
    def _from_dict(cls, data: dict) -> ShallowDataset:
        # `data` is the JSON returned by calling GET /dataconnection/
        return cls(
            data.get("id"),
            data.get("name"),
            data.get("connector_type"),
            data.get("whitelisted_table_names"),
        )


class Dataset(DataSpecWrapper[t.Iterator[pa.RecordBatch]]):
    """A class representing a Sarus Dataset.

    This class is the interface to the protected data. It enables to inspect the
    Sarus dataset metadata, manipulate synthetic data locally, prepare
    processing steps and identify the dataset for executing remote private
    queries.

    Args:
        id: The dataset id.
        client: The Sarus client where the dataset is defined.
        type_metadata: A serialized json holding the dataset metadata.
        marginals: A serialized json holding the dataset marginals.
        human_description: A short human readable description.
        policy:
    """

    def __init__(
        self,
        id: int,
        client: "Client",
        dataspec: st.DataSpec,
        is_bigdata: Optional[bool] = None,
        type_metadata: Optional[str] = None,
        human_description: Optional[str] = None,
        marginals: Optional[str] = None,
        policy: Optional[dict] = None,
        synthetic: Dict[str, Synthetic] = None,
    ):
        self.client: "Client" = client
        self._set_dataspec(dataspec)
        name = dataspec.properties().get("slugname")
        attach_properties(
            dataspec,
            name=srt.ATTRIBUTES_DS,
            properties={
                "id": str(id),
                "name": name,
                "desc": f"<Sarus Dataset slugname={name} id={str(id)}>",
            },
        )
        self.type_metadata: Optional[Dict[str, Any]] = None
        if type_metadata is not None:
            self.type_metadata = json.loads(type_metadata)
        self.human_description: Optional[str] = human_description
        if synthetic is None:
            self._synthetic = dict(original=Synthetic(), encoded=Synthetic())
        else:
            self._synthetic = synthetic
        self.marginals: Optional[Dict[str, Any]] = None
        if marginals is not None:
            self.marginals = json.loads(marginals)

        self.policy: Optional[dict] = policy

    @classmethod
    def _from_dict(cls, admin_ds: dict, client: Client) -> Dataset:
        """Get a dataset from the json data sent by the server.

        Deserializes the protobufs contained in the response and registers them
        in the storage.

        Args:
            admin_ds (dict): JSON data returned by calling GET /datasets/<id>
            client (Client): client used to get information from the server

        Returns:
            Dataset
        """
        dataspec_id = admin_ds.get("id")
        serialized_dataspec = admin_ds.get("dataspec")
        slugname = admin_ds.get("name")
        manager: SDKManager = client.context().manager()

        if serialized_dataspec is None:
            # TODO /datasets doesn't return the DataSpec def
            raise ValueError(f"{slugname} not returned by the server.")

        # Deserialize objects from the JSON response
        dataspec: st.Dataset = (
            client.context()
            .factory()
            .create(
                dict_deserialize(serialized_dataspec["dataset"]), store=False
            )
        )
        pull_dataspec_graph(client=client, uuid=dataspec.uuid())

        syn_dataset: st.Dataset = dataspec.variant(st.ConstraintKind.SYNTHETIC)

        # Update statuses
        dataspec.manager().copy_status_from_server(
            dataspec, task_names=[SCHEMA_TASK]
        )
        dataspec.manager().copy_status_from_server(
            syn_dataset, task_names=[SCHEMA_TASK]
        )
        dataspec.manager().copy_status_from_server(
            dataspec, task_names=[BIG_DATA_TASK]
        )
        dataspec.manager().copy_status_from_server(
            syn_dataset, task_names=[BIG_DATA_TASK]
        )

        # TODO fetch the PUP token from the API
        # (it is lazily computed on the server)
        h = hashlib.md5(usedforsecurity=False)
        h.update(dataspec.protobuf().SerializeToString())
        pup_token = h.hexdigest()
        pup_constraint(
            dataspec=dataspec,
            token=pup_token,
            required_context=[],
            privacy_limit=DeltaEpsilonLimit({0.0: 0.0}),
        )

        # Attach default delta to the source
        sources_ds = dataspec.sources(sp.type_name(sp.Dataset))
        source = sources_ds.pop()
        manager.set_admin_ds(source, admin_ds)

        return cls(
            id=dataspec_id,
            dataspec=dataspec,
            client=client,
            type_metadata=admin_ds.get("type_metadata"),
            marginals=admin_ds.get("marginals"),
            human_description=admin_ds.get("human_description"),
        )

    @property
    def features(self) -> Optional[Dict[str, Dict]]:
        """Features of the Sarus dataset and associated metadata.

        Returns:
            Dict[str, Dict]: A dictionary holding metadata where each key
            is a table name and each value is a dict with features.
        """
        if self.type_metadata is None:
            return None
        if len(self.type_metadata) > 1:
            features: Dict[str, Dict] = {
                table["name"]: table["features"]
                for table in self.type_metadata
            }
        else:
            features: Dict[str, Dict] = self.type_metadata[0]["features"]
        return features

    def __repr__(self) -> str:
        attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
        if attributes_ds is not None:
            return attributes_ds["desc"]
        else:
            return "<Sarus Dataset>"

    def _ipython_display_(self) -> None:
        """Custom ipython display."""
        print(repr(self))

    def as_tensorflow(
        self,
        max_download_size: Optional[int] = None,
        original: bool = False,
    ) -> sltf.Dataset:
        """Return the corresponding `sarus.tensorflow.Dataset` object.

        This allows to manipulate the Sarus `Dataset` as a Tensorflow dataset.

        Args:
            max_download_size (int, optional): Max number of synthetic data rows
                to download locally. Indicates the number of synthetic data
                rows to download from the Sarus server. It will not download
                more than the maximum number of available synthetic data. If
                `None`, it will download all the synthetic data. If different
                from `None`, all local computations will be done on the local
                synthetic sample so local results will differ from remote
                results.

            original (bool): Returns categories original values.
                If True will return categories as original values. If False,
                will encode categories as integers.

        Returns:
            A sarus_tensorflow.Dataset.
        """
        logging.warning(
            "'as_tensorflow()' uses the old API, not preprocessing."
        )
        if self._dataspec.manager().is_big_data(self._dataspec):
            raise Exception(
                "`as_tensorflow()` is not supported for this dataset"
            )
        return sltf.Dataset(
            self,
            max_download_size=max_download_size,
            original=original,
        )

    def as_pandas(self, randomize_bigdata_sampling=True) -> DataFrame:
        """Create a DataFrame wrapper ready to be used for pandas operations.

        If the source dataset is big data, we select, if needed, a limited number of
        rows to enable external transformations (pandas, sklearn, etc.).

        Args:
            randomize_bigdata_sampling (bool, optional): Determines whether the limited rows should be selected
            randomly or if only the first rows should be used. This is only applicable if sampling is performed.
            Defaults to True.

        Returns:
            DataFrame: The Sarus DataFrame wrapper.
        """
        # attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)   # noqa: E800
        dataspec_small_data = transform_to_small_data(
            self._dataspec, None, random_sampling=randomize_bigdata_sampling
        )
        # assert attributes_ds is not None
        return DataFrame.from_dataspec(dataspec_small_data)

    def __getitem__(self, item: t.List[str]) -> Dataset:
        return self.table(item)

    def table(self, table_name: t.List[str]) -> Dataset:
        """Get a table from the dataset.

        Args:
            table_name (List[str]): Name of a form ['namespace_1','namespace_2'...,'table_name'].
                One can omit namespaces if table names are not ambiguous.

        Returns:
            Table: Table fitting the given name.
        """
        dataspec_tables = [
            el.to_strings_list()[0] for el in self._dataspec.schema().tables()
        ]
        # remove protection name and add schema_name
        dataspec_tables = [
            [self._dataspec.schema().name(), *(val for val in el[1:])]
            for el in dataspec_tables
        ]

        possible_tables_indices = []
        # iterate over tables and select_ones that have same path
        n_elements = len(table_name)
        for i, table_path in enumerate(dataspec_tables):
            if table_path[-n_elements:] == table_name:
                possible_tables_indices.append(i)

        try:
            assert len(possible_tables_indices) == 1
        except AssertionError:
            if len(possible_tables_indices) == 0:
                raise ValueError(f"Table {table_name} not found")
            else:
                raise ValueError(f"Ambiguous table name {table_name}")

        else:
            table_path = self._dataspec.schema().tables()[
                possible_tables_indices[0]
            ]

        ds_filter = self._dataspec.schema().data_type().get(table_path)
        filtered_ds = sarus_data_spec.transform.filter(filter=ds_filter)(
            self._dataspec
        )
        selected_ds = sarus_data_spec.transform.get_item(path=table_path)(
            filtered_ds
        )

        # create dataset
        table_ds = Dataset.from_dataspec(selected_ds)

        attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
        assert attributes_ds is not None
        name = f"<Sarus Table name={table_name}>"
        attach_properties(
            selected_ds,
            name=srt.ATTRIBUTES_DS,
            properties={
                "id": attributes_ds["id"],
                "name": name,
                "desc": f"<Sarus Table name={table_name}>",
            },
        )

        return table_ds

    def tables(self) -> t.List[t.List[str]]:
        """For given parameters of a Sarus Dataset return a list of Sarus Tables."""
        dataspec_tables = [
            el.to_strings_list()[0] for el in self._dataspec.schema().tables()
        ]

        # remove protection name and add schema_name
        dataspec_tables = [
            [self._dataspec.schema().name(), *(val for val in el[1:])]
            for el in dataspec_tables
        ]
        return dataspec_tables

    def sql(self, query: str, sarus_default_output=None) -> Dataset:
        """Apply an SQL query to the dataset.

        Args:
            query (str): SQL query

        Returns:
            an instance of Sarus Dataset.
        """
        select_ds = select_sql(
            query, sarus_default_output=sarus_default_output
        )(self._dataspec)
        attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
        assert attributes_ds is not None
        attach_properties(
            select_ds,
            name=srt.ATTRIBUTES_DS,
            properties={
                "id": attributes_ds["id"],
                "name": attributes_ds["name"],
                "desc": f"<Sarus Dataset query='{query}'>",
            },
        )
        computation_graph = select_ds.manager().computation_graph(select_ds)
        referrables = (
            list(computation_graph["dataspecs"])
            + list(computation_graph["transforms"])
            + list(computation_graph["attributes"])
        )
        push_dataspec_graph(self.manager().client(), referrables)
        # TODO: remove when we can compute the pup token of select SQL in SDK
        pull_dataspec_graph(self.manager().client(), select_ds.uuid())
        ds_wrapper = self.from_dataspec(select_ds)
        return ds_wrapper

    @property
    def epsilon(self) -> float:
        """Retrieve the remaining global privacy budget (epsilon) of the current access rule.

        Returns:
            float: The remaining privacy budget (global epsilon) of the access
            rule.
        """
        attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
        assert attributes_ds is not None
        resp = self.client.session().get(
            f"{self.client.base_url}/datasets/{attributes_ds['id']}",
        )
        if resp.status_code > 200:
            raise Exception(
                f"Error while retrieving the current value of epsilon. "
                f"Gateway answer was: \n{resp}"
            )
        return float(resp.json()["accesses"][0]["current_epsilon"])

    @property
    def max_epsilon(self) -> float:
        """Retrieve the maximum global privacy budget (epsilon) granted by the Data preparator, for the current access rule.

        Returns:
            float: The maximum privacy budget (global epsilon) of the access
            rule.
        """
        attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
        assert attributes_ds is not None
        resp = self.client.session().get(
            f"{self.client.base_url}/datasets/{attributes_ds['id']}",
        )
        if resp.status_code > 200:
            raise Exception(
                f"Error while retrieving the current value of epsilon. "
                f"Gateway answer was: \n{resp}"
            )
        return float(resp.json()["accesses"][0]["max_epsilon"])

    def _fetch_synthetic(
        self,
        rows_number: Optional[int] = None,
        force_refresh: bool = False,
        original: bool = True,
        table_name: Optional[str] = None,
    ) -> pa.Table:
        """Fetch synthetic data as a pyarrow.Table.

        Downloads them if they are not in memory yet or if more rows are
        required. Do nothing if enough data have already been downloaded.

        Args:
            rows_number (int, optional): number of rows to return
            force_refresh (bool): if True, always fetch from server
            original (bool): if False, get categorical values as integers
            table_name (str, optional): The name of the table to fetch from.
        """
        if table_name is None and len(self.type_metadata) > 1:
            raise ValueError("Table name needs to be specified in this case.")

        dataset_size = int(self.marginals["rows"])
        if rows_number is None:
            rows_number = dataset_size

        if rows_number < dataset_size:
            logging.warning(
                "Requested `max_download_size` is lower than "
                "total number of remote synth data, so"
                "local operations' results will differ from remote results. \n"
                "Use `max_download_size`=None to locally download all "
                "available synth data"
            )

        if rows_number > dataset_size:
            logging.warning(
                "Cannot satisfy `max_download_size` as there is not enough "
                "remote synth data. \nDownloading max available synth data..."
            )

        rows_number = min(dataset_size, rows_number)

        synthetic_type = "original" if original else "encoded"
        has_enough_synthetic = (
            self._synthetic[synthetic_type].rows is not None
            and rows_number <= self._synthetic[synthetic_type].rows
        )

        if not has_enough_synthetic or force_refresh:
            # Fetch synthetic data
            attributes_ds = self._dataspec.attribute(name=srt.ATTRIBUTES_DS)
            uri = (
                f"{self.client.base_url}/synthetic_data/{attributes_ds['id']}"
            )
            if table_name is not None:
                uri = f"{uri}/{table_name}"

            resp = self.client.session().get(
                uri,
                stream=True,
                params={
                    "textual_categories": original,
                    "rows_number": rows_number,
                },
            )
            if resp.status_code > 200:
                raise Exception(
                    f"Error while retrieving synthetic data. "
                    f"Gateway answer was: \n{resp}"
                )

            synthetic_table = pq.ParquetFile(io.BytesIO(resp.content)).read()
            self._synthetic[synthetic_type].data = synthetic_table
            self._synthetic[synthetic_type].rows = rows_number

        return self._synthetic[synthetic_type].data.slice(length=rows_number)

    @staticmethod
    def _sarus_features_to_tf_spec(
        features: Dict[str, Any],
        original: bool,
    ) -> Dict[str, tf.TensorSpec]:
        """Convert Sarus features to Tensorflow spec."""
        mapping = {
            "categorical": tf.string if original else tf.int16,
            "boolean": tf.bool,
            "integer": tf.int64,
            "real": tf.float32,
            "text": tf.string,
            "datetime": tf.int64,
            "image": tf.uint8,
        }

        def get_tensorspec(feature) -> tf.TensorSpec:
            """Return the tensorflow spec of a Sarus feature."""
            feature_type = list(feature["type"].keys())[0]
            dtype = mapping[feature_type]
            if feature_type == "image":
                width = feature["type"]["image"]["shape"]["width"]
                height = feature["type"]["image"]["shape"]["height"]
                channels = feature["type"]["image"]["shape"]["channel"]
                shape = (None, width, height, channels)
            else:
                shape = (None,)
            return tf.TensorSpec(dtype=dtype, shape=shape)

        return {
            feature["name"]: get_tensorspec(feature) for feature in features
        }

    @staticmethod
    def _adapt_for_tf(
        batch: Dict[str, Any],
        features: Dict[str, Any],
        original: bool,
    ) -> Dict[str, Any]:
        """Convert python data to tensorflow compatible data.

        Convert datetime.datetime to nanoseconds.
        Convert images serialized as bytes by petastorm to 3d arrays.
        """
        adapted_batch = dict()
        for feature in features:
            dtype = list(feature["type"].keys())[0]
            if dtype == "datetime":

                def decode_datetime(datetime_value: datetime.datetime) -> int:
                    if datetime_value is None:
                        return np.iinfo(np.int64).min
                    return int(datetime_value.timestamp()) * int(1e9)

                adapted_batch[feature["name"]] = tf.constant(
                    list(map(decode_datetime, batch[feature["name"]])),
                    dtype=tf.int64,
                )
            elif dtype == "image":
                adapted_batch[feature["name"]] = tf.stack(
                    list(map(Dataset.decode_image, batch[feature["name"]])),
                    axis=0,
                )

            elif dtype == "text":
                adapted_batch[feature["name"]] = tf.constant(
                    list(map(str, batch[feature["name"]])), dtype=tf.string
                )

            elif dtype == "categorical":
                dtype = tf.string if original else tf.int16
                adapted_batch[feature["name"]] = tf.constant(
                    batch[feature["name"]], dtype=dtype
                )

            elif dtype == "integer":
                # replace None by min_int_32 to avoid crash
                cleaned_batch = [
                    x if x is not None else np.iinfo(np.int64).min
                    for x in batch[feature["name"]]
                ]
                adapted_batch[feature["name"]] = tf.constant(
                    cleaned_batch, dtype=tf.int64
                )

            elif dtype == "real":
                # replace None by NaN to avoid crash
                cleaned_batch = [
                    x if x is not None else float("NaN")
                    for x in batch[feature["name"]]
                ]
                adapted_batch[feature["name"]] = tf.constant(
                    cleaned_batch, dtype=tf.float32
                )

            elif dtype == "boolean":
                adapted_batch[feature["name"]] = tf.constant(
                    batch[feature["name"]], dtype=tf.bool
                )

        return adapted_batch

    def _synthetic_as_tf_dataset(
        self,
        batch_size: int,
        rows_number: Optional[int] = None,
        original: bool = False,
        force_refresh: bool = False,
        table_name: Optional[str] = None,
    ) -> tf.data.Dataset:
        """Return synthetic data as a tensorflow.data.Dataset.

        Args:
            batch_size (int): size of the batches in the dataset
            rows_number (int, optional): number of rows in the dataset
            original (bool): if False, return categories as integers
            force_refresh (bool): if True, always fetch from server

        Returns:
            tensorflow.data.Dataset: synthetic data
        """
        if table_name is None and len(self.type_metadata) > 1:
            raise ValueError("Table name needs to be specified in this case.")

        if force_refresh:
            self._fetch_synthetic(
                force_refresh=force_refresh,
                original=original,
                rows_number=rows_number,
            )

        if table_name is None:
            features = self.features
        else:
            features = self.features[table_name]

        # Generator function iterating pyarrow RecordBatches
        def generator() -> Dict[str, List[Any]]:
            synthetic_table = self._fetch_synthetic(
                original=original, rows_number=rows_number
            )
            for batch in synthetic_table.to_batches(max_chunksize=batch_size):
                yield Dataset._adapt_for_tf(
                    batch=batch.to_pydict(),
                    features=features,
                    original=original,
                )

        tf_signature = Dataset._sarus_features_to_tf_spec(features, original)

        return tf.data.Dataset.from_generator(
            generator, output_signature=tf_signature
        )


class Client:
    """Entry point for the Sarus API client."""

    _URL_SUFFIX = "/gateway"
    _HEADER_NAME_CLIENT_SDK_VERSION = "SARUS-Client-SDK-Version"

    def _url_validator(self, url):
        """URL validator.

        From https://stackoverflow.com/questions/7160737/
        python-how-to-validate-a-url-in-python-malformed-or-not
        """
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|"
            r"[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

    def __init__(
        self,
        url: str = f"http://0.0.0.0{_URL_SUFFIX}",
        google_login: bool = False,
        email: Optional[str] = None,
        password: Optional[str] = None,
        verbose: int = 1,
    ):
        # TODO : progress bar self.progress_bar = Progbar(100,
        # stateful_metrics=None)
        if not self._url_validator(url):
            raise ValueError("Bad url")
        if not url.endswith(self._URL_SUFFIX):
            raise ValueError(
                "Error: Invalid URL. "
                f'Please ensure you are using the correct URL endpoint ("{self._URL_SUFFIX}"). '
                "If you continue to experience issues, contact your Sarus account manager."
            )
        self.base_url = url

        self._session = session = Session()
        session.headers[self._HEADER_NAME_CLIENT_SDK_VERSION] = sarus.VERSION

        if google_login:
            self._oidc_login()
        else:
            self._credentials_login(email, password)

        self._context = LocalSDKContext(self, verbose=verbose)
        self._context.set_sync_policy(srt.SyncPolicy.SEND_ON_VALUE)
        push_global_context(self._context)

        self.force_runtime_check = False

    def set_verbose(self, verbose: int) -> None:
        self._context._verbose = verbose

    def context(self) -> LocalSDKContext:
        return self._context

    def url(self):
        return self.base_url

    def session(self):
        return self._session

    def save(self, wrapper: srt.DataSpecWrapper, path: str) -> None:
        """Save the representation of a sarus object to a file.

        Args:
            wrapper (DataSpecWrapper): The sarus object to save.
            path (str): The path to save the object to.

        Returns:
            None
        """
        manager: SDKManager = self.context().manager()

        user_ds = wrapper.dataspec(srt.DataSpecVariant.USER_DEFINED)
        manager.push(user_ds)

        saved_data = {
            "user_ds_uuid": user_ds.uuid(),
            "wrapper_type": type(wrapper).__name__,
        }

        with open(path, "w") as save_file:
            json.dump(saved_data, save_file)

    def load(
        self,
        path=None,
        uuid=None,
        to_dataset: bool = False,
    ) -> srt.DataSpecWrapper:
        """Load a sarus object from a path.

        Args:
            path (str): The file path to load the sarus object from.

        Returns:
            DataSpecWrapper: The sarus object (eg: DataFrame,model..).
        """
        if path is None and uuid is None:
            raise ValueError(
                "You must provide either argument 'path' or 'uuid'."
            )

        if uuid is not None:
            user_ds_uuid = uuid
            wrapper_type = None
        elif path is not None:
            with open(path, "r") as load_file:
                saved_data = json.load(load_file)

            user_ds_uuid = saved_data["user_ds_uuid"]
            wrapper_type = saved_data["wrapper_type"]

        pull_dataspec_graph(client=self, uuid=user_ds_uuid)
        ds = get_dataspec(client=self, uuid=user_ds_uuid)

        sources_ds = ds.sources(sp.type_name(sp.Dataset))
        for source in sources_ds:
            if not source.is_public():
                self.dataset(source["slugname"])

        if to_dataset and ds.prototype() == sp.Dataset:
            loaded_wrapper = Dataset.from_dataspec(ds)
        elif wrapper_type is not None and ds.prototype() == sp.Dataset:
            if wrapper_type == "Dataset":
                loaded_wrapper = Dataset.from_dataspec(ds)
            else:
                loaded_wrapper = DataFrame.from_dataspec(ds)
        else:
            # scalar must be created using the python type
            # transformed dataset also for now
            loaded_wrapper = self.context().wrapper_factory().create(ds)

        return loaded_wrapper

    def _oidc_login(self):
        oidc_login_url = f"{self.base_url}/oidc_login?headless=true"
        try:
            from IPython.display import Javascript, clear_output

            display(  # noqa: F821
                Javascript(f'window.open("{oidc_login_url}");')
            )
            display(clear_output())  # noqa: F821
        except Exception:
            webbrowser.open(oidc_login_url)
        token = getpass.getpass(
            "Logging in via google.\nYou will be redirected to a login page "
            "where you will obtain a token to paste below.\nIf you are not "
            f"redirected automatically, you can visit {oidc_login_url}\n"
        )
        self.session().cookies.set(
            "session", base64.b64decode(token).decode("ascii")
        )
        # just to check that the login is successful
        try:
            self.list_datasets()
        except Exception:
            raise Exception("Error during login: incorrect token")

    def _credentials_login(self, email=None, password=None):
        if email is None:
            raise ValueError("Please enter your email")

        credentials = {}
        credentials["email"] = email

        if password is not None:
            credentials["password"] = password
        else:
            credentials["password"] = getpass.getpass(
                prompt="Password: ", stream=None
            )

        response = self.session().post(
            f"{self.base_url}/login",
            json=credentials,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 401:
            raise ValueError("Error during login: incorrect credentials")

        # Let `requests` handle unexpected HTTP status codes.
        response.raise_for_status()

        resp_json = response.json()
        warning_message = resp_json.get("warning_message")
        if warning_message:
            logging.warning(warning_message)

    def list_datasets(self) -> DatasetList:
        """List available Sarus datasets.

        Returns:
            DatasetList: List of available Sarus datasets.
        """
        request = self.session().get(f"{self.base_url}/datasets")
        raise_response(request)
        unsorted_datasets = [
            ShallowDataset._from_dict(ds_json)
            for ds_json in request.json()
            if ds_json["status"] == "ready"
        ]
        sorted_datasets = sorted(
            unsorted_datasets,
            key=lambda x: x.name,
        )
        return DatasetList(sorted_datasets, self)

    def _dataconnections(self, slugname=None):
        payload = {"slugname": slugname} if slugname is not None else {}
        request = self.session().get(
            f"{self.base_url}/dataconnections",
            json=payload,
        )
        raise_response(request)
        dataconnections = request.json()
        return dataconnections

    def list_writable_dataconnections(self, slugname=None):
        dataconnections = self._dataconnections(slugname)
        return DataConnectionList._from_list(dataconnections)

    def describe_destination_table(
        self, data_connection_name: str, table: str
    ):
        type_table = self._get_type_destination_table(
            data_connection_name, table
        )
        for column_name in type_table.children().keys():
            print(
                f"Column name: {column_name}, Type: {type_table.children()[column_name].name()}"
            )

    def _get_type_destination_table(
        self, data_connection_name: str, table: str
    ):
        parts = table.split(".")
        if len(parts) == 2 and all(parts):
            schema_name = parts[0]
            table_name = parts[1]
        else:
            raise ValueError(
                "Error: Input must be in the format 'dataconnection_name.table_name' with non-empty Schema and table_name."
            )
        start = time.perf_counter()
        resp = self.session().get(
            f"{self.url()}/table/{data_connection_name}/{schema_name}/{table_name}/describe",
        )
        end = time.perf_counter()
        logger.debug(
            f"GET /table/{data_connection_name}/{schema_name}/{table_name}/describe {resp.status_code} {resp.headers.get('Content-Type')} ({end-start:.2f}s)"
        )
        raise_response(resp)

        proto = dict_deserialize(resp.json()["table_type"])
        type_table = self.context().factory().create(proto)
        return type_table

    def dataset(self, slugname: str = None, id: int = None) -> Dataset:
        """Select a dataset from the Sarus Gateway.

        Either `slugname` or `id` should be provided. If both are provided, then
        only the `slugname` is considered.

        Args:
            slugname (str): the slugname of the Dataset to select.
            id (int): the id of the Dataset to select.

        Returns:
            Dataset: The selected Sarus dataset.

        """
        if slugname:
            return self._fetch_dataset_by_name(slugname)
        else:
            return self._fetch_dataset_by_id(id)

    def _fetch_dataset_by_id(self, id: int) -> Dataset:
        """Fetch a dataset from the Sarus Gateway.

        Args:
            id (int): id of the dataset to be fetched

        Returns:
            an instance of Dataset
        """
        request = self.session().get(f"{self.base_url}/datasets/{id}")
        raise_response(request)
        return Dataset._from_dict(request.json(), self)

    def _fetch_dataset_by_name(self, name: str) -> Dataset:
        """Fetch a dataset from the Sarus Gateway.

        Args:
            name (string): name of the dataset to be fetched

        Returns:
            Dataset: an instance of Dataset
        """
        request = self.session().get(
            f"{self.base_url}/datasets/name/{name}",
        )
        raise_response(request)
        dataset = Dataset._from_dict(request.json(), self)
        return dataset

    def query(
        self,
        query: str,
        target_epsilon: Optional[float] = None,
        verbose: bool = True,
        use_old_query=False,
        debug=False,
    ) -> int:
        """Execute a SQL query.

        Args:
            query (String): SQL query

            target_epsilon (Optional[float]): Maximum privacy budget (epsilon) to assign to the query.
                If 0, runs on the synthetic data.
                If >0, result is a combination of a query on the synthetic data and a
                Differentially-Private query on the real data.
                If None, a default target epsilon specific to the current user and access rule is used.
                Default target epsilon is 0 if the access is a Differentially-Private access with
                per-user or per-group limit; default value equals to per-query limit if the access is
                a Differentially-Private access with a per-query limit only. Meaning Sarus maximizes result
                accuracy in the given privacy constraints. See user documentation to know more.

            use_old_query (bool): Whether to use the v1 version of the query task.

            debug (bool): Print the remote traceback if available

        Returns:
            int: Id of the task.
        """
        endpoint = "query"
        if use_old_query:
            endpoint = "query_v1"

        payload = {
            "query": query,
        }
        if target_epsilon is not None:
            payload["target_epsilon"] = target_epsilon

        request = self.session().post(
            f"{self.base_url}/{endpoint}",
            json=payload,
        )
        if request.status_code > 200:
            if request.status_code == 403:
                raise ValueError(
                    "Query failed with the following error: Privacy budget "
                    "limit exceeded"
                )
            else:
                try:
                    error_message = request.json()["error_message"]
                    message_to_user = error_message

                    error_chain = request.json().get("error_chain", None)
                    if error_chain is not None and debug:
                        message_to_user += "\n\nRemote Traceback:\n\n"
                        message_to_user += pprint.pformat(error_chain)
                    raise MessageToUserException(message_to_user)
                except (json.JSONDecodeError, KeyError):
                    raise Exception(
                        f"Error while sending a query.\
                                                             Full Gateway answer was:{request}"
                    )

        task_id = request.json()["task"]
        dataset_id = request.json()["dataset"]["id"]
        start_eps = request.json()["dataset"]["accesses"][0]["current_epsilon"]
        status = self._poll_query_status(task_id)
        error_message = status.get("error_message", None)
        error_chain = status.get("error_chain", None)

        if error_message is not None:
            message_to_user = error_message

            if error_chain is not None and debug:
                message_to_user += "\n\nRemote Traceback:\n\n"
                message_to_user += pprint.pformat(error_chain)
            raise MessageToUserException(message_to_user)
        if verbose:
            ds = self._fetch_dataset_by_id(dataset_id)
            logging.info(
                f"Actual privacy consumption (epsilon): "
                f"{ds.epsilon-start_eps:.03f}"
            )

        if status["status"] == "SUCCESS":
            warning_msg = status["warning_message"]
            if warning_msg is not None:
                logging.warning(warning_msg)

            status_with_pyobjs = self._convert_to_result_with_pyobjs(status)

            return status_with_pyobjs
        else:
            return status

    @staticmethod
    def _convert_to_result_with_pyobjs(
        status: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Convert the query result values to native Python objects using the description field.

        Args:
            status (dict): the status response for a given completed query task returned by the server.

        Returns:
            dict: a new status dict with the initialized Python objects.
        """
        result = []
        for row in status["result"]:
            for idx, col_desc in enumerate(status["description"]):
                _, class_name, _, _, _, _, _ = col_desc
                if class_name == str(decimal.Decimal):
                    row[idx] = decimal.Decimal(row[idx])
            result.append(row)
        return {
            **status,
            "result": result,
        }

    def _abort_training(self, id: int):
        """Abort a training on the Sarus Gateway.

        Args:
            id (int): id of the task to abort (provided by the fit method).
        """
        resp = self.session().delete(
            f"{self.base_url}/training_tasks/{id}/abort",
        )
        if resp.status_code != 204:
            raise Exception(
                f"Error while trying to abort task:\n{resp.content}"
            )

    def _training_status(self, id: int) -> dict:
        """Fetch a dataset from the Sarus Gateway.

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method

        Returns:
            dict: a dict with the status of a training tasks
        """
        request = self.session().get(
            f"{self.base_url}/training_tasks/{id}",
        )
        return request.json()

    def _poll_training_status(self, id: int, timeout: int = 1000) -> dict:
        """Poll & display the status of a training task.

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method

            timeout (int): in seconds

        Returns:
            dict: The training status at the end of the task

        Raises:
            TimeoutError: if timeout is reached before the training finishes
        """
        offset = 0
        elapsed_time = 0.0
        while elapsed_time < timeout:
            elapsed_time += 0.5
            request = self.session().get(
                f"{self.base_url}/training_tasks/{id}",
                params=dict(offset=offset),
            )
            response_dict = request.json()
            offset = response_dict.get("next_offset", 0)
            if "progress" in response_dict:
                progress = base64.b64decode(
                    response_dict["progress"].encode("ascii")
                ).decode("ascii")
                if progress:
                    sys.stdout.write(progress)
            else:
                # this is the end of the training
                sys.stdout.write("\n")
                return response_dict
            sys.stdout.flush()
            time.sleep(0.5)
        raise TimeoutError(
            "Timeout reached while waiting for the model training to finish."
        )

    def _poll_query_status(self, id: int, timeout: int = 1000) -> dict:
        """Poll & display the status of a query task.

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method

            timeout (int): in seconds

        Returns:
            dict: The query status at the end of the task

        Raises:
            TimeoutError: if timeout is reached before the query finishes
        """
        offset = 0
        elapsed_time = 0.0
        while elapsed_time < timeout:
            elapsed_time += 0.5
            request = self.session().get(
                f"{self.base_url}/query_tasks/{id}",
                params=dict(offset=offset),
            )
            response_dict = request.json()
            status = response_dict["status"]
            if status != "PENDING":
                return response_dict
            time.sleep(0.5)
        raise TimeoutError(
            "Timeout reached while waiting for the model training to finish."
        )

    def _fetch_model(self, id: int) -> tf.keras.Model:
        """Fetch a trained model from the Sarus Gateway.

        Args:
            id (int): id of the task to be queried. It was provided by the fit
                method

        Returns:
            tf.keras.Model: a Keras model
        """
        response = self.session().get(
            f"{self.base_url}/models/{id}",
        )
        # apparently we need to save to a temp file
        # https://github.com/keras-team/keras/issues/9343
        with tempfile.TemporaryDirectory() as _dir:
            f = tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
            f.extractall(_dir, members=None)

            return tf.keras.models.load_model(_dir)


def _save_model(model: tf.keras.Model) -> bytes:
    """Convert a keras Model to compressed archive format."""
    with tempfile.TemporaryDirectory() as _dir:
        model.save(_dir)
        with tempfile.TemporaryDirectory() as _second_dir:
            path = os.path.join(_second_dir, "tmpzip")
            with tarfile.open(path, mode="w:gz") as archive:
                archive.add(_dir, recursive=True, arcname="")
            with open(path, "rb") as f:
                ret = f.read()
                return ret
