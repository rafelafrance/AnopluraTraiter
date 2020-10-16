"""Parse numbers."""

import re

from traiter.pylib.util import to_positive_float

from ..pylib.util import DASH, NUMERIC_STEP, NUMBER_RE, REPLACE

TO_INT = {
    'no': 0,
    'pair': 2,

    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
}

OTHER_WORDS = """ no pair """.split()
TO = ['to'] + DASH

LABELS = 'count low high'.split()


def integer(span):
    """Convert a word range like 'five to six' into a numeric range."""
    words = [t.lower_ for t in span if t.lower_ not in TO]
    keys = LABELS[:1] if len(words) == 1 else LABELS[1:]
    try:
        data = {k: int(TO_INT.get(w, w)) for k, w in zip(keys, words)}
    except ValueError:
        return {'_forget': True}
    return data


def measurement(span):
    """Build the range parts."""
    data = {}

    values = [t.text for t in span if re.match(NUMBER_RE, t.text)]
    for field, value in zip(['low', 'high'], values):
        data[field] = to_positive_float(value)

    units = [t.text for t in span if t.ent_type_ == 'length_units']
    data['length_units'] = REPLACE[units[0]]

    return data


NUMERIC = {
    NUMERIC_STEP: [
        {
            'label': 'integer',
            'on_match': integer,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                ],
                [
                    {'LIKE_NUM': True},
                    {'LOWER': {'IN': TO}},
                    {'LIKE_NUM': True},
                ],
                [
                    {'LOWER': {'IN': OTHER_WORDS}},
                ],
            ],
        },
        {
            'label': 'measurement',
            'on_match': measurement,
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER_RE}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER_RE}},
                    {'ENT_TYPE': 'length_units'},
                ],
                [
                    {'TEXT': {'REGEX': NUMBER_RE}},
                    {'ENT_TYPE': 'length_units'},
                ],
            ],
        },

    ],
}
