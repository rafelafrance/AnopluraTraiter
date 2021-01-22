"""Parse size notations."""

import re

import spacy
from traiter.util import to_positive_float

from ..pylib.consts import EQ_, FLOAT_RE

BAR = ['bar', 'bars']

SIZE_PARTS = [
    {
        'label': 'bar',
        'patterns': [[
            {'LOWER': {'IN': BAR}},
        ]],
    },
    {
        'label': 'mean',
        'on_match': 'mean.v1',
        'patterns': [
            [
                {'LOWER': 'mean'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'ENT_TYPE': 'measurement'},
            ],
        ],
    },
    {
        'label': 'mean',
        'on_match': 'mean_no_units.v1',
        'patterns': [
            [
                {'LOWER': 'mean'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'TEXT': {'REGEX': FLOAT_RE}},
            ],
        ],
    },
    {
        'label': 'n',
        'on_match': 'sample.v1',
        'patterns': [[
            {'LOWER': 'n'},
            {'TEXT': {'IN': EQ_}},
            {'ENT_TYPE': 'integer'},
        ]],
    },
]

SIZE = [
    {
        'label': 'size',
        'on_match': 'size.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'bar', 'OP': '?'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'ENT_TYPE': 'measurement'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'ENT_TYPE': 'mean', 'OP': '?'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'ENT_TYPE': 'n', 'OP': '?'},
                {'IS_PUNCT': True, 'OP': '?'},
            ],
        ],
    },
]


@spacy.registry.misc(SIZE[0]['on_match'])
def size(span):
    """Enrich a phrase match."""
    data = {}

    for token in span:
        if token.ent_type_ in ('measurement', 'mean', 'n'):
            data = {**token._.data, **data}
    return data


@spacy.registry.misc(SIZE_PARTS[1]['on_match'])
def mean(span):
    """Convert the span into a single float."""
    values = [t._.data for t in span if t.ent_type_ == 'measurement']
    return {
        'mean': values[0].get('low'),
        'mean_units': values[0].get('length_units'),
    }


@spacy.registry.misc(SIZE_PARTS[2]['on_match'])
def mean_no_units(span):
    """Convert the span into a single float."""
    values = [t.text for t in span if re.match(FLOAT_RE, t.text)]
    return {'mean': to_positive_float(values[0])}


@spacy.registry.misc(SIZE_PARTS[3]['on_match'])
def sample(span):
    """Convert the span into a single integer."""
    values = [t._.data for t in span if t.ent_type_ == 'integer']
    return dict(n=values[0].get('count', values[0].get('low')))
