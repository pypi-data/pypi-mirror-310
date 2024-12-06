"""SDK classes and functions."""

# flake8: noqa
import warnings

VERSION = "0.12.0"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from sarus import (
        imblearn,
        numpy,
        pandas,
        pandas_profiling,
        plotly,
        scipy,
        shap,
        sklearn,
        skopt,
        std,
        xgboost,
        optbinning,
    )

    from .sarus import Client, Dataset
    from .utils import (
        eval,
        eval_perturbation,
        eval_policy,
        floating,
        integer,
        length,
        push_to_table,
        check_push_to_table_status,
    )
    from .dataspec_wrapper import enable_implicit_evaluation


__all__ = [
    "Dataset",
    "Client",
    "length",
    "eval",
    "eval_perturbation",
    "eval_policy",
    "floating",
    "integer",
    "push_to_table",
    "check_push_to_table_status",
    "enable_implicit_evaluation",
]
