#!/usr/bin/env python3

"""Extract src traits from scientific literature (PDFs to text)."""

import argparse
import textwrap
from copy import deepcopy

from src.matchers.pipeline import Pipeline
from src.writers.html_writer import html_writer


def main(args):
    """Extract data from the files."""
    pipeline = Pipeline()
    rows = []
    for doc in enumerate(pipeline.nlp.pipe({t[1] for t in args.text})):
        row = {'path': '', 'doc': doc}
        rows.append(row)

    if args.html_file:
        copied = deepcopy(rows)
        html_writer(args, copied)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--text', '-t', action='append',
        help="""Path to the text file to parse.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
