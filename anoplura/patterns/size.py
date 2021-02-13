"""Parse size notations."""

import re

import spacy
from traiter.const import FLOAT_TOKEN_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_float

from anoplura.pylib.const import EQ_, COMMON_PATTERNS


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
        '99.9 cm'
        '99.9 - 99.9 cm'
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
    patterns=['bar? ./,? measurement ./,? mean? ./,? sample? ./,?'],
)


@spacy.registry.misc(SIZE.on_match)
def size(ent):
    """Enrich a size match."""
    print(ent)
    data = {}
    for token in ent:
        if token.ent_type_ in ('measurement', 'mean', 'n'):
            data = {**token._.data, **data}
    ent._.data = data


@spacy.registry.misc(SIZE.on_match)
def measurement(ent):
    """Enrich a measurement match."""
    print(ent)

@spacy.registry.misc(MEAN.on_match)
def mean(ent):
    """Convert the span into a single float."""
    values = [t._.data for t in ent if t.ent_type_ == 'measurement']
    ent._.data = {
        'mean': values[0].get('low'),
        'mean_units': values[0].get('length_units'),
    }


@spacy.registry.misc(MEAN_NO_UNITS.on_match)
def mean_no_units(ent):
    """Convert the span into a single float."""
    values = [t.text for t in ent if re.match(FLOAT_TOKEN_RE, t.text)]
    ent._.data = {'mean': to_positive_float(values[0])}


@spacy.registry.misc(SAMPLE.on_match)
def sample(ent):
    """Convert the span into a single integer."""
    values = [t._.data for t in ent if t.ent_type_ == 'integer']
    ent._.data = dict(n=values[0].get('count', values[0].get('low')))
