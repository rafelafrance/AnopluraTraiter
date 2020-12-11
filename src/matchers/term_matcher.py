"""Base matcher object."""

from traiter.pylib.matcher import SpacyMatcher

from ..pylib.util import TERMS, TERM_STEP


class TermMatcher(SpacyMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS, step=TERM_STEP)
