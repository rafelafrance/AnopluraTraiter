"""Base matcher object."""

from traiter.pylib.matcher import SpacyMatcher

from .body_part import BODY_PART
from .body_part_count import BODY_PART_COUNT
from .description import DESCRIPTION
from .length import LENGTH
from .max_width import MAX_WIDTH
from .numeric import NUMERIC
from .sci_name import SCI_NAME
from .seta_count import SETA_COUNT
from .size import SIZE
from ..pylib.consts import ATTACH_STEP, DESCRIPTION_STEP, GROUP_STEP, NUMERIC_STEP, \
    TERMS, TRAIT_STEP

# from .sex_count import SEX_COUNT
# from .elevation import ELEVATION
# from .event_date import COLLECTION_DATE

MATCHERS = [
    BODY_PART, BODY_PART_COUNT, DESCRIPTION, LENGTH, MAX_WIDTH, NUMERIC,
    SCI_NAME, SETA_COUNT, SIZE]


class Matcher(SpacyMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
        self.add_patterns(MATCHERS, NUMERIC_STEP)
        self.add_patterns(MATCHERS, GROUP_STEP)
        self.add_patterns(MATCHERS, TRAIT_STEP)
        self.add_patterns(MATCHERS, ATTACH_STEP)
        self.add_patterns(MATCHERS, DESCRIPTION_STEP)
