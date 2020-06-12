"""Parse size notations."""

from .shared import CLOSE, COMMA, EQ, INT, NUMBER, OPEN, float_group, int_group


def length(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char)

    for token in span:
        label = token._.label
        datum = token._.data
        if label == 'range':
            data = {**datum, **data}
        elif label in ('mean', 'n'):
            data[label] = datum['value']
        else:
            return {}

    return data


BAR = ['bar', 'bars']

LENGTH = {
    'name': 'length',
    'groupers': [
        {
            'label': 'bar',
            'patterns': [[
                {'LOWER': {'IN': BAR}},
                {'TEXT': {'IN': COMMA}, 'OP': '?'},
            ]],
        },
        {
            'label': 'mean',
            'on_match': float_group,
            'patterns': [[
                {'TEXT': {'IN': COMMA}, 'OP': '?'},
                {'LOWER': 'mean'},
                {'TEXT': {'REGEX': NUMBER}},
                {'_': {'label': 'mm'}},
            ]],
        },
        {
            'label': 'n',
            'on_match': int_group,
            'patterns': [[
                {'TEXT': {'IN': OPEN}, 'OP': '?'},
                {'LOWER': 'n'},
                {'TEXT': {'IN': EQ}},
                {'TEXT': {'REGEX': INT}},
                {'TEXT': {'IN': CLOSE}, 'OP': '?'},
            ]],
        },
    ],
    'matchers': [
        {
            'label': 'length',
            'on_match': length,
            'patterns': [
                [
                    {'_': {'label': 'bar'}, 'OP': '?'},
                    {'_': {'label': 'range'}},
                    {'_': {'label': 'mean'}, 'OP': '?'},
                    {'_': {'label': 'n'}, 'OP': '?'},
                ],
            ],
        },
    ],
}
