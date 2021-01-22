"""Extract body part count notations."""

import spacy

from ..pylib.consts import REPLACE

BODY_PART_COUNT = [
    {
        'label': 'body_part_count',
        'on_match': 'body_part_count.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': 'body_part'},
            ],
        ],
    },
]


@spacy.registry.misc(BODY_PART_COUNT[0]['on_match'])
def body_part_count(span):
    """Enrich the match."""
    data = {}

    for token in span:
        label = token.ent_type_

        if label == 'body_part':
            data['body_part'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            data = {**data, **token._.data}

    return data
