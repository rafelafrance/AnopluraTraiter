"""Parse size notations."""

import re

import spacy
from traiter.const import FLOAT_RE, INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import list_to_re_choice, to_positive_float, to_positive_int

from anoplura.pylib.const import COMMON_PATTERNS, TERMS

UNITS_RE = [t['pattern'] for t in TERMS if t['label'] == 'metric_length']
UNITS_RE = '(?<![A-Za-z])' + list_to_re_choice(UNITS_RE) + r'\b'

DECODER = COMMON_PATTERNS | {
    'bar': {'LOWER': {'IN': ['bar', 'bars']}},
    'mean_word': {'LOWER': 'mean'},
    './,': {'IS_PUNCT': True},
    'n': {'LOWER': 'n'},
    'measurement': {'ENT_TYPE': 'measurement'},
    'mean': {'ENT_TYPE': 'mean'},
    'sample': {'ENT_TYPE': 'sample'},
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

SIZE = MatcherPatterns(
    'size',
    on_match='size.v1',
    decoder=DECODER,
    patterns=[
        'bar ./, measurement ./,? mean? ./,? sample? ./,?',
        'measurement ./,? mean? ./,? sample? ./,?',
    ],
)


@spacy.registry.misc(SIZE.on_match)
def size(ent):
    """Enrich a size match."""
    print(ent)
    data = {}
    for ent in ent.ents:
        print(ent.label_, '|', ent)
        if ent._.cached_label in ('measurement', 'mean', 'sample'):
            print('yes')
            data |= ent._.data
            print(data)
    ent._.data = data


@spacy.registry.misc(MEASUREMENT.on_match)
def measurement(ent):
    """Enrich a measurement match."""
    matches = re.findall(FLOAT_RE, ent.text)
    ent._.data = {'low': matches[0]}
    if len(matches) > 1:
        ent._.data['high'] = matches[1]


@spacy.registry.misc(MEAN.on_match)
def mean(ent):
    """Convert the span into a single float."""
    match = re.search(FLOAT_RE, ent.text)
    value = match.group(1)

    match = re.search(UNITS_RE, ent.text)
    units = match.group(1) if match else None

    ent._.data = {'mean': to_positive_float(value)}
    if units:
        ent._.data['mean_units'] = units


@spacy.registry.misc(SAMPLE.on_match)
def sample(ent):
    """Convert the span into a single integer."""
    match = re.search(INT_RE, ent.text)
    value = match.group(1)
    ent._.data = {'n': to_positive_int(value)}
