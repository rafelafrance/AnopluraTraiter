"""Utilities for converting PDFs into text."""

import re
from pathlib import Path

import pdftotext
from traiter.util import FLAGS

from .db import connect
from .util import now


def import_files(paths, type_):
    """Load files into the database."""
    for path in paths:
        path = Path(path)
        doc_id = path.name
        if type_ == 'pdf':
            pdf_to_text(path, doc_id)
        else:
            import_text(path, doc_id)


def pdf_to_text(path, doc_id):
    """Load one PDF into the database."""
    with open(path, 'rb') as handle:
        pdf = pdftotext.PDF(handle)
    text = '\n\n'.join(pdf)
    text_to_db(doc_id, path, text, 'pdf to text')


def import_text(path, doc_id):
    """Load a text file and import it."""
    with open(path) as handle:
        text = handle.read()
        text_to_db(doc_id, path, text, 'text import')


def text_to_db(doc_id, path, text, method):
    """Import a text file into the database."""
    sql = """
        INSERT OR REPLACE INTO docs
            (doc_id, path, loaded, edited, extracted, method, raw, edits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
    with connect() as cxn:
        cxn.execute(
            sql,
            (doc_id, str(path), now(), '', '', method, text, text))


def clean_text_more(text):
    """Clean peculiarities particular to these guides."""
    text = re.sub(r'(?<= [a-z] -) \s (?= [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<= [a-z]) \s (?= - [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<=[a-z]) / (?=[a-z])', 'l', text, flags=FLAGS)
    return text
