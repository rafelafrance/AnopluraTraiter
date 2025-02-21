#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib import pipeline
from pylib.writers import html_writer
from traiter.pylib.util import clean_text


def main(args):
    nlp = pipeline.build()

    with args.text.open() as in_file:
        text = " ".join(in_file.readlines())
        text = clean_text(text)
        html_writer.writer(nlp, text)


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
