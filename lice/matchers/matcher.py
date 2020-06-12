"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error
from traiter.util import Step  # pylint: disable=import-error

from .event_date import COLLECTION_DATE
from .elevation import ELEVATION
from .sex_count import SEX_COUNT
from .length import LENGTH
from .range import RANGE
from ..pylib.segmenter import NLP
from ..pylib.terms import TERMS, itis_terms

MATCHERS = (COLLECTION_DATE, ELEVATION, SEX_COUNT, LENGTH, RANGE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        terms = TERMS
        terms += itis_terms('Anoplura')
        terms += itis_terms('Mammalia', abbrev=True)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('matchers', [])
            groupers += matcher.get('groupers', [])

        self.add_patterns(groupers, Step.GROUP)
        self.add_patterns(traiters, Step.TRAIT)
        self.add_terms(terms)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        for sent in doc.sents:
            print('=' * 120)
            print(sent)
            for token in sent:
                label = token._.label
                data = token._.data
                print(label, data)

        traits = defaultdict(list)

        return traits
