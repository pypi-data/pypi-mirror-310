from sarus.utils import register_ops

try:
    from sklearn.metrics import *  # noqa: F401, F403
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


register_ops()
