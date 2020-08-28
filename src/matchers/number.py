"""Parse counts."""

from traiter.pylib.util import to_positive_int

from ..pylib.util import GROUP_STEP, REPLACE

_TO = """ to """.split()
_KEYS = 'count low high'.split()


def word_count(span):
    """Convert a word range like 'five to six' into a numeric range."""
    words = [t.lower_ for t in span if t.ent_type_ == 'count_word']
    keys = _KEYS[:1] if len(words) == 1 else _KEYS[1:]
    data = {k: to_positive_int(REPLACE[w]) for k, w in zip(keys, words)}
    return data


NUMBER = {
    GROUP_STEP: [
        {
            'label': 'word_count',
            'on_match': word_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_word'},
                ],
                [
                    {'ENT_TYPE': 'count_word'},
                    {'LOWER': {'IN': _TO}},
                    {'ENT_TYPE': 'count_word'},
                ],
            ],
        },
    ],
}
