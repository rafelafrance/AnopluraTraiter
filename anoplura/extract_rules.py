#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from anoplura.pylib import pipeline
from anoplura.pylib import text_util as util
from anoplura.writers import html_writer, md_writer


def main(args: argparse.Namespace) -> None:
    nlp = pipeline.build()

    with args.text_input.open() as in_file:
        text = " ".join(in_file.readlines())
        text = util.clean_text(text, eol_hyphens=True)
        doc = nlp(text)

        if args.html_output:
            html_writer.writer(doc, args.html_output)

        if args.markdown_output:
            md_writer.write(doc, args.markdown_output)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse data from papers describing lice."""),
    )

    arg_parser.add_argument(
        "--text-input",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Path to the text file to parse.""",
    )

    arg_parser.add_argument(
        "--html-output",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--markdown-output",
        type=Path,
        metavar="PATH",
        help="""Output the results to this markdown file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
