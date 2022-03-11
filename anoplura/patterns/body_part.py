"""Extract body part annotations."""
import re

import spacy
from traiter.const import COMMA
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import COMMON_PATTERNS
from anoplura.pylib.const import CONJ
from anoplura.pylib.const import MISSING
from anoplura.pylib.const import REPLACE

JOINER = CONJ + COMMA
JOINER_RE = "|".join(JOINER + [r"\s"])
JOINER_RE = re.compile(rf"\b(?:{JOINER_RE})\b", flags=re.IGNORECASE)

MISSING_RE = "|".join([fr"\b{m}\b" for m in MISSING])
MISSING_RE = re.compile(MISSING_RE, flags=re.IGNORECASE)

BODY_PART = MatcherPatterns(
    "body_part",
    on_match="anoplura.body_part.v1",
    decoder=COMMON_PATTERNS
    | {
        "seg": {"ENT_TYPE": "segmented"},
        "ord": {"ENT_TYPE": {"IN": ["ordinal", "number_word"]}},
    },
    patterns=[
        "missing part+",
        "missing? any_part* part",
        "part+ &/,/or* part* &/,/or* part+",
        "part+ ord -? ord",
        "part+ 99? -? 99",
        "part+ ord?",
        "part+ 99?",
        "part+ ord -? seg",
        "part+ 99 -? seg",
        "ord? -? seg? part+",
        "99 - seg part+",
    ],
)


@spacy.registry.misc(BODY_PART.on_match)
def body_part(ent):
    """Enrich a body part span."""
    data = {}

    parts = JOINER_RE.split(ent.text.lower())
    parts = [REPLACE.get(p, p) for p in parts]
    text = " ".join(parts)
    text = re.sub(r"\s*-\s*", "-", text)
    text = REPLACE.get(text, text)

    if MISSING_RE.search(ent.text.lower()) is not None:
        data["missing"] = True

    data["body_part"] = text

    ent._.data = data
