"""Base matcher object."""

from traiter.spacy_nlp.matcher import SpacyMatcher

from ..pylib.util import TERMS


class TermMatcher(SpacyMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
