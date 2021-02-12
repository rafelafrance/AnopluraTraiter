"""Parse size notations."""

import re

import spacy
from traiter.const import FLOAT_TOKEN_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_float

from anoplura.pylib.const import EQ_

BAR = MatcherPatterns(
    'bar',
    patterns=[[{'LOWER': {'IN': ['bar', 'bars']}}]],
)

MEAN = MatcherPatterns(
    'mean',
    on_match='mean.v1',
    patterns=[
        [
            {'LOWER': 'mean'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'ENT_TYPE': 'measurement'},
        ],
    ],
)

MEAN_NO_UNITS = MatcherPatterns(
    'mean_no_units',
    on_match='mean_no_units.v1',
    patterns=[
        [
            {'LOWER': 'mean'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'TEXT': {'REGEX': FLOAT_TOKEN_RE}},
        ],
    ],
)

SAMPLE = MatcherPatterns(
    'sample',
    on_match='sample.v1',
    patterns=[[
        {'LOWER': 'n'},
        {'TEXT': {'IN': EQ_}},
        {'ENT_TYPE': 'integer'},
    ]],
)

SIZE = MatcherPatterns(
    'size',
    on_match='size.v1',
    patterns=[
        [
            {'ENT_TYPE': 'bar', 'OP': '?'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'ENT_TYPE': 'measurement'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'ENT_TYPE': {'IN': ['mean', 'mean_no_units']}, 'OP': '?'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'ENT_TYPE': 'sample', 'OP': '?'},
            {'IS_PUNCT': True, 'OP': '?'},
        ],
    ],
)


@spacy.registry.misc(SIZE.on_match)
def size(ent):
    """Enrich a phrase match."""
    data = {}
    for token in ent:
        if token.ent_type_ in ('measurement', 'mean', 'n'):
            data = {**token._.data, **data}
    ent._.data = data


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
