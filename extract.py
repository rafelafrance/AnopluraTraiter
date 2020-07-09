#!/usr/bin/env python3

"""Extract anoplura traits from scientific literature (PDFs to text)."""

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams

from anoplura.matchers.matcher import Matcher
from anoplura.pylib.segmenter import clean_pdf
from anoplura.pylib.util import PDF_DIR

DOCS = ['270-Lemurpediculus_2_n_spp.pdf']


def main():
    """Extract data from the files."""
    laparams = LAParams(
        # line_overlap=0.5,
        # char_margin=2.0,
        # line_margin=0.5,
        # word_margin=0.1,
        boxes_flow=-0.5,
        # detect_vertical=False,
        # all_texts=False
    )

    matcher = Matcher()

    for path in DOCS:
        path = str(PDF_DIR / path)
        # text = extract_text(path, laparams=laparams)
        text = [p.groups[0].get_text()
                for p in extract_pages(path, laparams=laparams)]
        text = clean_pdf(''.join(text))
        traits = matcher.parse(text)

        from pprint import pp
        pp(dict(traits))


if __name__ == '__main__':
    main()
