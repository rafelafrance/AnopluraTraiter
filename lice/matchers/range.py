"""Shared range patterns."""

import re

from traiter.util import to_positive_float  # pylint: disable=import-error

from .shared import DASH, MM, NUMBER


def range_(span):
    """Build the range parts."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        units='mm',
    )

    values = [t.text for t in span if re.match(NUMBER, t.text)]
    fields = ['low', 'high']

    for field, value in zip(fields, values):
        data[field] = to_positive_float(value)

    return data


RANGE = {
    'name': 'range',
    'groupers': [
        {
            'label': 'range',
            'on_match': range_,
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': {'IN': MM}},
                ],
                [{'TEXT': {'IN': DASH}}, {'LOWER': {'IN': MM}}],
            ],
        },
    ],
}
