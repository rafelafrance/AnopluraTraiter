"""Extract sclerotized annotations."""

from ..pylib.util import TRAIT_STEP


def sclerotized(span):
    """Enrich the match."""
    data = {}
    for token in span:
        if token.ent_type_ == 'sclerotin':
            pass
        else:
            data['sclerotized'] = token.lower_
    return data


SCLEROTIZED = {
    'name': 'sclerotized',
    TRAIT_STEP: [
        {
            'label': 'sclerotized',
            'on_match': sclerotized,
            'patterns': [
                [
                    {'POS': 'ADV'},
                    {'ENT_TYPE': 'sclerotin'},
                ],
            ],
        },
    ],
}
