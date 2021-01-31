"""Get scientific names."""

import spacy

from ..pylib.consts import REPLACE

NAMES = ['anoplura', 'mammalia']

SCI_NAME = [
    {
        'label': 'sci_name',
        'on_match': 'sci_name.v1',
        'patterns': [
            [
                {'ENT_TYPE': {'IN': NAMES}},
            ],
        ],
    },
    {
        'label': 'genus',
        'on_match': 'genus.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'anoplura_genus'},
            ],
        ],
    },
]


@spacy.registry.misc(SCI_NAME[0]['on_match'])
def sci_name(span):
    """Enrich the match."""
    data = {
        'sci_name': REPLACE.get(span.lower_, span.text.capitalize()),
        'group': span[0].ent_type_,
    }
    return data


@spacy.registry.misc(SCI_NAME[1]['on_match'])
def genus(span):
    """Enrich the match."""
    data = {
        'genus': REPLACE.get(span.lower_, span.text.capitalize()),
        'group': span[0].ent_type_.split('_')[0],
    }
    return data
