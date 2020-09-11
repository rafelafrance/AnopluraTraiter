"""Parse counts."""

from ..pylib.util import GROUP_STEP
from .shared import DASH

TO_INT = {
    'no': 0,
    'pair': 2,

    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
}

_OTHER_WORDS = """ no pair """.split()
_TO = ['to'] + DASH
_KEYS = 'count low high'.split()


def count(span):
    """Convert a word range like 'five to six' into a numeric range."""
    words = [t.lower_ for t in span if t.lower_ not in _TO]
    keys = _KEYS[:1] if len(words) == 1 else _KEYS[1:]
    try:
        data = {k: int(TO_INT.get(w, w)) for k, w in zip(keys, words)}
    except ValueError:
        return {'_forget': True}
    return data


NUMBER = {
    GROUP_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'LIKE_NUM': True},
                ],
                [
                    {'LIKE_NUM': True},
                    {'LOWER': {'IN': _TO}},
                    {'LIKE_NUM': True},
                ],
                [
                    {'LOWER': {'IN': _OTHER_WORDS}},
                ],
            ],
        },
    ],
}
