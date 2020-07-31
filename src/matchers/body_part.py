"""Extract sclerotized annotations."""

from .shared import COMMA
from traiter.pylib.util import squash  # pylint: disable=import-error


def body_part(span):
    """Enrich the match."""
    parts = []
    for token in span:
        if token.ent_type_ == 'part':
            parts.append(token.lower_)
    return {'part': squash(parts)}


_JOINER = ['and', 'or'] + COMMA


BODY_PART = {
    'name': 'body_part',
    'traits': [
        {
            'label': 'body_part',
            'on_match': body_part,
            'patterns': [
                [
                    {'ENT_TYPE': 'part'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part'},
                    {'LOWER': {'IN': _JOINER}, 'OP': '*'},
                    {'ENT_TYPE': 'part'},
                ],
            ],
        },
    ],
}
