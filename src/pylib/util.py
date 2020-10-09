"""Utilities and constants."""

from pathlib import Path

from traiter.spacy_nlp.terms import VOCAB_DIR, itis_terms, read_terms


DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = Path.cwd() / 'output'
MODEL_DIR = Path.cwd() / 'models'

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
TERMS += read_terms(VOCAB_DIR / 'common.csv')
TERMS += itis_terms('Anoplura', abbrev=True)
TERMS += itis_terms('Mammalia', abbrev=True)

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

CLOSE = [')', ']']
COLON = [':']
COMMA = [',']
CROSS = ['x', '×', '⫻']  # ⫻ = 0x3f
DASH = ['–', '-', '––', '--']
DOT = ['.']
EQ = ['=', '¼']  # ¼ = 0xbc
INT = r'^\d+$'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SEMICOLON = [';']
SLASH = ['/']
BREAK = DOT + SEMICOLON
