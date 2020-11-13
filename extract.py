#!/usr/bin/env python3

"""Extract src traits from scientific literature (PDFs to text)."""

import argparse
import sys
import textwrap
from pathlib import Path

from traiter.pylib.util import clean_text

from src.matchers.pipeline import Pipeline
from src.pylib.util import TRANS

PAPERS = {
}


def main(args):
    """Extract data from the files."""
    texts = []
    for path in args.paper:
        with open(path) as txt:
            text = txt.read()
            text = clean_text(text, trans=TRANS)
            texts.append(text)

    pipeline = Pipeline()
    for doc in pipeline.nlp.pipe(texts):
        for ent in doc.ents:
            print(ent)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--paper', '-p', action='append', required=True,
        help="""Path to the paper to parse. You may repeat this argument.""")

    arg_parser.add_argument(
        '--dir', '-d',
        help="""Directory that contains the paper. Use this if all of the
            papers are in the same directory.""")

    args = arg_parser.parse_args()

    # Convert the --paper arguments into paths
    papers = []
    for paper in args.paper:
        paper = Path(args.dir) / paper if args.dir else Path(paper)
        papers.append(paper)

    # Make sure the files exist
    errors = False
    for paper in papers:
        if not paper.exists():
            print(f'Error: "{paper}" does not exist.')
            errors = True
    if errors:
        sys.exit(1)

    args.paper = papers

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
