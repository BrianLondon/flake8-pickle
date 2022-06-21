"""Flake8 module to prevent use of Pickle"""
import ast
import sys
from typing import Any, Generator, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata as impmd
else:
    import importlib.metadata as impmd


_PICKLE_MSG = "PKL000: Unsafe use of pickle module"


class Plugin(object):
    name = __name__
    version = impmd.version(__name__)

    def __init__(self) -> None:
        pass

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        yield 1, 0, _PICKLE_MSG, type(self)

