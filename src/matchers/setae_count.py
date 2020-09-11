"""Extract setae count notations."""

from .shared import CLOSE, OPEN
from ..pylib.util import REPLACE, TRAIT_STEP


def setae_count(span):
    """Enrich the match."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label in ('seta_abbrev', 'seta'):
            data['setae'] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'count':
            data = {**data, **token._.data}
        elif label == 'location':
            data['location'] = token.lower_
    return data


SETAE_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'setae_count',
            'on_match': setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'seta_leader'},
                    {'ENT_TYPE': 'seta'},
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'seta_abbrev'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'seta'},
                    {'POS': {'IN': ['ADP', 'ADJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'location'}
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'seta'},
                ],
            ],
        },
    ],
}
