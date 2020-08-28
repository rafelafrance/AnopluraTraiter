"""Extract setae count notations."""

from .shared import CLOSE, OPEN
from ..pylib.util import REPLACE, TRAIT_STEP


def setae_count(span):
    """Enrich the match."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label == 'seta_abbrev':
            data['setae'] = REPLACE[token.lower_]
        elif label == 'word_count':
            data = {**data, **token._.data}
    return data


SETAE_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'setae_count',
            'on_match': setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'word_count'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'seta_leader'},
                    {'ENT_TYPE': 'seta'},
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'seta_abbrev'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
            ],
        },
    ],
}
