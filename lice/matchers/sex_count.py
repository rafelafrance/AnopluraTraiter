"""Parse count notations."""

from traiter.util import to_positive_int

from ..pylib.terms import REPLACE


def sex_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.lower_

        if label == 'sex':
            data['sex'] = REPLACE[value]
        elif (as_int := to_positive_int(value)) is not None:
            data['count'] = as_int
        else:
            return {}

    return data


SEX_COUNT = {
    'name': 'sex_count',
    'matchers': [
        {
            'label': 'sex_count',
            'on_match': sex_count,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'_': {'label': 'sex'}},
                ]
            ]
        },
    ]
}
