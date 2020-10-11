"""Extract antenna notations."""

from ..pylib.util import DASH, TRAIT_STEP, REPLACE


def antenna(span):
    """Enrich the match."""
    part = REPLACE.get(span.lower_, span.lower_)
    return {'body_part': part}


ANTENNA = {
    TRAIT_STEP: [
        {
            'label': 'body_part',
            'on_match': antenna,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': ['antenna', 'antennal_segment']}},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'segment'},
                    {'ENT_TYPE': 'antenna'},
                ],
                [
                    {'ENT_TYPE': 'ordinal'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'antennal_segment'},
                ],
                [
                    {'ENT_TYPE': 'antennal_segment'},
                    {'ENT_TYPE': 'count'},
                ],
            ],
        },
    ],
}
