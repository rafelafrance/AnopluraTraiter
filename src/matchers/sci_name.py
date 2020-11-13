"""Get scientific names."""

from ..pylib.util import REPLACE, TRAIT_STEP

NAMES = ['anoplura', 'mammalia']


def sci_name(span):
    """Enrich the match."""
    data = {
        'sci_name': REPLACE.get(span.lower_, span.text.capitalize()),
        'group': span[0].ent_type_}
    return data


def genus(span):
    """Enrich the match."""
    data = {
        'genus': REPLACE.get(span.lower_, span.text.capitalize()),
        'group': span[0].ent_type_.split('_')[0],
    }
    return data


SCI_NAME = {
    TRAIT_STEP: [
        {
            'label': 'sci_name',
            'on_match': sci_name,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': NAMES}},
                ],
            ],
        },
        {
            'label': 'genus',
            'on_match': genus,
            'patterns': [
                [
                    {'ENT_TYPE': 'anoplura_genus'},
                ],
            ],
        },
    ],
}
