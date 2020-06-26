"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error
from traiter.util import Step  # pylint: disable=import-error

from .event_date import COLLECTION_DATE
from .elevation import ELEVATION
from .sex_count import SEX_COUNT
from .size import SIZE
from .range import RANGE
from ..pylib.segmenter import NLP
from ..pylib.terms import TERMS, itis_terms

MATCHERS = (COLLECTION_DATE, ELEVATION, RANGE, SEX_COUNT, SIZE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        terms = TERMS
        terms += itis_terms('Anoplura')
        terms += itis_terms('Mammalia', abbrev=True)
        self.add_terms(terms)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('matchers', [])
            groupers += matcher.get('groupers', [])

        self.add_patterns(groupers, Step.GROUP)
        self.add_patterns(traiters, Step.TRAIT)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)
        traits = defaultdict(list)

        for sent in doc.sents:
            for token in sent:
                label = token._.label
                data = token._.data
                if label and data and token._.step == Step.TRAIT:
                    traits[label].append(data)

        # from pprint import pp
        # pp(dict(traits))

        return traits
