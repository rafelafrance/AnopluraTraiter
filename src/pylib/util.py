"""Utilities and constants."""

from pathlib import Path

import traiter.pylib.terms as terms

DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = Path.cwd() / 'output'
MODEL_DIR = Path.cwd() / 'models'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

NUMERIC_STEP = 'numerics'
GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
ATTACH_STEP = 'attach'
DESCRIPTION_STEP = 'description'

ABBREVS = """
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    mm cm m
    al Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Figs Hist
    IUCN Inst Int Lond Me´m Mol Mus Nat nov Physiol Rep Sci Soc sp Syst Zool
    """

TERMS = terms.read_terms(VOCAB_DIR / 'common_terms.csv')
TERMS += terms.read_terms(VOCAB_DIR / 'anoplura_terms.csv')
TERMS += terms.read_terms(VOCAB_DIR / 'anoplura_species.csv')
TERMS += terms.abbrev_species(TERMS, label='anoplura')
TERMS += terms.taxon_level_terms(
    TERMS, label='anoplura', new_label='anoplura_genus', level='genus')
TERMS += terms.itis_terms(taxon='Mammalia', label='mammalia')
TERMS += terms.abbrev_species(TERMS, label='mammalia')

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

CLOSE = [')', ']']
COLON = [':']
COMMA = [',']
CROSS = ['x', '×', '⫻']  # ⫻ = 0x3f
DASH = ['–', '-', '––', '--']
DOT = ['.']
EQ = ['=', '¼']  # ¼ = 0xbc
INT_RE = r'^\d+$'
NUMBER_RE = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SEMICOLON = [';']
SLASH = ['/']
BREAK = DOT + SEMICOLON
