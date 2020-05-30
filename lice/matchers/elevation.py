"""Parse elevation notations."""

from traiter.util import to_positive_int


def elevation(span):
    """Enrich the match with data."""


ELEVATION = {
    'name': 'elevation',
    'matchers': [
        {
            'label': 'elevation',
            'on_match': elevation,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                    {'_': {'label': 'units'}},
                    {'_': {'label': 'elevation'}},
                ]
            ]
        },
    ]
}
