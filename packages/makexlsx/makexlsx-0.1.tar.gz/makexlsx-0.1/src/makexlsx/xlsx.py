"""
Interface to xlsxwriter.
"""

import tablib

from pathlib import Path
from io import BytesIO

from xlsxwriter import Workbook

# Interface to other programs.  Treat everything else as internal!
__all__ = ["Workbook", "read_table", "add_table"]


def make_xlsx(outfile, files, **kw):
    """
    Make an XLSX file.

    Args:
        outfile (str): Excel file to make
        files (iterable): table files to read
        kw (dict): formatting options
    """

    # Initialise output.
    buf = BytesIO()
    opts = dict(strings_to_numbers=True)
    wb = Workbook(buf, opts)
    names = kw.pop("names", [])

    # Read and convert tabular data files.
    for idx, filename in enumerate(files):
        path = Path(filename)
        table, header = read_table(path)
        title = names[idx] if idx < len(names) else path.stem
        add_table(wb, title, table, header=header, **kw)

    # Finalize output.
    wb.close()

    # Write to output file.
    with open(outfile, "wb") as f:
        f.write(buf.getvalue())


def read_table(path):
    """
    Read table data from a file.

    Args:
        path (Path): Table filename

    Returns:
        tuple (table rows, header)
    """

    # TODO: catch data import errors properly
    dataset = tablib.Dataset()

    try:
        dataset.load(path.read_text())
    except UnicodeDecodeError:
        dataset.load(path.read_bytes())

    return dataset, dataset.headers


def add_table(wb, title, table, header=None, formats={}, wrapwidth=80,
              maxcentre=20, scalewidth=1.2, minwidth=12, zoom=100):
    """
    Add a table to a workbook.

    Args:
        wb (xl.Workbook): Workbook to add to
        title (str): Table title
        table (iterable): Lines containing each table row
        header (iterable or None): Table header strings
        formats (dict): Cell formats
        wrapwidth (int): Maximum width before wrapping triggered
        maxcentre (int): Maximum width before not centering
        scalewidth (float): Excel column width scaling factor
        minwidth (float): minimum column width
        zoom (int): Excel sheet zoom factor

    Returns:
        worksheet
    """

    # Get table size.
    nrows = len(table)
    ncols = max(len(row) for row in table)

    if header:
        ncols = max(ncols, len(header))

    # Default parameters per column.
    colwidth = [0] * ncols                # Widths
    colalign = ["center"] * ncols         # Alignment
    colwrap = [False] * ncols             # Whether to wrap
    colnumeric = [True] * ncols           # Whether numeric

    # Set up helper function to get column info.
    def analyze(rowdata, is_header):
        for col, value in enumerate(rowdata):
            if value:
                # Get text lines and their maximum width.
                lines = str(value).split("\n")
                width = max(len(line) for line in lines)
            else:
                # Skip empty values.
                continue

            # Update the maximum column width.
            colwidth[col] = max(colwidth[col], width)

            # If the width exceeds the maximum for centring, left-justify.
            if width > maxcentre:
                colalign[col] = "left"

            # Check for wrapping -- more than one line, or width too big.
            if len(lines) > 1 or width > wrapwidth:
                colwrap[col] = True

            # If any non-header value isn't numeric, nor is the column.
            if not is_header and not is_numeric(value):
                colnumeric[col] = False

    # Analyze header and row data to update column info.
    if header:
        analyze(header, True)

    for rowdata in table:
        analyze(rowdata, False)

    # Right-align all numeric columns.
    for col in range(ncols):
        if colnumeric[col]:
            colalign[col] = "right"

    # Add a new worksheet.
    ws = wb.add_worksheet(title)

    # Set up columns.
    for col in range(ncols):
        fmt = wb.add_format()

        fmt.set_align("top")
        fmt.set_align(colalign[col])
        fmt.set_text_wrap(colwrap[col])

        width = min(colwidth[col], wrapwidth)
        width = max(width * scalewidth, minwidth)

        ws.set_column(col, col, width, fmt)

    # Add a header if required.
    if header:
        for col, value in enumerate(header):
            fmt = wb.add_format()

            fmt.set_bold()
            fmt.set_align("vcenter")
            fmt.set_align("center")
            fmt.set_text_wrap(colwrap[col])

            ws.write(0, col, value, fmt)

    # Add the data.
    startrow = 1 if header else 0
    for row, rowdata in enumerate(table, startrow):
        for col, value in enumerate(rowdata):
            props = formats.get((row, col), None)

            if props:
                fmt = wb.add_format(props)
                fmt.set_align("top")
                fmt.set_align(colalign[col])
                fmt.set_text_wrap(colwrap[col])
            else:
                fmt = None

            ws.write(row, col, value, fmt)

    # Finalize sheet.
    if header:
        ws.autofilter(0, 0, nrows, ncols - 1)
        ws.freeze_panes(1, 0)

    ws.set_zoom(zoom)

    return ws


def is_numeric(value):
    "Return whether a string value represents a number."

    try:
        float(value)
        return True
    except ValueError:
        return False
