"""Parse numbers."""

import re

import spacy
from traiter.consts import DASH, FLOAT_RE, INT_RE
from traiter.util import to_positive_float

from ..pylib.consts import REPLACE

TO_INT = {'no': 0, 'pair': 2}

OTHER_WORDS = """ no pair """.split()
TO = ['to'] + DASH

LABELS = 'count low high'.split()

NUMERIC = [
    {
        'label': 'integer',
        'on_match': 'integer.v1',
        'patterns': [
            [
                {'TEXT': {'REGEX': INT_RE}},
            ],
            [
                {'TEXT': {'REGEX': INT_RE}},
                {'LOWER': {'IN': TO}},
                {'TEXT': {'REGEX': INT_RE}},
            ],
            [
                {'LOWER': {'IN': OTHER_WORDS}},
            ],
            [
                {'ENT_TYPE': 'number_word'},
            ],
        ],
    },
    {
        'label': 'measurement',
        'on_match': 'measurement.v1',
        'patterns': [
            [
                {'TEXT': {'REGEX': FLOAT_RE}},
                {'TEXT': {'IN': DASH}},
                {'TEXT': {'REGEX': FLOAT_RE}},
                {'ENT_TYPE': 'metric_length'},
            ],
            [
                {'TEXT': {'REGEX': FLOAT_RE}},
                {'ENT_TYPE': 'metric_length'},
            ],
        ],
    },
]


@spacy.registry.misc(NUMERIC[0]['on_match'])
def integer(span):
    """Convert a word range like 'five to six' into a numeric range."""
    words = [t.lower_ for t in span if t.lower_ not in TO]
    keys = LABELS[:1] if len(words) == 1 else LABELS[1:]
    try:
        data = {k: int(REPLACE.get(w, TO_INT.get(w, w))) for k, w in zip(keys, words)}
    except ValueError:
        return
    return data


@spacy.registry.misc(NUMERIC[1]['on_match'])
def measurement(span):
    """Build the range parts."""
    data = {}

    values = [t.text for t in span if re.match(FLOAT_RE, t.text)]
    for field, value in zip(['low', 'high'], values):
        data[field] = to_positive_float(value)

    units = [t.text for t in span if t.ent_type_ == 'metric_length']
    data['length_units'] = REPLACE[units[0]]

    return data
