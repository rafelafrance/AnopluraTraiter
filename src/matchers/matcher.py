"""Base matcher object."""

from traiter.matcher import TraitMatcher  # pylint: disable=import-error

from .abbreviations import ABBREV
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
from ..pylib.terms import TERMS
from ..pylib.util import ATTACH_STEP, FIND_STEP, GROUP_STEP, TRAIT_STEP

MATCHERS = (
    ABBREV, BODY_LENGTH, BODY_PART, COLLECTION_DATE, ELEVATION, MAX_WIDTH,
    RANGE, SCI_NAME, SCLEROTIZED, SEX_COUNT, SIZE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        terms = TERMS
        self.add_terms(terms)

        finders = []
        traiters = []
        groupers = []
        attachers = []

        for matcher in MATCHERS:
            finders += matcher.get(FIND_STEP, [])
            groupers += matcher.get(GROUP_STEP, [])
            traiters += matcher.get(TRAIT_STEP, [])
            attachers += matcher.get(ATTACH_STEP, [])

        self.add_patterns(finders, FIND_STEP)
        self.add_patterns(groupers, GROUP_STEP)
        self.add_patterns(traiters, TRAIT_STEP)
        self.add_patterns(attachers, ATTACH_STEP)
