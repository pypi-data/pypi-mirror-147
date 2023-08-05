"""
Command-line interface.
"""

import sys
import argparse as ap

from . import __version__
from .xlsx import make_xlsx

# Program name.
__program__ = "makexlsx"


def main(args=sys.argv[1:]):
    """
    Main function.
    """

    # Parse command arguments.
    class Formatter(ap.RawDescriptionHelpFormatter,
                    ap.ArgumentDefaultsHelpFormatter):
        pass

    p = ap.ArgumentParser(description=__doc__, formatter_class=Formatter)

    p.add_argument("output", metavar="XLSXFILE",
                   help="Excel file to make")

    p.add_argument("file", metavar="FILE", nargs="+",
                   help="tabular data file")

    p.add_argument("-w", "--wrapwidth", type=int, default=80,
                   help="max width before wrapping column")

    p.add_argument("-c", "--maxcentre", type=int, default=20,
                   help="max width of centred columns")

    p.add_argument("-s", "--scalewidth", type=float, default=1.2,
                   help="column width scaling factor")

    p.add_argument("-m", "--minwidth", type=float, default=12,
                   help="minimum column width")

    p.add_argument("-z", "--zoom", type=int, default=100,
                   help="sheet zoom factor")

    p.add_argument("-n", "--name", type=str, action="append",
                   help="set sheet name (may be repeated)")

    p.add_argument("--traceback", action="store_true",
                   help="print traceback on error")

    p.add_argument("-v", "--version", action="version",
                   version="%(prog)s version " + __version__)

    opts = p.parse_args(args)

    # Run things.
    try:
        make_xlsx(opts.output, opts.file,
                  wrapwidth=opts.wrapwidth,
                  maxcentre=opts.maxcentre,
                  scalewidth=opts.scalewidth,
                  minwidth=opts.minwidth,
                  zoom=opts.zoom,
                  names=opts.name or [])

    except Exception as msg:
        if opts.traceback:
            raise
        else:
            sys.exit("Error: " + str(msg))
