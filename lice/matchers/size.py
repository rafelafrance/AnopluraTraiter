"""Parse size notations."""

from traiter.util import to_positive_float

from ..pylib.terms import REPLACE


def size(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.lower_
        as_float = None

        if (token.like_num and not label
                and (as_float := to_positive_float(value)) is not None):
            data['low'] = as_float

        elif (label == 'high'
                and (as_float := to_positive_float(value)) is not None):
            data['high'] = as_float

        elif label == 'mm':
            data['units'] = REPLACE[value]

        else:
            return {}

    return data


SIZE = {
    'name': 'size',
    'groupers': {
        'high': [[
            {'_': {'label': 'dash'}},
            {'LIKE_NUM': True},
        ]],
        'not_size': [[
            {'_': {'label': 'bar'}},
            {'_': {'label': 'comma'}, 'OP': '?'},
        ]],
        'mean': [[
            {'_': {'label': 'comma'}, 'OP': '?'},
            {'_': {'label': 'mean'}},
            {'LIKE_NUM': True},
            {'_': {'label': 'mm'}},
        ]],
        'n': [[
            {'_': {'label': 'open'}, 'OP': '?'},
            {'_': {'label': 'n'}},
            {'_': {'label': 'eq'}},
            {'LIKE_NUM': True},
            {'_': {'label': 'close'}, 'OP': '?'},
        ]],
    },
    'matchers': [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'_': {'label': 'not_size'}, 'OP': '?'},
                    {'LIKE_NUM': True},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'mm'}},
                ],
            ],
        },
    ],
}
