#!/usr/bin/env python3

"""Extract anoplura traits from scientific literature (PDFs to text)."""
import subprocess
from collections import Counter
from os.path import exists, splitext

import regex

from anoplura.pylib.util import PDF_DIR, TXT_DIR

FLAGS = regex.VERBOSE | regex.IGNORECASE

TRANS_TABLE = {'¼': '='}
TRANS = str.maketrans(TRANS_TABLE)


def main():
    """Extract data from the files."""
    pdf2txt()
    for txt in TXT_DIR.glob('*.txt'):
        with open(txt) as txt_file:
            text = txt_file.read()
            pages = text.count('\f')
            lines = text.splitlines()
            clean_pdf(lines, pages)
        break


def pdf2txt():
    """Convert PDF files into text."""
    for pdf in PDF_DIR.glob('*.pdf'):
        txt = TXT_DIR / (splitext(pdf.name)[0] + '.txt')
        if not exists(txt):
            cmd = f'pdftotext {pdf} {txt}'
            subprocess.check_call(cmd, shell=True)


def clean_pdf(text, pages):
    """Remove headers & footers and join hyphenated words etc."""

    # Remove figure notes and abstract
    lines = []
    keys = []
    removing = False
    for ln in text:
        if regex.match(r'^ \s* ( abstract | fig[.u] )', ln, flags=FLAGS):
            removing = True
        elif len(ln) == 0:
            removing = False
        elif removing:
            pass
        elif regex.match(r'^ \s* \d{0,4} \s* $', ln, flags=FLAGS):
            pass
        else:
            lines.append(ln)
            key = regex.sub(r'^\s*\d+|\d+\s*$', ' ', ln)
            key = ' '.join(key.split())
            keys.append(key)

    counts = Counter(keys)
    patterns = []
    for pattern, n in counts.most_common(4):
        if n >= pages / 2:
            pattern = regex.sub(r'\s+', r'\s*', pattern)
            pattern = fr'^ [\s\d]* {pattern} [\s\d]* $'
            patterns.append(pattern)
            print(pattern)

    pattern = ' | '.join(patterns)
    pattern = regex.compile(pattern, flags=FLAGS)

    lines = [ln for ln in lines if not pattern.match(ln)]

    # Joining hyphens has to happen after the removal of headers & footers
    # text = regex.sub(r' [–-] \n ([a-z]) ', r'\1', text, flags=FLAGS)

    # text = ' '.join(text.split())

    for ln in lines:
        print(ln)

    # Space normalize text
    # return text


if __name__ == '__main__':
    main()
