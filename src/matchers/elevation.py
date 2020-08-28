"""Parse elevation notations."""

from traiter.pylib.util import to_positive_float

from ..pylib.terms import TERMS
from ..pylib.util import TRAIT_STEP

UNITS = {t['pattern']: t['replace'] for t in TERMS if t['label'] == 'units'}

ELEV_LIST = """ elevation elev """.split()
ELEV_SET = set(ELEV_LIST)


def elevation(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        label = token.ent_type_
        value = token.lower_

        if label == 'units':
            data['units'] = UNITS[value]
        elif value in ELEV_SET:
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
                    {'ENT_TYPE': 'units'},
                    {'LOWER': {'IN': ELEV_LIST}},
                ]
            ]
        },
    ]
}
