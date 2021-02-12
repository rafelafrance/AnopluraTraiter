"""Extract body part annotations."""

import re

import spacy
from traiter.const import COMMA
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import COMMON_PATTERNS, CONJ, MISSING, REPLACE

JOINER = CONJ + COMMA

BODY_PART = MatcherPatterns(
    'body_part',
    on_match='body_part.v1',
    decoder=COMMON_PATTERNS | {
        'seg': {'ENT_TYPE': 'segment'},
        'ordinal': {'ENT_TYPE': 'ordinal'},
        '99/ord': {'ENT_TYPE': {'IN': ['integer', 'ordinal']}},
    },
    patterns=[
        'missing part+',
        'missing? any_part* part',
        'ordinal -? part+',
        'part+ &/,/or* part* &/,/or* part+',
        'part+ 99/ord -? 99/ord',
        'part+ seg?',
        'seg part+',
    ],
)


@spacy.registry.misc(BODY_PART.on_match)
def body_part(ent):
    """Enrich the match."""
    data = {}

    parts = [REPLACE.get(t.lower_, t.lower_) for t in ent if t.text not in JOINER]
    data['body_part'] = re.sub(r'\s*-\s*', '-', ' '.join(parts))

    if [t for t in ent if t.lower_ in MISSING]:
        data['missing'] = True

    ent._.data = data
