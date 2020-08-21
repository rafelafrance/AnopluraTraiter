"""Get scientific names."""

from ..pylib.terms import REPLACE
from ..pylib.util import TRAIT_STEP

NAMES = {'src', 'mammalia'}


def sci_name(span):
    """Enrich the match."""
    data = {'sci_name': REPLACE[span.lower_], 'group': span[0].ent_type_}
    return data


SCI_NAME = {
    'name': 'sci_name',
    TRAIT_STEP: [
        {
            'label': 'sci_name',
            'on_match': sci_name,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': list(NAMES)}},
                ],
            ],
        },
    ],
}
