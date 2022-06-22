import ast
from typing import Set

from flake8_pickle import Plugin


_MSG_000 = "PKL000: Unsafe use of pickle module"
_MSG_001 = "PKL001: Unsafe use of Pandas pickle functionality"


def _result(code: str) -> Set[str]:
    tree = ast.parse(code)
    plugin = Plugin(tree)
    return {(line, col, msg) for line, col, msg, _ in plugin.run()}


def test_version():
    assert Plugin.version == '0.1.0'


def test_empty():
    assert _result("") == set()


def test_import_pickle():
    assert _result("import pickle") == {(1, 0, _MSG_000)}


def test_import_other():
    assert _result("import requests") == set()


def test_import_multi():
    assert _result("import requests, pickle") == {(1, 0, _MSG_000)}


def test_import_from_pickle():
    assert _result("from pickle import dump") == {(1, 0, _MSG_000)}


def test_import_from_other():
    assert _result("from datetime import time") == set()


_import_in_method_code = """# comment
def write_to_foo(s):
    from pickle import dump
    with open('foo', 'wb') as f:
        dump(s, f)
"""


def test_import_in_method():
    assert _result(_import_in_method_code) == {(3, 4, _MSG_000)}


def test_import_alias_pickle():
    assert _result("import pickle as pandas") == {(1, 0, _MSG_000)}


def test_import_alias_other():
    assert _result("import pandas as pickle") == set()


_import_conditional_code = """
if condition:
    import json as serialization
else:
    import pickle as serialization
"""

def test_import_conditional():
    assert _result(_import_conditional_code) == {(5, 4, _MSG_000)}


_import_from_conditional_code = """
if condition:
    from pickle import dump
else:
    from json import dump
"""

def test_import_conditional():
    assert _result(_import_from_conditional_code) == {(3, 4, _MSG_000)}


def test_import_multiple():
    assert _result("from pickle import dump\nfrom pickle import dumps") == {
        (1, 0, _MSG_000),
        (2, 0, _MSG_000)
    }
