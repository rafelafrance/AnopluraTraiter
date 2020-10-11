"""Extract sclerotized annotations."""

from traiter.pylib.util import squash

from ..pylib.util import COMMA, TRAIT_STEP


def body_part(span):
    """Enrich the match."""
    parts = []
    for token in span:
        if token.ent_type_ == 'part':
            parts.append(token.lower_)
    return {'body_part': squash(parts)}


_JOINER = ['and', 'or'] + COMMA

BODY_PART = {
    TRAIT_STEP: [
        {
            'label': 'body_part',
            'on_match': body_part,
            'patterns': [
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
            ],
        },
    ],
}
