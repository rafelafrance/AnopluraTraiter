"""Shared range patterns."""

import re

from traiter.pylib.util import to_positive_float

from .consts import DASH, GROUP_STEP, NUMBER, REPLACE


def measurement(span):
    """Build the range parts."""
    data = {}

    values = [t.text for t in span if re.match(NUMBER, t.text)]
    for field, value in zip(['low', 'high'], values):
        data[field] = to_positive_float(value)

    units = [t.text for t in span if t.ent_type_ == 'length_units']
    data['length_units'] = REPLACE[units[0]]

    return data


MEASUREMENT = {
    GROUP_STEP: [
        {
            'label': 'measurement',
            'on_match': measurement,
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'length_units'},
                ],
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'length_units'},
                ],
            ],
        },
    ],
}
