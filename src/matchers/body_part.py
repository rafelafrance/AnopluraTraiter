"""Extract body part annotations."""

from traiter.actions import text_action
from traiter.util import squash

from ..pylib.consts import COMMA, DASH, GROUP_STEP, MISSING, REPLACE


def body_part(span):
    """Enrich the match."""
    data = text_action(span, REPLACE)
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
    # SEGMENT_STEP: [
    #     {
    #         'label': 'segment',
    #         'patterns': [
    #             [
    #                 {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
    #                 {'TEXT': {'IN': DASH}, 'OP': '?'},
    #                 {'ENT_TYPE': 'segmented'},
    #             ],
    #             [
    #                 {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
    #                 {'TEXT': {'IN': DASH}, 'OP': '?'},
    #                 {'ENT_TYPE': 'segmented'},
    #             ],
    #         ],
    #     },
    # ],
    GROUP_STEP: [
        {
            'label': 'body_part',
            'on_match': body_part,
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
                    {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
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
