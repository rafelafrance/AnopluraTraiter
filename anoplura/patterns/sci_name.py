"""Get scientific names."""
import spacy
from spacy.tokens import Token
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import REPLACE

NAMES = ["anoplura", "mammalia"]

SCI_NAME = MatcherPatterns(
    "sci_name",
    on_match="anoplura.sci_name.v1",
    patterns=[[{"ENT_TYPE": {"IN": NAMES}}]],
)

GENUS = MatcherPatterns(
    "genus",
    on_match="anoplura.genus.v1",
    patterns=[[{"ENT_TYPE": "anoplura_genus"}]],
)


@spacy.registry.misc(SCI_NAME.on_match)
def sci_name(ent):
    """Enrich the match."""
    if isinstance(ent, Token):
        return

    ent._.data = {
        "sci_name": REPLACE.get(ent.text.lower(), ent.text.capitalize()),
        "group": ent[0]._.first_label,
    }


@spacy.registry.misc(GENUS.on_match)
def genus(ent):
    """Enrich the match."""
    if isinstance(ent, Token):
        return

    ent._.data = {
        "genus": REPLACE.get(ent.text.lower(), ent.text.capitalize()),
        "group": ent[0]._.first_label.split("_")[0],
    }
