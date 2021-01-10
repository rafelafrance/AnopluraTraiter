"""Utilities and constants."""

from pathlib import Path

from traiter.terms.itis import Itis

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

TERMS = Itis.shared('animals insect_anatomy numerics')
TERMS += Itis.shared('units', labels='metric_length')
TERMS += Itis.read_csv(VOCAB_DIR / 'common_terms.csv')
TERMS += Itis.read_csv(VOCAB_DIR / 'anoplura_terms.csv')
TERMS += Itis.read_csv(VOCAB_DIR / 'anoplura_species.csv')
TERMS += Itis.abbrev_species(TERMS, label='anoplura')
TERMS += Itis.taxon_level_terms(
    TERMS, label='anoplura', new_label='anoplura_genus', level='genus')
TERMS += Itis.taxon_level_terms(TERMS, label='mammalia')
TERMS += Itis.abbrev_species(TERMS, label='mammalia')

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

CLOSE = [')', ']']
COLON = [':']
COMMA = [',']
CROSS = ['x', '×', '⫻']  # ⫻ = 0x3f
DASH = ['–', '-', '––', '--']
DOT = ['.']
EQ = ['=', '¼']  # ¼ = 0xbc
FLOAT_RE = r'^\d+(\.\d*)?$'
INT_RE = r'^\d+$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SEMICOLON = [';']
SLASH = ['/']
BREAK = DOT + SEMICOLON

MISSING = """ without missing lack lacking except excepting """.split()
