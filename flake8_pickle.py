"""Flake8 module to prevent use of Pickle"""
import ast
import sys
from typing import Any, Generator, List, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata as impmd
else:
    import importlib.metadata as impmd


_PICKLE_MSG = "PKL000: Unsafe use of pickle module"
_PANDAS_MSG = "PKL001: Unsafe use of Pandas pickle functionality"


class PickleVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int, str]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name == "pickle":
                self.problems.append((node.lineno, node.col_offset, _PICKLE_MSG))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "pickle":
            self.problems.append((node.lineno, node.col_offset, _PICKLE_MSG))
        self.generic_visit(node)


class Plugin(object):
    name = __name__
    version = impmd.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        pickle_visitor = PickleVisitor()
        pickle_visitor.visit(self._tree)
        for lineno, colno, msg in pickle_visitor.problems:
            yield lineno, colno, msg, type(self)


