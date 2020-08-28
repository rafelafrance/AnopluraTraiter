"""Utilities and constants."""

from pathlib import Path

from traiter.pylib.terms import VOCAB_DIR, itis_terms, read_terms

DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
ATTACH_STEP = 'attach'

ABBREVS = """
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    mm cm m
    Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Hist IUCN Inst Int
    Lond Me´m Mol Mus Nat Physiol Rep Sci Soc Syst Zool
    """

TERMS = read_terms(VOCAB_DIR / 'anoplura.csv')
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

TERMS += read_terms(VOCAB_DIR / 'common.csv')
TERMS += itis_terms('Anoplura', abbrev=True)
TERMS += itis_terms('Mammalia', abbrev=True)
