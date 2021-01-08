"""Extract body part count notations."""

from ..pylib.consts import ATTACH_STEP, REPLACE


def body_part_count(span):
    """Enrich the match."""
    data = {}

    for token in span:
        label = token.ent_type_

        if label == 'body_part':
            data['body_part'] = REPLACE.get(token.lower_, token.lower_)

        elif label == 'integer':
            data = {**data, **token._.data}

    return data


BODY_PART_COUNT = {
    ATTACH_STEP: [
        {
            'label': 'body_part_count',
            'on_match': body_part_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'integer'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'body_part'},
                ],
            ],
        },
    ],
}
