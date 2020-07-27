"""Build the NLP pipeline."""

from collections import defaultdict

from traiter.spacy_nlp import spacy_nlp  # pylint: disable=import-error

from .segmenter import sentencizer
from ..matchers.matcher import Matcher

NLP = spacy_nlp(disable=['ner'])
NLP.add_pipe(sentencizer, before='parser')

MATCHER = Matcher(NLP)
NLP.add_pipe(MATCHER, after='parser')
NLP.max_length *= 2


def parse(text, with_sents=False):
    """Parse the traits."""
    doc = NLP(text)

    traits = defaultdict(list)

    sents = []

    for sent in doc.sents:
        sents.append((sent.start_char, sent.end_char))

        # if attach:
        #     attach_traits_to_parts(sent)

    for token in doc:
        label = token.ent_type_
        data = token._.data

        if label and data and token._.step in ('traits', 'attachers'):
            data = {k: v for k, v in token._.data.items()
                    if not k.startswith('_')}
            data['start'] = token.idx
            data['end'] = token.idx + len(token)
            traits[token._.label].append(data)

    # from pprint import pp
    # pp(dict(traits))

    return (traits, sents) if with_sents else traits
