#!/usr/bin/env python3

import argparse
import re
import textwrap
from pathlib import Path

from pylib import pipeline
from traiter.pylib import util
from writers import html_writer


def main(args: argparse.Namespace) -> None:
    nlp = pipeline.build()

    with args.text.open() as in_file:
        text = " ".join(in_file.readlines())
        text = util.clean_text(text)
        text = remove_figures(text)
        doc = nlp(text)
        traits = [e._.trait for e in doc.ents]
        html_writer.writer(traits, text, args.html_file)


def remove_figures(text: str) -> str:
    return re.sub(
        r" \s* \( [^)]* fig [^)]+ \) ", "", text, flags=re.IGNORECASE | re.VERBOSE
    )


def parse_args() -> argparse.Namespace:
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
