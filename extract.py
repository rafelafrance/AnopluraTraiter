#!/usr/bin/env python3

"""Extract lice traits from scientific literature (PDFs to text)."""

from pdfminer.high_level import extract_text

from lice.pylib.util import PDF_DIR
from lice.pylib.segmenter import clean_pdf
from lice.matchers.matcher import Matcher

DOCS = ['270-Lemurpediculus_2_n_spp.pdf']


def main():
    """Extract data from the files."""
    matcher = Matcher()

    for path in DOCS:
        path = str(PDF_DIR / path)
        text = extract_text(path)
        text = clean_pdf(text)
        traits = matcher.parse(text)


if __name__ == '__main__':
    main()
