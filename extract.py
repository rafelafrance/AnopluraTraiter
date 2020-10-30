#!/usr/bin/env python3

"""Extract src traits from scientific literature (PDFs to text)."""

import json

from traiter.pylib.util import clean_text

from src.pylib.util import OUTPUT_DIR, TXT_DIR
from src.matchers.pipeline import PIPELINE


def main():
    """Extract data from the files."""
    # pdf.pdf2txt(PDF_DIR, TXT_DIR)
    j_path = OUTPUT_DIR / 'raw_text.jsonl'
    if j_path.exists():
        j_path.unlink()
    for txt in TXT_DIR.glob('*.txt'):
        with open(txt) as txt_file, open(j_path, 'a') as j_file:
            text = txt_file.read()
            text = clean_text(text)
            doc = PIPELINE.nlp(text)
            for sent in doc.sents:
                rec = json.dumps({'text': sent.text.strip()})
                j_file.write(rec)
                j_file.write('\n')

    #         traits = parse(text)
    #
    #         from pprint import pp
    #         pp(dict(traits))
    #         break


if __name__ == '__main__':
    main()
