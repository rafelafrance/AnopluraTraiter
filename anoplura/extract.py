#!/usr/bin/env python3

import argparse
import textwrap
from copy import deepcopy
from pathlib import Path

from anoplura.pylib import pipeline
from anoplura.pylib.writers.html_writer import html_writer


def main(args):
    nlp = pipeline.build()

    with args.text.open() as in_file:
        lines = [ln.strip() for ln in in_file.readlines()]

    rows = [{"doc": doc} for doc in nlp.pipe(lines)]

    if args.html_file:
        copied = deepcopy(rows)
        html_writer(args, copied)


def parse_args():
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from lice papers."""),
    )

    arg_parser.add_argument(
        "--text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Path to the text file to parse.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
