"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .event_date import COLLECTION_DATE
from .elevation import ELEVATION
from .max_width import MAX_WIDTH
from .sci_name import SCI_NAME
from .sclerotized import SCLEROTIZED
from .sex_count import SEX_COUNT
from .size import SIZE
from .range import RANGE
from ..pylib.segmenter import NLP
from ..pylib.terms import TERMS, itis_terms

MATCHERS = (
    COLLECTION_DATE, ELEVATION, MAX_WIDTH, RANGE,
    SCI_NAME, SCLEROTIZED, SEX_COUNT, SIZE)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        terms = TERMS
        terms += itis_terms('Anoplura', abbrev=True)
        terms += itis_terms('Mammalia', abbrev=True)
        self.add_terms(terms)

        traiters = []
        groupers = []
        attachers = []

        for matcher in MATCHERS:
            traiters += matcher.get('matchers', [])
            groupers += matcher.get('groupers', [])
            attachers += matcher.get('attachers', [])

        self.add_patterns(groupers, 'groups')
        self.add_patterns(traiters, 'traits')
        self.add_patterns(attachers, 'attachers')

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)
        traits = defaultdict(list)

        for sent in doc.sents:
            # if 'head' in sent.text:
            #     print(sent)
            #     print()
            for token in sent:
                label = token._.label
                data = token._.data
                if label and data and token._.step in ('traits', 'attachers'):
                    data = {k: v for k, v in token._.data.items()
                            if not k.startswith('_')}
                    data['start'] = token.idx
                    data['end'] = token.idx + len(token)
                    traits[label].append(data)

        # from pprint import pp
        # pp(dict(traits))

        return traits
