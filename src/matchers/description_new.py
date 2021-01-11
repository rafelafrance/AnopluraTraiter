"""Look for trait descriptions in sentences."""

from ..pylib.consts import COLON, COMMA, DESCRIPTION_STEP, SEMICOLON, DOT


SPLITTERS = DOT + SEMICOLON + COLON + COMMA


def description(span):
    """The description is after the body part."""
    data = []
    part = [(i, t) for i, t in enumerate(span) if t.ent_type_ == 'body_part']
    if len(part) > 1:
        return data
    part = part[0]
    if part[0] > 0:
        data.append({
            '_start': 0,
            '_end': part[0],
            'description': span[:part[0]].text,
            'body_part': part[1]._.data['body_part'],
        })
    if part[0] < len(span) - 1:
        data.append({
            '_start': part[0] + 1,
            '_end': len(span),
            'description': span[part[0] + 1:].text,
            'body_part': part[1]._.data['body_part'],
        })
    return data


DESCRIPTION = {
    DESCRIPTION_STEP: [
        {
            'label': 'description',
            'on_match': description,
            'patterns': [
                [
                    {'LOWER': {'NOT_IN': SPLITTERS}, 'OP': '*'},
                    {'ENT_TYPE': 'body_part'},
                    {'LOWER': {'NOT_IN': SPLITTERS}, 'OP': '+'},
                ],
                [
                    {'LOWER': {'NOT_IN': SPLITTERS}, 'OP': '+'},
                    {'ENT_TYPE': 'body_part'},
                    {'LOWER': {'NOT_IN': SPLITTERS}, 'OP': '*'},
                ],
            ],
        },
    ],
}
