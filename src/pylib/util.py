"""Utilities and constants."""

import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

NAME = 'anoplura'

DATA_DIR = Path('.') / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
VOCAB_DIR = Path('.') / 'src' / 'vocabulary'


def log(msg):
    """Log a status message."""
    print(f'{now()} {msg}')


def now():
    """Generate a timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def today():
    """Get today's date."""
    return now()[:10]


@contextmanager
def get_temp_dir(prefix, where=None, keep=False):
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = mkdtemp(prefix=prefix, dir=where)
    # os.environ['SQLITE_TMPDIR'] = temp_dir

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)
