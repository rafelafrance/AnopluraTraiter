"""Common actions for enriching matches."""

from ..pylib.util import REPLACE


def text_action(span):
    """Enrich term matches."""
    label = span.label_.split('.')[0]
    return {label: REPLACE.get(span.lower_, span.lower_)}
