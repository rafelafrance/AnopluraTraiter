"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .body_length import BODY_LENGTH
from .body_part import BODY_PART
from .elevation import ELEVATION
from .event_date import COLLECTION_DATE
from .max_width import MAX_WIDTH
from .range import RANGE
from .sci_name import SCI_NAME
from .sclerotized import SCLEROTIZED
from .sex_count import SEX_COUNT
from .size import SIZE
from ..pylib.terms import TERMS, itis_terms

MATCHERS = (
    BODY_LENGTH, BODY_PART, COLLECTION_DATE, ELEVATION, MAX_WIDTH, RANGE,
    SCI_NAME, SCLEROTIZED, SEX_COUNT, SIZE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp, attach=True, as_entities=True):
        super().__init__(nlp, as_entities=as_entities)

        terms = TERMS
        terms += itis_terms('Anoplura', abbrev=True)
        terms += itis_terms('Mammalia', abbrev=True)
        self.add_terms(terms)

        traiters = []
        groupers = []
        attachers = []

        for matcher in MATCHERS:
            traiters += matcher.get('traits', [])
            groupers += matcher.get('groupers', [])
            attachers += matcher.get('attachers', [])

        self.add_patterns(groupers, 'groups')
        self.add_patterns(traiters, 'traits')
        if attach:
            self.add_patterns(attachers, 'attachers')
