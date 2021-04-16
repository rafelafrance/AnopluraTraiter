"""Actions for entities without patterns."""

import spacy
from traiter.actions import text_action

from anoplura.pylib.const import REPLACE

REPLACER = 'replacer.v1'


@spacy.registry.misc(REPLACER)
def replacer(ent):
    """Replace text in an entity."""
    text_action(ent, replace=REPLACE)


ACTIONS = {
    'sex': REPLACER,
    'seta_abbrev': REPLACER,
    'anoplura': REPLACER,
    'mammalia': REPLACER,
}
