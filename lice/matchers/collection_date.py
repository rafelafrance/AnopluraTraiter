"""Parse date notations."""

from dateutil import parser


def collection_date(span):
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
    'name': 'collection_date',
    'matchers': [
        {
            'label': 'collection_date',
            'on_match': collection_date,
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
