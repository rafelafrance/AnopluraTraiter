"""Look for trait descriptions in sentences."""

from ..pylib.consts import DESCRIPTION_STEP, SEMICOLON, DOT


SPLITTERS = DOT + SEMICOLON


def description(span):
    """Enrich the match."""
    data = {}
    print(span)
    # return data
    return {'_forget': True}


DESCRIPTION = {
    DESCRIPTION_STEP: [
        {
            'label': 'description',
            'on_match': description,
            'patterns': [
                [
                    {'ENT_TYPE': 'body_part'},
                    {'TEXT': {'NOT_IN': SPLITTERS}, 'OP': '+'},
                ],
            ],
        },
    ],
}
