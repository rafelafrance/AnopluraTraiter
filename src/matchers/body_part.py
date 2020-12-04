"""Extract body part annotations."""

from traiter.pylib.util import squash

from ..pylib.actions import text_action
from ..pylib.util import COMMA, DASH, GROUP_STEP, MISSING


def body_part(span):
    """Enrich the match."""
    data = text_action(span)
    if [t for t in span if t.lower_ in MISSING]:
        data['missing'] = True
    return data


def multiple_parts(span):
    """Enrich the match."""
    parts = []
    for token in span:
        if token.ent_type_ == 'part':
            parts.append(token.lower_)
    return {'body_part': squash(parts)}


JOINER = ['and', 'or'] + COMMA

BODY_PART = {
    GROUP_STEP: [
        {
            'label': 'body_part',
            'on_match': body_part,
            'patterns': [
                [
                    {'LOWER': {'IN': MISSING}, 'OP': '?'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'ENT_TYPE': 'segment'},
                    {'ENT_TYPE': 'integer'},
                ],
                [
                    {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'segment'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
                [
                    {'ENT_TYPE': 'ordinal'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'ENT_TYPE': 'segment'},
                ],
                [
                    {'ENT_TYPE': 'segment'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'ENT_TYPE': 'integer'},
                ],
                [
                    {'LOWER': {'IN': MISSING}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': ['part_loc', 'part']}, 'OP': '*'},
                    {'ENT_TYPE': 'part'},
                ],
            ],
        },
        {
            'label': 'body_part',
            'on_match': multiple_parts,
            'patterns': [
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'LOWER': {'IN': JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part', 'OP': '*'},
                    {'LOWER': {'IN': JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
            ],
        },
    ],
}
