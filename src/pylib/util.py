"""Utilities and constants."""

from datetime import datetime
from pathlib import Path

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
