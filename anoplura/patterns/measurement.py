"""Parse size notations."""

import re

import spacy
from traiter.const import FLOAT_RE, INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import list_to_re_choice, to_positive_float, to_positive_int

from anoplura.pylib.const import COMMON_PATTERNS, TERMS

UNITS_RE = [t['pattern'] for t in TERMS if t['label'] == 'metric_length']
UNITS_RE = '(?<![A-Za-z])' + list_to_re_choice(UNITS_RE) + r'\b'

BODY_PART_ENTITIES = """ body_part setae setae_abbrev """.split()
LENGTH_ENTITIES = """ measurement mean sample """.split()
LENGTH_WORDS = """ length len """.split()
MAXIMUM = """ maximum max """.split()
WIDTH = """ width """.split()

DECODER = COMMON_PATTERNS | {
    'bar': {'LOWER': {'IN': ['bar', 'bars']}},
    'mean_word': {'LOWER': 'mean'},
    './,': {'IS_PUNCT': True},
    'n': {'LOWER': 'n'},
    'measurement': {'ENT_TYPE': 'measurement'},
    'mean': {'ENT_TYPE': 'mean'},
    'sample': {'ENT_TYPE': 'sample'},
    'total': {'LOWER': 'total', 'OP': '?'},
    'part': {'ENT_TYPE': {'IN': BODY_PART_ENTITIES}},
    'len': {'LOWER': {'IN': LENGTH_WORDS}},
    'non_ent': {'ENT_TYPE': ''},
    'max': {'LOWER': {'IN': MAXIMUM}},
    'width': {'LOWER': {'IN': WIDTH}},
}

MEASUREMENT = MatcherPatterns(
    'measurement',
    on_match='measurement.v1',
    decoder=DECODER,
    patterns=[
        '99.9 cm',
        '99.9 - 99.9 cm',
    ],
)

MEAN = MatcherPatterns(
    'mean',
    on_match='mean.v1',
    decoder=DECODER,
    patterns=['mean_word ./,? 99.9 cm?'],
)

SAMPLE = MatcherPatterns(
    'sample',
    on_match='sample.v1',
    decoder=DECODER,
    patterns=['n = 99'],
)

LENGTH = MatcherPatterns(
    'length',
    on_match='length.v1',
    decoder=DECODER,
    patterns=[
        ('total? part len non_ent? non_ent? bar? ./,* '
         'measurement ./,? mean? ./,* sample? ./,?'),
    ],
)

MAX_WIDTH = MatcherPatterns(
    'max_width',
    on_match='max_width.v1',
    decoder=DECODER,
    patterns=[
        ('max part width non_ent? non_ent? bar? ./,* '
         'measurement ./,? mean? ./,* sample? ./,?'),
    ],
)


@spacy.registry.misc(MAX_WIDTH.on_match)
def max_width(ent):
    """Enrich the match."""
    data = {}
    for token in ent:
        data |= token._.data
    ent._.data = data


@spacy.registry.misc(LENGTH.on_match)
def length(ent):
    """Enrich a size match."""
    data = {}
    for token in ent:
        data |= token._.data

    if ent.text.lower().find('total') > -1:
        ent._.new_label = 'total_length'
    ent._.data = data


@spacy.registry.misc(MEASUREMENT.on_match)
def measurement(ent):
    """Enrich a measurement match."""
    values = re.findall(FLOAT_RE, ent.text)
    values = [to_positive_float(v) for v in values]

    ent._.data = {k: v for k, v in zip(['low', 'high'], values)}

    match = re.search(UNITS_RE, ent.text)
    units = match.group(0)
    ent._.data['length_units'] = units


@spacy.registry.misc(MEAN.on_match)
def mean(ent):
    """Convert the span into a single float."""
    match = re.search(FLOAT_RE, ent.text)
    value = match.group(0)

    match = re.search(UNITS_RE, ent.text.lower())
    units = match.group(0) if match else None

    ent._.data = {'mean': to_positive_float(value)}

    if units:
        ent._.data['mean_units'] = units


@spacy.registry.misc(SAMPLE.on_match)
def sample(ent):
    """Convert the span into a single integer."""
    match = re.search(INT_RE, ent.text)
    value = match.group(0)
    ent._.data = {'n': to_positive_int(value)}
