#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib import pipeline
from traiter.pylib.util import clean_text
from writers import html_writer


def main(args):
    nlp = pipeline.build()

    with args.text.open() as in_file:
        text = " ".join(in_file.readlines())
        text = clean_text(text)
        doc = nlp(text)
        traits = [e._.trait for e in doc.ents if e._.trait]
        html_writer.writer(traits, text, args.html_file)


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
