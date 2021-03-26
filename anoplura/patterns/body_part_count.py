"""Extract body part count notations."""

import re

import spacy
from traiter.const import INT_TOKEN_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_int

from anoplura.pylib.const import COMMON_PATTERNS

BODY_PART_COUNT = MatcherPatterns(
    'body_part_count',
    on_match='body_part_count.v1',
    decoder=COMMON_PATTERNS,
    patterns=['99 not_ent? not_ent? part'],
)


@spacy.registry.misc(BODY_PART_COUNT.on_match)
def body_part_count(ent):
    """Enrich the match."""
    part = [e.text for e in ent.ents if e._.cached_label == 'part'][0]
    part = part.lower()

    count = [t.text for t in ent if re.search(INT_TOKEN_RE, t.text)][0]
    count = to_positive_int(count)

    ent._.data = {'body_part': part, 'count': count}
