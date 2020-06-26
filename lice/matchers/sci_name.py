"""Get scientific names."""


NAMES = {'anoplura', 'mammalia'}


def sci_name(span):
    """Enrich the match."""
    data = {'sci_name': span.text, 'label': span[0]._.label}
    return data


SCI_NAME = {
    'name': 'sci_name',
    'matchers': [
        {
            'label': 'sci_name',
            'on_match': sci_name,
            'patterns': [
                [
                    {'_': {'label': {'IN': list(NAMES)}}},
                ],
            ],
        },
    ],
}
