"""Utilities for converting PDFs into text."""

import re
from pathlib import Path

import pandas as pd
import pdftotext
from traiter.util import FLAGS

from .db import connect
from .util import now


# Todo move these to pipes
def clean_text_more(text):
    """Clean peculiarities particular to these guides."""
    text = re.sub(r'(?<= [a-z] -) \s (?= [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<= [a-z]) \s (?= - [a-z])', '', text, flags=FLAGS)
    text = re.sub(r'(?<=[a-z]) / (?=[a-z])', 'l', text, flags=FLAGS)
    return text


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


def select_docs():
    """Get documents as a dataframe."""
    sql = """
        select doc_id, loaded, edited, extracted, method, path
          from docs
      order by doc_id;"""
    with connect() as cxn:
        return pd.read_sql(sql, cxn)


def select_doc(doc_id):
    """Get a document for editing."""
    sql = """select edits from docs where doc_id = ?;"""
    with connect() as cxn:
        return cxn.execute(sql, (doc_id,)).fetchone()[0]


def update_doc(doc_id, edits):
    """Update the document with edits."""
    sql = """update docs set edits = ? where doc_id = ?;"""
    with connect() as cxn:
        cxn.execute(sql, (edits, doc_id))
        cxn.commit()


def reset_doc(doc_id):
    """Reset the doc edits to back to the original text."""
    sql = """update docs set edits = raw where doc_id = ?;"""
    with connect() as cxn:
        cxn.execute(sql, (doc_id,))
        cxn.commit()
