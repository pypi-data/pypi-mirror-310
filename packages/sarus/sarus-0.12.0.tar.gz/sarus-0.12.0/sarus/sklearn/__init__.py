"""Sarus Sklearn package documentation."""
# flake8: noqa

try:
    from sklearn import *

    import sarus.sklearn.cluster as cluster
    import sarus.sklearn.compose as compose
    import sarus.sklearn.decomposition as decomposition
    import sarus.sklearn.ensemble as ensemble
    import sarus.sklearn.impute as impute
    import sarus.sklearn.inspection as inspection
    import sarus.sklearn.linear_model as linear_model
    import sarus.sklearn.metrics as metrics
    import sarus.sklearn.model_selection as model_selection
    import sarus.sklearn.pipeline as pipeline
    import sarus.sklearn.preprocessing as preprocessing
    import sarus.sklearn.svm as svm
except (ModuleNotFoundError, NameError):
    pass
