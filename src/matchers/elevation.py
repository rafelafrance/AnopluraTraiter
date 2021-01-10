"""Parse elevation notations."""

from traiter.util import to_positive_float

from ..pylib.consts import REPLACE, TRAIT_STEP

ELEV_WORDS = """ elevation elev """.split()


def elevation(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        label = token.ent_type_
        value = token.lower_

        if label == 'length_units':
            data['length_units'] = REPLACE.get(value, value)
        elif value in ELEV_WORDS:
            continue
        elif (as_float := to_positive_float(value)) is not None:
            data['elevation'] = as_float
        else:
            return {}

    return data


ELEVATION = {
    TRAIT_STEP: [
        {
            'label': 'elevation',
            'on_match': elevation,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'ENT_TYPE': 'length_units'},
                    {'LOWER': {'IN': ELEV_WORDS}},
                ]
            ]
        },
    ]
}
