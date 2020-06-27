"""Get body length notations."""


def body_length(span):
    """Enrich the match."""
    data = {}

    for token in span:
        label = token._.label

        if label == 'size':
            data = {**data, **token._.data}

    return data


LENGTH = """ length len """.split()


BODY_LENGTH = {
    'name': 'body_length',
    'attachers': [
        {
            'label': 'body_length',
            'on_match': body_length,
            'patterns': [
                [
                    {'LOWER': 'total', 'OP': '?'},
                    {'LOWER': 'body'},
                    {'LOWER': {'IN': LENGTH}},
                    {'_': {'label': ''}, 'OP': '?'},
                    {'_': {'label': ''}, 'OP': '?'},
                    {'_': {'label': 'size'}},
                ],
            ],
        }
    ]
}
