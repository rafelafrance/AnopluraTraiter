"""Extract sclerotized annotations."""


def sclerotized(span):
    """Enrich the match."""
    data = {}
    for token in span:
        if token._.label == 'sclerotin':
            pass
        else:
            data['sclerotized'] = token.lower_
    return data


SCLEROTIZED = {
    'name': 'sclerotized',
    'traits': [
        {
            'label': 'sclerotized',
            'on_match': sclerotized,
            'patterns': [
                [
                    {'POS': 'ADV'},
                    {'_': {'label': 'sclerotin'}},
                ],
            ],
        },
    ],
}
