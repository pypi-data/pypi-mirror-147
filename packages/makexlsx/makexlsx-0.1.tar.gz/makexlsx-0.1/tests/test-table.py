# Test table conversion.

from makexlsx import xlsx


def test_convert():
    xlsx.make_xlsx("test-table.xlsx", ["test-table.csv"])
