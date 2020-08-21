"""Get terms from various sources (CSV files or SQLite database."""

from traiter.pylib.terms import VOCAB_DIR, itis_terms, read_terms

LICE_TERMS = VOCAB_DIR / 'anoplura.csv'
COMMON_TERMS = VOCAB_DIR / 'common.csv'

TERMS = read_terms(LICE_TERMS)
TERMS += read_terms(COMMON_TERMS)

TERMS += itis_terms('Anoplura', abbrev=True)
TERMS += itis_terms('Mammalia', abbrev=True)

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
