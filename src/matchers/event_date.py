"""Parse date notations."""

from dateutil import parser
from ..pylib.util import TRAIT_STEP


def event_date(span):
    """Enrich the match with data."""
    data = {}

    if not (value := parser.parse(span.text)):
        return {}

    data['date'] = value.isoformat()[:10]
    return data


COLLECTION_DATE = {
    'name': 'event_date',
    TRAIT_STEP: [
        {
            'label': 'event_date',
            'on_match': event_date,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'ENT_TYPE': 'month'},
                    {'LIKE_NUM': True},
                ]
            ]
        },
    ]
}
