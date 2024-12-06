import numpy as np

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import sklearn.preprocessing as sk_preprocessing
    from sklearn.preprocessing import *  # noqa: F401, F403
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class OneHotEncoder(DataSpecWrapper[sk_preprocessing.OneHotEncoder]):
    @sarus_init("sklearn.SK_ONEHOT")
    def __init__(
        self,
        *,
        categories="auto",
        drop=None,
        sparse=True,
        dtype=np.float64,
        handle_unknown="error",
        _dataspec=None,
    ): ...

    @sarus_method("sklearn.SK_PIPELINE_FIT", inplace=True)
    def fit(self, X, y=None): ...


class LabelEncoder(DataSpecWrapper[sk_preprocessing.LabelEncoder]):
    @sarus_init("sklearn.SK_LABEL_ENCODER")
    def __init__(
        self,
        *,
        _dataspec=None,
    ): ...

    @sarus_method("sklearn.SK_FIT_Y", inplace=True)
    def fit(self, y): ...


class FunctionTransformer(
    DataSpecWrapper[sk_preprocessing.FunctionTransformer]
):
    @sarus_init("sklearn.SK_FUNCTION_TRANSFORMER")
    def __init__(
        self,
        func=None,
        inverse_func=None,
        *,
        validate=False,
        accept_sparse=False,
        check_inverse=True,
        feature_names_out=None,
        kw_args=None,
        inv_kw_args=None,
    ): ...

    @sarus_method("sklearn.SK_PIPELINE_FIT", inplace=True)
    def fit(self, X, y=None): ...


register_ops()
