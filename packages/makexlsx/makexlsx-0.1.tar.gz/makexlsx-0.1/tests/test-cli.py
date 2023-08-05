# Test command line usage.

from makexlsx.cli import main
from pytest import raises


def test_table():
    main(["test-table.xlsx", "test-table.csv"])


def test_help():
    with raises(SystemExit):
        main(["--help"])
