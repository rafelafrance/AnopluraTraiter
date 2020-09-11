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
        elif label == 'group':
            data['group'] = token.lower_
    return data


def multiple_setae_count(span):
    """Handle multiple setae in one match."""
    data = {}
    low, high = 0, 0
    for token in span:
        label = token.ent_type_
        if label in ('seta_abbrev', 'seta'):
            data['setae'] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'count':
            if token._.data.get('count'):
                low += token._.data['count']
            else:
                low += token._.data['low']
                high += token._.data['high']
        elif label == 'group':
            data['group'] = token.lower_

    if high:
        data['low'] = low
        data['high'] = high
    else:
        data['count'] = low
    return data


SETAE_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'setae_count',
            'on_match': setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
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
                    {'ENT_TYPE': 'group'}
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'seta'},
                ],
            ],
        },
        {
            'label': 'setae_count',
            'on_match': multiple_setae_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'count'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'seta'},
                ],
            ],
        },
    ],
}
