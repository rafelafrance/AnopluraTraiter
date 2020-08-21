"""Create a trait pipeline."""

# pylint: disable=import-error
import spacy
from traiter.pipeline import Pipeline as Pipes
from traiter.spacy_nlp import setup_tokenizer

from .util import ATTACH_STEP, TRAIT_STEP
from ..matchers.matcher import Matcher
from ..pylib.sentencizer import sentencizer


class Pipeline(Pipes):
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP, ATTACH_STEP}

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        super().__init__(self.nlp)

        self.nlp.max_length *= 2

        self.nlp.disable_pipes(['ner'])

        setup_tokenizer(self.nlp)

        self.matcher = Matcher(self.nlp)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)


PIPELINE = Pipeline()
