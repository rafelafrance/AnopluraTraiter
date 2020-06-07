"""Parse date notations."""

from dateutil import parser

from ..pylib.terms import REPLACE


def event_date(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    if not (value := parser.parse(span.text)):
        return {}

    data['date'] = value.isoformat()[:10]
    return data


COLLECTION_DATE = {
    'name': 'event_date',
    'matchers': [
        {
            'label': 'event_date',
            'on_match': event_date,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'_': {'label': 'month'}},
                    {'LIKE_NUM': True},
                ]
            ]
        },
    ]
}
