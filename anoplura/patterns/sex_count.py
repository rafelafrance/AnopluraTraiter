"""Parse count notations."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_int

SEX_COUNT = MatcherPatterns(
    'sex_count',
    on_match='sex_count.v1',
    patterns=[
        [
            {'IS_DIGIT': True},
            {'ENT_TYPE': 'sex'},
        ]
    ]
)


@spacy.registry.misc(SEX_COUNT.on_match)
def sex_count(ent):
    """Enrich the match with data."""
    data = {}

    for token in ent:
        label = token.ent_type_
        value = token.lower_

        if label == 'sex':
            data['sex'] = value
        elif (as_int := to_positive_int(value)) is not None:
            data['count'] = as_int

    ent._.data = data
