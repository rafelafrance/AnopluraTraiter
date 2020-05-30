"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .collection_date import COLLECTION_DATE
from .sex_count import SEX_COUNT
from ..pylib.terms import TERMS, itis_terms

MATCHERS = (SEX_COUNT, COLLECTION_DATE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self):
        super().__init__()

        terms = TERMS
        terms += itis_terms('Anoplura')
        terms += itis_terms('Mammalia', abbrev=True)

        trait_patterns = []
        group_patterns = {}

        for matcher in MATCHERS:
            trait_patterns += matcher['matchers']
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)
        self.add_terms(terms)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        traits = defaultdict(list)

        return traits
