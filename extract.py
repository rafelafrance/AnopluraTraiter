#!/usr/bin/env python3

"""Extract lice traits from scientific literature (PDFs to text)."""

from lice.pylib.util import DOC_DIR
from lice.matchers.matcher import Matcher

DOCS = ['270-Lemurpediculus_2_n_spp.pdf']


def main():
    """Extract data from the files."""
    matcher = Matcher()

    for path in DOCS:
        with open(DOC_DIR / path) as in_doc:
            lines = in_doc.readlines()
        for line in lines:
            doc = matcher.parse(line)
            # if doc[0]._.label != 'anoplura':
            #     continue
            # print(doc)


if __name__ == '__main__':
    main()
