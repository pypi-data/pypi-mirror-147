from inspect import Parameter, signature
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def get_single_parameter(function: Callable[[T], Any]) -> Parameter:
    """
    Returns metadata about the single parameters of a 1-arg function.

    It can be especially used in meta-programming techniques.
    """
    parameters = list(signature(function).parameters.values())
    if len(parameters) != 1:
        raise ValueError(len(parameters))

    return parameters[0]
