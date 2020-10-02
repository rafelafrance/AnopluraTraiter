"""Parse count notations."""

from traiter.pylib.util import to_positive_int

from ..pylib.util import INT, REPLACE, TRAIT_STEP


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


SEX_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'sex_count',
            'on_match': sex_count,
            'patterns': [
                [
                    {'TEXT': {'REGEX': INT}},
                    {'ENT_TYPE': 'sex'},
                ]
            ]
        },
    ]
}
