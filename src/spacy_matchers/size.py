"""Parse size notations."""

import re

from traiter.pylib.util import to_positive_float, to_positive_int

from .consts import EQ, GROUP_STEP, INT, NUMBER, TRAIT_STEP


def size(span):
    """Enrich a phrase match."""
    data = {}

    for token in span:
        if token.ent_type_ in ('measurement', 'mean', 'n'):
            data = {**token._.data, **data}
    return data


def sample(span):
    """Convert the span into a single integer."""
    if values := [t.text for t in span if re.match(INT, t.text)]:
        if (value := to_positive_int(values[0])) is not None:
            return dict(n=value)
    return {}


def mean(span):
    """Convert the span into a single float."""
    if values := [t.text for t in span if re.match(NUMBER, t.text)]:
        if (value := to_positive_float(values[0])) is not None:
            data = dict(mean=value)
            if units := [t.text for t in span
                         if t.ent_type_ == 'length_units']:
                data['mean_units'] = units[0]
            return data
    return {}


BAR = ['bar', 'bars']

SIZE = {
    GROUP_STEP: [
        {
            'label': 'bar',
            'patterns': [[
                {'LOWER': {'IN': BAR}},
            ]],
        },
        {
            'label': 'mean',
            'on_match': mean,
            'patterns': [[
                {'LOWER': 'mean'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'TEXT': {'REGEX': NUMBER}},
                {'ENT_TYPE': 'length_units'},
            ]],
        },
        {
            'label': 'n',
            'on_match': sample,
            'patterns': [[
                {'LOWER': 'n'},
                {'TEXT': {'IN': EQ}},
                {'TEXT': {'REGEX': INT}},
            ]],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'size',
            'on_match': size,
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
    ],
}
