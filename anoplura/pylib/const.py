"""Utilities and constants."""

from pathlib import Path

from traiter.const import CLOSE, COMMA, CROSS, DASH, EQ, FLOAT_TOKEN_RE, OPEN
from traiter.terms.itis import Itis

DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = Path.cwd() / 'output'
MODEL_DIR = Path.cwd() / 'models'
VOCAB_DIR = Path.cwd() / 'anoplura' / 'vocabulary'

# #########################################################################
# Term relate constants
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

REPLACE = TERMS.pattern_dict('replace')

# #########################################################################
# Tokenizer constants
ABBREVS = """
        Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
        mm. cm. m.
        al. Am. Anim. Bio. Biol. Bull. Bull. Conserv. D.C. Ecol. Entomol. Fig. Figs.
        Hist. Inst. Int. Lond. Me´m. Mol. Mus. Nat. nov. Physiol. Rep. Sci. Soc.
        sp. Syst. Zool.
        """.split()

# #########################################################################
# Pattern related constants
MISSING = """ no without missing lack lacking except excepting """.split()
EQ_ = EQ + ['¼']
CONJ = ['and', '&', 'or']

COMMON_PATTERNS = {
    '(': {'TEXT': {'IN': OPEN}},
    ')': {'TEXT': {'IN': CLOSE}},
    '=': {'TEXT': {'IN': EQ_}},  # ¼ = 0xbc
    'x': {'LOWER': {'IN': CROSS + ['⫻']}},  # ⫻ = 0x3f
    '-': {'TEXT': {'IN': DASH}},
    '-/to': {'LOWER': {'IN': DASH + ['to']}},
    '&/or': {'LOWER': {'IN': CONJ}},
    '&/,/or': {'LOWER': {'IN': CONJ + COMMA}},
    '99': {'IS_DIGIT': True},
    '99.9': {'TEXT': {'REGEX': FLOAT_TOKEN_RE}},
    'cm': {'ENT_TYPE': 'metric_length'},
    'part': {'ENT_TYPE': 'part'},
    'any_part': {'ENT_TYPE': {'IN': ['part_loc', 'part']}},
    'part_loc': {'ENT_TYPE': {'IN': ['part_loc']}},
    'missing': {'LOWER': {'IN': MISSING}},
    'not_ent': {'ENT_TYPE': ''},
}

# #########################################################################
# Remove these stray entities
FORGET = """ number_word part_loc sclerotin stop """.split()
