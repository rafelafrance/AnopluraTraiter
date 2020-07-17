"""Common functions for dealing with the database."""

import sqlite3
import subprocess
from datetime import datetime
from os import fspath, remove
from pathlib import Path
import pandas as pd

from .util import DATA_DIR, NAME

DB = DATA_DIR / f'{NAME}.sqlite3.db'
SCRIPT_PATH = Path('.') / 'src' / 'sql'


def connect(path=None):
    """Connect to an SQLite database."""
    path = path if path else str(DB)
    cxn = sqlite3.connect(path)

    cxn.execute('PRAGMA page_size = {}'.format(2 ** 16))
    cxn.execute('PRAGMA busy_timeout = 10000')
    cxn.execute('PRAGMA journal_mode = WAL')
    return cxn


def create():
    """Create the database."""
    script = fspath(SCRIPT_PATH / 'create_db.sql')
    cmd = f'sqlite3 {DB} < {script}'

    if DB.exists():
        remove(DB)

    return subprocess.check_call(cmd, shell=True)


def backup_database():
    """Backup the SQLite3 database."""
    now = datetime.now()
    name = str(DB)
    backup = f'{name[:-3]}.{now.strftime("%Y-%m-%d")}.db'
    cmd = f'cp {name} {backup}'

    return subprocess.check_call(cmd, shell=True)


def select_docs():
    """Get guides as a dataframe."""
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
