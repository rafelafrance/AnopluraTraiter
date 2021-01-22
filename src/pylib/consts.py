"""Utilities and constants."""

from pathlib import Path

from traiter.consts import CROSS, DOT, EQ, SEMICOLON
from traiter.terms.itis import Itis

DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = Path.cwd() / 'output'
MODEL_DIR = Path.cwd() / 'models'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

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

CROSS_ = CROSS + ['⫻']  # ⫻ = 0x3f
EQ_ = EQ + ['¼']  # ¼ = 0xbc
BREAK = DOT + SEMICOLON

MISSING = """ without missing lack lacking except excepting """.split()
