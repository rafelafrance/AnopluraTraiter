"""Parse count notations."""

import spacy
from traiter.consts import INT_TOKEN_RE
from traiter.util import to_positive_int

from ..pylib.consts import REPLACE

SEX_COUNT = [
    {
        'label': 'sex_count',
        'on_match': 'sex_count.v1',
        'patterns': [
            [
                {'TEXT': {'REGEX': INT_TOKEN_RE}},
                {'ENT_TYPE': 'sex'},
            ]
        ]
    },
]


@spacy.registry.misc(SEX_COUNT[0]['on_match'])
def sex_count(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        label = token.ent_type_
        value = token.lower_

        if label == 'sex':
            data['sex'] = REPLACE[value]
        elif (as_int := to_positive_int(value)) is not None:
            data['count'] = as_int
        else:
            return {}

    return data
