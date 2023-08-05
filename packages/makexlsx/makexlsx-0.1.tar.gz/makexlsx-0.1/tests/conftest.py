"""
Common test stuff.
"""

import os
from pytest import fixture
from makexlsx import __version__


def pytest_report_header(config):
    return "package: makexlsx, version %s" % __version__


@fixture(autouse=True)
def setup(monkeypatch):
    "Global test setup."

    # Run tests from this directory.
    path = os.path.dirname(__file__)
    monkeypatch.chdir(path)
