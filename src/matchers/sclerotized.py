"""Extract sclerotized annotations."""

from ..pylib.util import ATTACH_STEP, TRAIT_STEP


def sclerotized(span):
    """Enrich the match."""
    data = {}
    for token in span:
        if token.ent_type_ == 'sclerotin':
            pass
        else:
            data['sclerotized'] = token.lower_
    return data


def sclerotized_part(span):
    """Enrich the match."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label in ('body_part', 'sclerotized'):
            data = {**data, **token._.data}
        elif label == 'location':
            data['location'] = token.lower_
    return data


SCLEROTIZED = {
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
    ATTACH_STEP: [
        {
            'label': 'sclerotized_part',
            'on_match': sclerotized_part,
            'patterns': [
                [
                    {'ENT_TYPE': 'body_part'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'location', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'sclerotized'},
                ],
                [
                    {'ENT_TYPE': 'sclerotized'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'location', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '*'},
                    {'ENT_TYPE': 'body_part'},
                ],
            ],
        },
    ],
}
