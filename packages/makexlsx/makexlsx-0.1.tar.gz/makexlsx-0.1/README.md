# makexlsx \-- make XLSX spreadsheet from tabular data files

Do you often import CSV files to Excel, and find yourself doing the same
mouse-clicky nonsense every time to make it look nice? Would you like
all that fiddling with column widths, autofiltering, text wrapping and
centering to just happen by magic? Yes, so would I. Which is why I wrote
this:

-   It takes one or more tabular data files (not just CSV, but any
    format that [tablib](https://pypi.org/project/tablib) will accept)
    and produces an XLSX workbook with one table per sheet.
-   If a table header is present, it\'s made bold, the header line is
    frozen, and autofiltering is applied to all the columns.
-   Wrapping is applied to any columns that have line breaks in their
    values, or lines beyond a certain (user-defined) length.
-   All numeric columns are right-justified. Non-numeric columns are
    centred if their width is below a certain (user-defined) size,
    otherwise they are left-justified.
-   It uses the amazing
    [xlsxwriter](https://pypi.org/project/XlsxWriter) package to do all
    the output.
