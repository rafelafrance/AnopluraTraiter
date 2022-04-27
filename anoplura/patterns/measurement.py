"""Parse size notations."""
import re

import spacy
from traiter.const import FLOAT_RE
from traiter.const import INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_float
from traiter.util import to_positive_int

from anoplura.pylib.const import COMMON_PATTERNS
from anoplura.pylib.const import REPLACE
from anoplura.pylib.const import TERMS


def list_to_re_choice(values):
    """Convert a list of values into a regex choice."""
    values = sorted(values, key=lambda v: -len(v))
    values = [re.escape(v) for v in values]
    pattern = "|".join(values)
    pattern = rf"({pattern})"
    return pattern


UNITS_RE = [t["pattern"] for t in TERMS if t["label"] == "metric_length"]
UNITS_RE = "(?<![A-Za-z])" + list_to_re_choice(UNITS_RE) + r"\b"

BODY_PART_ENTITIES = """ body_part setae setae_abbrev seta seta_abbrev """.split()
LENGTH_ENTITIES = """ measurement mean sample """.split()
LENGTH_WORDS = """ length len """.split()
MAXIMUM = """ maximum max """.split()
WIDTH = """ width """.split()

DECODER = COMMON_PATTERNS | {
    "bar": {"LOWER": {"IN": ["bar", "bars"]}},
    "mean_word": {"LOWER": "mean"},
    "punct": {"IS_PUNCT": True},
    "n": {"LOWER": "n"},
    "measurement": {"ENT_TYPE": "measurement"},
    "mean": {"ENT_TYPE": "mean"},
    "sample": {"ENT_TYPE": "sample"},
    "total": {"LOWER": "total", "OP": "?"},
    "part": {"ENT_TYPE": {"IN": BODY_PART_ENTITIES}},
    "len": {"LOWER": {"IN": LENGTH_WORDS}},
    "non_ent": {"ENT_TYPE": ""},
    "max": {"LOWER": {"IN": MAXIMUM}},
    "width": {"LOWER": {"IN": WIDTH}},
}

MEASUREMENT = MatcherPatterns(
    "measurement",
    decoder=DECODER,
    patterns=[
        "99.9 cm",
        "99.9 - 99.9 cm",
    ],
)

MEAN = MatcherPatterns(
    "mean",
    decoder=DECODER,
    patterns=["mean_word punct? 99.9 cm?"],
)

SAMPLE = MatcherPatterns(
    "sample",
    decoder=DECODER,
    patterns=["n = 99"],
)

LENGTH = MatcherPatterns(
    "length",
    on_match="anoplura.length.v1",
    decoder=DECODER,
    patterns=[
        "part len punct? measurement punct? mean? punct* sample? punct?",
        (
            "total? part len non_ent? non_ent? bar? punct* "
            "measurement punct? mean? punct* sample? punct?"
        ),
    ],
)

MAX_WIDTH = MatcherPatterns(
    "max_width",
    on_match="anoplura.max_width.v1",
    decoder=DECODER,
    patterns=[
        (
            "max part width non_ent? non_ent? bar? punct* "
            "measurement punct? mean? punct* sample? punct?"
        ),
    ],
)


@spacy.registry.misc(MAX_WIDTH.on_match)
def max_width(ent):
    """Enrich the match."""
    measurement_parts(ent)


@spacy.registry.misc(LENGTH.on_match)
def length(ent):
    """Enrich a size match."""
    measurement_parts(ent)

    if ent.text.lower().find("total") > -1:
        ent._.new_label = "total_length"


def measurement_parts(ent):
    """Fill in the measurement parts."""
    data = {}
    for token in ent:
        label = token._.cached_label

        if label in BODY_PART_ENTITIES:
            data |= {label: REPLACE.get(token.lower_, token.lower_)}

        if label == "measurement":
            data |= measurement(token)

        elif label == "mean":
            data |= mean(token)

        elif label == "sample":
            data |= sample(token)

    ent._.data = data


def measurement(token):
    """Enrich a measurement match."""
    values = re.findall(FLOAT_RE, token.text)
    values = [to_positive_float(v) for v in values]

    data = {k: v for k, v in zip(["low", "high"], values)}

    match = re.search(UNITS_RE, token.text)
    units = match.group(0)
    data["length_units"] = units

    return data


def mean(token):
    """Convert the span into a single float."""
    match = re.search(FLOAT_RE, token.text)
    value = match.group(0)

    match = re.search(UNITS_RE, token.text.lower())
    units = match.group(0) if match else None

    data = {"mean": to_positive_float(value)}

    if units:
        data["mean_units"] = units

    return data


def sample(token):
    """Convert the span into a single integer."""
    match = re.search(INT_RE, token.text)
    value = match.group(0)
    return {"n": to_positive_int(value)}
