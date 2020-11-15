#!/usr/bin/env python3

"""Convert a PDF to HTML and then to text."""

import argparse
import regex
import subprocess
import textwrap
from math import floor
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup
from traiter.pylib.util import clean_text, get_temp_dir

from src.matchers.pipeline import Pipeline
from src.pylib.util import TRANS, DASH


def main(args):
    """Convert the PDF to a text format we can use.

    The standard utilities for for converting PDFs don't really do what we need.
    """
    with get_temp_dir(where=args.temp_dir, keep=args.keep_temp_dir) as temp_dir:
        page_file = NamedTemporaryFile(
            suffix='.html', mode='r', dir=temp_dir, delete=(not args.keep_temp_dir))
        to_html(args, page_file)
        page = clean_html(page_file)
        page_file.close()

    lines = order_lines(args, page)
    lines = [str(ln[4]) for ln in lines]

    lines = filter_lines(args, lines)
    text = join_lines(lines)
    lines = split_sentences(text)

    for ln in lines:
        args.text_file.write(ln)
        args.text_file.write('\n')


def split_sentences(text):
    """Split the text into sentences."""
    pipeline = Pipeline()
    doc = pipeline.nlp(text)
    lines = [x for s in doc.sents if (x := ' '.join(s.text.split()))]
    # lines = [s.text for s in doc.sents]
    return lines


def join_lines(lines):
    """Join lines into a text blob."""
    dash = '|'.join(DASH)
    text = '\n'.join(lines)
    text = regex.sub(rf'(\w)(?:{dash})\n(\w)', r'\1\2', text)
    return text


def filter_lines(args, lines):
    """Filter lines like header, footers, and figures."""
    if args.remove:
        return [ln for ln in lines if not args.remove.search(ln)]
    return lines


def order_lines(args, page):
    """Convert html page into text paragraphs."""
    lines = []
    page = BeautifulSoup(page, features='lxml')
    for i, div in enumerate(page.find_all('div')):
        width = int(regex.search(r'width:(\d+)', div['style'])[1])
        half = width // 2
        for para in div.find_all('p'):
            top = int(regex.search(r'top:(\d+)', para['style'])[1])
            left = int(regex.search(r'left:(\d+)', para['style'])[1])
            column = floor(left // half)
            text = clean_text(para.get_text(), trans=TRANS[args.mojibake])
            lines.append((i, column, top, left, text))
    return lines


def to_html(args, page_file):
    """Convert the PDF to html."""
    cmd = ['pdftohtml -s -i -q -noframes', args.pdf, page_file.name]
    cmd = ' '.join(cmd)
    subprocess.run(cmd, shell=True)


def clean_html(page_file):
    """Setup the HTML file for further processing."""
    page = page_file.read()
    page = page.replace('&#160;', ' ')  # Replace non-breaking spaces
    page = page.replace('-<br/>', '')  # Join words split with a hyphen & line break
    page = page.replace('<br/>', ' ')  # Remove hard line breaks
    return page


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--pdf', '-p', help="""Path to the PDF paper to parse.""")

    arg_parser.add_argument(
        '--text-file', '-T', type=argparse.FileType('w'),
        help="""Output the results to this text file.""")

    arg_parser.add_argument(
        '-t', '--temp-dir', metavar='DIR', default=None,
        help="""Place temporary files in this directory. All files will be
            deleted after aTRAM completes. The directory must exist.""")

    trans = list(TRANS.keys())
    arg_parser.add_argument(
        '--mojibake', default=trans[0], choices=trans,
        help="""Translation table to use for converting odd mojibake.""")

    arg_parser.add_argument(
        '-r', '--remove', action='append',
        help=r"""Remove lines that have this pattern. You may need to quote this
            argument. Examples: --remove '^Journal of' --remove '^\d+$'.""")

    arg_parser.add_argument(
        '--keep-temp-dir', action='store_true',
        help="""This flag will keep the temporary files in the --temp-dir
            around for debugging.""")

    args = arg_parser.parse_args()

    if args.remove:
        args.remove = regex.compile('|'.join([f'(?:{r})' for r in args.remove]))

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
