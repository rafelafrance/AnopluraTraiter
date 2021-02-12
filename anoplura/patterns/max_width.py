"""Get maximum width notations."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns

MAXIMUM = """ maximum max """.split()
WIDTH = """ width """.split()

MAX_WIDTH = MatcherPatterns(
    'max_width',
    on_match='max_width.v1',
    patterns=[
        [
            {'LOWER': {'IN': MAXIMUM}},
            {'ENT_TYPE': 'body_part'},
            {'LOWER': {'IN': WIDTH}},
            {'ENT_TYPE': '', 'OP': '?'},
            {'ENT_TYPE': '', 'OP': '?'},
            {'ENT_TYPE': 'size'},
        ],
    ],
)


@spacy.registry.misc(MAX_WIDTH.on_match)
def max_width(ent):
    """Enrich the match."""
    data = {}

    for token in ent:
        label = token.ent_type_

        if label == 'body_part':
            data['part'] = token.text

        elif label == 'size':
            data = {**data, **token._.data}

    ent._.data = data
