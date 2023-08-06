from __future__ import annotations

import atexit
from typing import TYPE_CHECKING, Callable, Dict, Optional, Set

if TYPE_CHECKING:
    from .wrapped_function import WrappedFunction

__all__ = ["init", "shutdown"]

_session = None


def is_initialized() -> bool:
    return _session is not None


def init(session: Optional[Session] = None) -> None:
    """Initialize PyUsage.

    Arguments:
        session: .
    """
    global _session
    if session is None:
        _session = Session()
    else:
        _session = session


def shutdown() -> None:
    global _session
    _session = None


atexit.register(shutdown)


def get_current_session() -> Session:
    if not is_initialized():
        init()

    global _session
    return _session


class Session:
    def __init__(self):
        self._metadata_function = None
        self._metadata = None
        self._functions = set()

    @property
    def metadata(self) -> Optional[Dict[str, str]]:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Dict[str, str]) -> None:
        assert self._metadata is None
        self._metadata = metadata

    @property
    def functions(self) -> Set[WrappedFunction]:
        return self._functions

    def register(self, function: WrappedFunction) -> None:
        self._functions.add(function)
