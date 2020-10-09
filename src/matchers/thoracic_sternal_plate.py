"""Parse thoracic sternal plate notations."""

from ..pylib.util import BREAK, TRAIT_STEP


def thoracic_sternal_plate(span):
    """Enrich the match."""
    return {'description': span[1:-1].text}


THORACIC_STERNAL_PLATE = {
    TRAIT_STEP: [
        {
            'label': 'thoracic_sternal_plate',
            'on_match': thoracic_sternal_plate,
            'patterns': [
                [
                    {'ENT_TYPE': 'sternal_plate'},
                    {'TEXT': {'NOT_IN': BREAK}, 'OP': '*'},
                    {'TEXT': {'IN': BREAK}},
                ],
            ],
        },
    ],
}
