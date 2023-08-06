import functools
from typing import Callable, List, Optional

from .session import get_current_session
from .wrapped_function import WrappedFunction

__all__ = ["metadata", "collect"]


def metadata(function):
    """Do something."""
    session = get_current_session()
    if session.metadata is not None:
        raise RuntimeError
    session.metadata = function()
    return function


def collect(
    function: Optional[Callable] = None,
    *,
    labels: Optional[List[str]] = None,
    secrets: Optional[List[str]] = None,
):
    """Do something.

    Arguments:
        labels:
        secrets:

    Examples:
        >>> TK
    """

    def wrap(function):
        session = get_current_session()
        wrapped_function = WrappedFunction(function, labels, secrets)
        session.register(wrapped_function)
        return functools.wraps(function)(wrapped_function)

    # Allows for both `@usage.collect` and `@usage.collect(...)`.
    if function:
        return wrap(function)

    return wrap
