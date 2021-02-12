"""Get scientific names."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns

from anoplura.pylib.const import REPLACE

NAMES = ['anoplura', 'mammalia']

SCI_NAME = MatcherPatterns(
    'sci_name',
    on_match='sci_name.v1',
    patterns=[[{'ENT_TYPE': {'IN': NAMES}}]],
)

GENUS = MatcherPatterns(
    'genus',
    on_match='genus.v1',
    patterns=[[{'ENT_TYPE': 'anoplura_genus'}]],
)


@spacy.registry.misc(SCI_NAME.on_match)
def sci_name(ent):
    """Enrich the match."""
    ent._.data = {
        'sci_name': REPLACE.get(ent.lower_, ent.text.capitalize()),
        'group': ent[0].ent_type_,
    }


@spacy.registry.misc(GENUS.on_match)
def genus(ent):
    """Enrich the match."""
    ent._.data = {
        'genus': REPLACE.get(ent.lower_, ent.text.capitalize()),
        'group': ent[0].ent_type_.split('_')[0],
    }
