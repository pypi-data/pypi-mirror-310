from sarus.utils import register_ops

try:
    from shap.utils import *  # noqa: F401, F403
except ModuleNotFoundError:
    pass


register_ops()
