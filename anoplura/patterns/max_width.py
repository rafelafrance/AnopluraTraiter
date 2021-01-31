"""Get maximum width notations."""

import spacy

MAXIMUM = """ maximum max """.split()
WIDTH = """ width """.split()

MAX_WIDTH = [
    {
        'label': 'max_width',
        'on_match': 'max_width.v1',
        'patterns': [
            [
                {'LOWER': {'IN': MAXIMUM}},
                {'ENT_TYPE': 'body_part'},
                {'LOWER': {'IN': WIDTH}},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': 'size'},
            ],
        ],
    }
]


@spacy.registry.misc(MAX_WIDTH[0]['on_match'])
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
