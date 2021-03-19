"""Extract body part annotations."""

import re

import spacy
from spacy.tokens import Token
from traiter.const import COMMA
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import COMMON_PATTERNS, CONJ, MISSING, REPLACE

JOINER = CONJ + COMMA
JOINER_RE = '|'.join(JOINER)
JOINER_RE = re.compile(JOINER_RE)

MISSING_RE = '|'.join([fr'\b{m}\b' for m in MISSING])
MISSING_RE = re.compile(MISSING_RE)

BODY_PART = MatcherPatterns(
    'body_part',
    on_match='body_part.v1',
    decoder=COMMON_PATTERNS | {
        'seg': {'ENT_TYPE': 'segmented'},
        'ord': {'ENT_TYPE': {'IN': ['ordinal', 'number_word']}},
    },
    patterns=[
        'missing part+',
        'missing? any_part* part',
        'part+ &/,/or* part* &/,/or* part+',
        'part+ ord -? ord',
        'part+ 99? -? 99',
        'part+ ord?',
        'part+ 99?',
        'part+ ord -? seg',
        'part+ 99 -? seg',
        'ord? -? seg? part+',
        '99 -? seg? part+',
    ],
)


@spacy.registry.misc(BODY_PART.on_match)
def body_part(frag):
    """Enrich the match."""
    if isinstance(frag, Token):
        body_part_token(frag)
    else:
        body_part_span(frag)


def body_part_span(ent):
    """Enrich a body part span."""
    data = {}

    parts = [REPLACE.get(t.lower_, t.lower_) for t in ent if t.text not in JOINER]
    data['body_part'] = re.sub(r'\s*-\s*', '-', ' '.join(parts))

    if [t for t in ent if MISSING_RE.search(t.lower_) is not None]:
        data['missing'] = True

    ent._.data = data


def body_part_token(token):
    """Enrich a body part token."""
    data = {}

    parts = JOINER_RE.split(token.lower_)
    parts = [REPLACE.get(p, p) for p in parts]

    data['body_part'] = re.sub(r'\s*-\s*', '-', ' '.join(parts))

    if MISSING_RE.search(token.lower_) is not None:
        data['missing'] = True

    token._.data = data
