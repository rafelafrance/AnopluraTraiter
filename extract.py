#!/usr/bin/env python3

"""Extract src traits from scientific literature (PDFs to text)."""

import argparse
import sys
import textwrap
from copy import deepcopy
from pathlib import Path

from traiter.pylib.util import clean_text

from src.matchers.pipeline import Pipeline
from src.pylib.util import TRANS
from src.writers.html_writer import html_writer


def main(args):
    """Extract data from the files."""
    pass
    # pipeline = Pipeline()
    # rows = []
    # for i, doc in enumerate(pipeline.nlp.pipe({t[1] for t in texts})):
    #     row = {'path': '', 'doc': doc}
    #     rows.append(row)
    #
    # if args.html_file:
    #     copied = deepcopy(rows)
    #     html_writer(args, copied)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--pdf', '-p', help="""Path to the PDF paper to parse.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    arg_parser.add_argument(
        '-t', '--temp-dir', metavar='DIR', default=None,
        help="""Place temporary files in this directory. All files will be
            deleted after aTRAM completes. The directory must exist.""")

    arg_parser.add_argument(
        '--keep-temp-dir', action='store_true',
        help="""This flag will keep the temporary files in the --temp-dir
            around for debugging.""")

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
