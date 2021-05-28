#!/usr/bin/env python3

"""Extract anoplura traits from scientific literature (PDFs to text)."""

import argparse
import textwrap
from copy import deepcopy

from anoplura.pylib.pipeline import pipeline
from anoplura.writers.html_writer import html_writer


def main(args):
    """Extract data from the files."""
    nlp = pipeline()
    rows = []

    with open(args.text) as in_file:
        lines = [ln.strip() for ln in in_file.readlines()]

    for doc in nlp.pipe(lines):
        rows.append({'doc': doc})

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
        '--text', '-t', help="""Path to the text file to parse.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
