"""Get total length notations."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import REPLACE

BODY_PART_ENTITIES = """ body_part setae seta_abbrev """.split()
LENGTH_WORDS = """ length len """.split()

LENGTH = MatcherPatterns(
    'length',
    on_match='length.v1',
    patterns=[[
        {'LOWER': 'total', 'OP': '?'},
        {'ENT_TYPE': {'IN': BODY_PART_ENTITIES}},
        {'LOWER': {'IN': LENGTH_WORDS}},
        {'ENT_TYPE': '', 'OP': '?'},
        {'ENT_TYPE': '', 'OP': '?'},
        {'ENT_TYPE': 'size'},
    ]],
)


@spacy.registry.misc(LENGTH.on_match)
def length(ent):
    """Enrich the match."""
    field = [t for t in ent if t.ent_type_ == 'size']
    data = field[0]._.data

    field = [t for t in ent if t.ent_type_ in BODY_PART_ENTITIES]
    data['body_part'] = REPLACE.get(field[0].lower_, field[0].lower_)

    data['trait'] = 'length'
    if any(t.lower_ == 'total' for t in ent):
        data['_label'] = 'total_length'

    ent._.data = data
