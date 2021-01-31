"""Extract body part annotations."""

import spacy
from traiter.const import COMMA, DASH
from traiter.util import squash

from ..pylib.consts import MISSING, REPLACE

JOINER = ['and', 'or'] + COMMA

BODY_PART = [
    {
        'label': 'body_part',
        'on_match': 'body_part.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'part', 'OP': '+'},
            ],
            [
                {'ENT_TYPE': 'segment'},
                {'ENT_TYPE': 'part', 'OP': '+'},
            ],
            [
                {'ENT_TYPE': 'part', 'OP': '+'},
                {'ENT_TYPE': 'segment'},
            ],
            [
                {'LOWER': {'IN': MISSING}, 'OP': '?'},
                {'ENT_TYPE': 'part', 'OP': '+'},
            ],
            [
                {'ENT_TYPE': {'IN': ['ordinal']}},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'part', 'OP': '+'},
            ],
            [
                {'ENT_TYPE': 'part', 'OP': '+'},
                {'ENT_TYPE': {'IN': ['integer', 'ordinal']}, 'OP': '?'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
            ],
            [
                {'LOWER': {'IN': MISSING}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['part_loc', 'part']}, 'OP': '*'},
                {'ENT_TYPE': 'part'},
            ],
            [
                {'ENT_TYPE': 'part', 'OP': '+'},
                {'LOWER': {'IN': JOINER}, 'OP': '*'},
                {'ENT_TYPE': 'part', 'OP': '*'},
                {'LOWER': {'IN': JOINER}, 'OP': '*'},
                {'ENT_TYPE': 'part', 'OP': '+'},
            ],
        ],
    },
]


@spacy.registry.misc(BODY_PART[0]['on_match'])
def body_part(span):
    """Enrich the match."""
    data = {}

    parts = [REPLACE.get(t.lower_, t.lower_) for t in span if t.ent_type_ == 'part']
    data['body_part'] = squash(parts)

    if [t for t in span if t.lower_ in MISSING]:
        data['missing'] = True

    return data
