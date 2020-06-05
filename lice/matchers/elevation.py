"""Parse elevation notations."""

from traiter.util import to_positive_float

from ..pylib.terms import TERMS

UNITS = {t['pattern']: t['replace'] for t in TERMS if t['label'] == 'units'}


def elevation(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.lower_

        if label == 'units':
            data['units'] = UNITS[value]
        elif label == 'elevation':
            continue
        elif (as_float := to_positive_float(value)) is not None:
            data['value'] = as_float
        else:
            return {}

    return data


ELEVATION = {
    'name': 'elevation',
    'matchers': [
        {
            'label': 'elevation',
            'on_match': elevation,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'_': {'label': 'units'}},
                    {'_': {'label': 'elevation'}},
                ]
            ]
        },
    ]
}
