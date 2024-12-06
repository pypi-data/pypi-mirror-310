from __future__ import annotations

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import sklearn.decomposition as decomposition  # noqa: F401, F403
    from sklearn.decomposition import *  # noqa: F401, F403
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class PCA(DataSpecWrapper[decomposition.PCA]):
    @sarus_init("sklearn.SK_PCA")
    def __init__(
        self,
        n_components=None,
        *,
        copy=True,
        whiten=False,
        svd_solver="auto",
        tol=0.0,
        iterated_power="auto",
        random_state=None,
        _dataspec=None,
    ): ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y=None): ...


register_ops()
