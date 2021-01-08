"""Get total length notations."""

from ..pylib.consts import ATTACH_STEP, REPLACE


BODY_PART_ENTITIES = """ body_part setae seta_abbrev """.split()


def length(span):
    """Enrich the match."""
    field = [t for t in span if t.ent_type_ == 'size']
    data = field[0]._.data

    field = [t for t in span if t.ent_type_ in BODY_PART_ENTITIES]
    data['body_part'] = REPLACE.get(field[0].lower_, field[0].lower_)

    data['trait'] = 'length'
    if any(t.lower_ == 'total' for t in span):
        data['_label'] = 'total_length'

    return data


LENGTH_WORDS = """ length len """.split()

LENGTH = {
    ATTACH_STEP: [
        {
            'label': 'length',
            'on_match': length,
            'patterns': [
                [
                    {'LOWER': 'total', 'OP': '?'},
                    {'ENT_TYPE': {'IN': BODY_PART_ENTITIES}},
                    {'LOWER': {'IN': LENGTH_WORDS}},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'size'},
                ],
            ],
        }
    ]
}
