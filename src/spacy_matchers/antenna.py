"""Extract antenna notations."""

import re

from .consts import BREAK, DASH, TRAIT_STEP


def antenna(span):
    """Enrich the match."""
    parts = [t.lower_ for t in span
             if t.ent_type_ != 'antenna' and t.text not in BREAK]
    desc = ' '.join(parts)
    desc = re.sub(r'\s-\s', '-', desc)
    desc = re.sub(r'\s([,;])', r'\1', desc)
    return {'description': desc}


def antenna_all(span):
    """Enrich the match."""
    return {'description': span[:-1].lower_}


ANTENNA = {
    TRAIT_STEP: [
        {
            'label': 'antenna',
            'on_match': antenna,
            'patterns': [
                [
                    {'ENT_TYPE': 'antenna'},
                    {'TEXT': {'NOT_IN': BREAK}, 'OP': '*'},
                    {'TEXT': {'IN': BREAK}},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'segment'},
                    {'ENT_TYPE': 'antenna'},
                    {'TEXT': {'NOT_IN': BREAK}, 'OP': '*'},
                    {'TEXT': {'IN': BREAK}},
                ],
            ],
        },
        {
            'label': 'antenna',
            'on_match': antenna_all,
            'patterns': [
                [
                    {'ENT_TYPE': 'ordinal'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'antenna_segment'},
                    {'TEXT': {'NOT_IN': BREAK}, 'OP': '*'},
                    {'TEXT': {'IN': BREAK}},
                ],
                [
                    {'ENT_TYPE': 'antenna_segment'},
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'NOT_IN': BREAK}, 'OP': '*'},
                    {'TEXT': {'IN': BREAK}},
                ],
            ],
        },
    ],
}
