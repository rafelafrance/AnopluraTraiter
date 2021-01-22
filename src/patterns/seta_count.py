"""Extract setae count notations."""

import spacy
from traiter.consts import CLOSE, OPEN

from ..pylib.consts import REPLACE

SETAE = [
    {
        'label': 'setae',
        'patterns': [
            [
                {'ENT_TYPE': 'body_part', 'OP': '*'},
                {'ENT_TYPE': 'seta'},
            ],
            [
                {'ENT_TYPE': 'part_loc', 'OP': '+'},
                {'ENT_TYPE': 'seta'},
            ],
        ],
    },
]

SETA_COUNT = [
    {
        'label': 'seta_count',
        'on_match': 'seta_count.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': 'setae'},
                {'TEXT': {'IN': OPEN}, 'OP': '?'},
                {'ENT_TYPE': 'seta_abbrev'},
                {'TEXT': {'IN': CLOSE}, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': 'setae'},
                {'POS': {'IN': ['ADP', 'ADJ']}, 'OP': '?'},
                {'ENT_TYPE': 'group'}
            ],
            [
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': 'setae'},
            ],
        ],
    },
    {
        'label': 'seta_count',
        'on_match': 'multiple_seta_count.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                {'ENT_TYPE': 'integer'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': '', 'OP': '?'},
                {'ENT_TYPE': {'IN': ['part_loc']}, 'OP': '*'},
                {'ENT_TYPE': {'IN': ['part_loc', 'body_part']}, 'OP': '?'},
                {'ENT_TYPE': 'setae'},
            ],
        ],
    },
]


@spacy.registry.misc(SETA_COUNT[0]['on_match'])
def seta_count(span):
    """Enrich the match."""
    data = {'body_part': 'seta'}
    location = []

    for token in span:
        label = token.ent_type_

        if label == 'setae':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            data = {**data, **token._.data}

        elif label == 'group':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    if data.get('count', data.get('low')) is None:
        data['present'] = True

    if location:
        data['type'] = ' '.join(location)

    return data


@spacy.registry.misc(SETA_COUNT[1]['on_match'])
def multiple_seta_count(span):
    """Handle multiple setae in one match."""
    data = {'body_part': 'seta'}
    low, high = 0, 0

    for token in span:
        label = token.ent_type_

        if label == 'setae':
            data['seta'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            if token._.data.get('count'):
                low += token._.data['count']
            else:
                low += token._.data.get('low', 0)
                high += token._.data.get('high', 0)

        elif label == 'group':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    if high and low:
        data['low'] = low
        data['high'] = high
    else:
        data['count'] = low

    return data
