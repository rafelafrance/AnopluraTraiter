"""Extract sclerotized annotations."""

from traiter.pylib.util import squash

from .shared import COMMA
from ..pylib.util import TRAIT_STEP, GROUP_STEP


def anatomy(span):
    """Enrich the match."""
    return {'anatomy': span.lower_}


def body_part(span):
    """Enrich the match."""
    parts = []
    for token in span:
        if token.ent_type_ == 'anatomy':
            parts.append(token.lower_)
    return {'part': squash(parts)}


_JOINER = ['and', 'or'] + COMMA

BODY_PART = {
    GROUP_STEP: [
        {
            'label': 'anatomy',
            'on_match': anatomy,
            'patterns': [
                [
                    {'ENT_TYPE': 'part', 'OP': '+'},
                ],
            ],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'body_part',
            'on_match': body_part,
            'patterns': [
                [
                    {'ENT_TYPE': 'anatomy'},
                ],
                [
                    {'ENT_TYPE': 'anatomy'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'anatomy'},
                ],
                [
                    {'ENT_TYPE': 'anatomy'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'anatomy'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'anatomy'},
                ],
            ],
        },
    ],
}
