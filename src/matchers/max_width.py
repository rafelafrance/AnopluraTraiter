"""Get maximum width notations."""


def max_width(span):
    """Enrich the match."""
    data = {}

    for token in span:
        label = token.ent_type_

        if label == 'body_part':
            data['part'] = token.text

        elif label == 'size':
            data = {**data, **token._.data}

    return data


MAXIMUM = """ maximum max """.split()

MAX_WIDTH = {
    'name': 'max_width',
    'attachers': [
        {
            'label': 'max_width',
            'on_match': max_width,
            'patterns': [
                [
                    {'LOWER': {'IN': MAXIMUM}},
                    {'ENT_TYPE': 'body_part'},
                    {'LOWER': 'width'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'size'},
                ],
            ],
        }
    ]
}
