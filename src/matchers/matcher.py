"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher

from .body_length import BODY_LENGTH
from .body_part import BODY_PART
from .number import NUMBER
from .elevation import ELEVATION
from .event_date import COLLECTION_DATE
from .max_width import MAX_WIDTH
from .range import RANGE
from .sci_name import SCI_NAME
from .sclerotized import SCLEROTIZED
from .setae_count import SETAE_COUNT
from .sex_count import SEX_COUNT
from .size import SIZE
from ..pylib.util import ATTACH_STEP, GROUP_STEP, TERMS, TRAIT_STEP

MATCHERS = (
    BODY_LENGTH, BODY_PART, COLLECTION_DATE, ELEVATION, MAX_WIDTH, NUMBER,
    RANGE, SCI_NAME, SCLEROTIZED, SETAE_COUNT, SEX_COUNT, SIZE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
        self.add_patterns(MATCHERS, GROUP_STEP)
        self.add_patterns(MATCHERS, TRAIT_STEP)
        self.add_patterns(MATCHERS, ATTACH_STEP)
