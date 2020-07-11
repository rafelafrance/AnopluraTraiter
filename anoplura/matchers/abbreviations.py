"""Find abbreviations in the text."""

from .shared import CLOSE, OPEN


NEW_TERMS = {}


def new_abbrev(span):
    """Find abbreviations and add them to the TERMS."""
    abbr = span.doc[span.start + 1]
    caps = [c for c in abbr.text if c.isupper()]
    start = span.start - len(caps)
    if len(caps) > 1 and start >= 0:
        words = span.doc[start:span.start]
        if all(c == t.text[0] for c, t in zip(caps, words)):
            NEW_TERMS[abbr.text] = words.text
    return {}


def abbrev(span):
    """Enrich the match."""
    return {'abbrev': span.text, 'definition': NEW_TERMS[span.text]}


def add_abbrevs(matcher_obj):
    """Add abbreviations to the rules."""
    rules = [
        {
            'label': 'abbrev',
            'on_match': abbrev,
            'patterns': [
                [
                    {'TEXT': {'IN': list(NEW_TERMS.keys())}},
                ],
            ],
        },
    ]
    matcher_obj.add_patterns(rules, 'traits')


ABBREV = {
    'name': 'abbrev',
    'finders': [
        {
            'label': 'new_abbrev',
            'on_match': new_abbrev,
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'IS_ALPHA': True},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ],
        },
    ],
}
