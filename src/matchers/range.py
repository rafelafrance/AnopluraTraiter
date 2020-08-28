"""Shared range patterns."""

import re

# pylint: disable=import-error
from traiter.pylib.util import to_positive_float

from .shared import DASH, NUMBER
from ..pylib.util import GROUP_STEP, REPLACE


def range_(span):
    """Build the range parts."""
    data = {}

    values = [t.text for t in span if re.match(NUMBER, t.text)]
    for field, value in zip(['low', 'high'], values):
        data[field] = to_positive_float(value)

    units = [t.text for t in span if t.ent_type_ == 'units']
    data['units'] = REPLACE[units[0]]

    return data


RANGE = {
    GROUP_STEP: [
        {
            'label': 'range',
            'on_match': range_,
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'units'},
                ],
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'units'},
                ],
            ],
        },
    ],
}
