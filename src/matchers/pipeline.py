"""Create a trait pipeline."""

from spacy.tokens import Doc
from traiter.pylib.util import clean_text
from traiter.spacy_nlp.pipeline import SpacyPipeline
from traiter.spacy_nlp.sentencizer import SpacySentencizer

from .matcher import Matcher
from ..pylib.util import ABBREVS, ATTACH_STEP, TRAIT_STEP


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP, ATTACH_STEP}
    trans = str.maketrans({'¼': '=', '⫻': '×'})

    def __init__(self):
        super().__init__()

        self.nlp.max_length *= 2
        self.nlp.disable_pipes(['ner'])

        self.matcher = Matcher(self.nlp)
        sentencizer = SpacySentencizer(ABBREVS)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)

    def find_entities(self, text: str) -> Doc:
        """Find entities in the doc."""
        text = clean_text(text, trans=self.trans)
        return super().find_entities(text)

    def sentence(self):
        """Parse traits based on sentence segmentation."""


PIPELINE = Pipeline()
