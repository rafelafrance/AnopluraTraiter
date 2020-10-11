"""Create a trait pipeline."""

from spacy.tokens import Doc
from traiter.pylib.util import clean_text
from traiter.spacy_nlp.pipeline import SpacyPipeline
from traiter.spacy_nlp.sentencizer import SpacySentencizer

from .description import description
from .matcher import Matcher
from ..pylib.util import ABBREVS, ATTACH_STEP, DESCRIPTION_STEP, TRAIT_STEP


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    token2entity = {TRAIT_STEP, ATTACH_STEP}
    entities2keep = {DESCRIPTION_STEP}
    trans = str.maketrans({'¼': '=', '⫻': '×'})

    def __init__(self):
        super().__init__()

        self.nlp.max_length *= 2
        self.nlp.disable_pipes(['ner'])

        self.matcher = Matcher(self.nlp)
        sentencizer = SpacySentencizer(ABBREVS)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)
        self.nlp.add_pipe(description, last=True)

    def find_entities(self, text: str) -> Doc:
        """Find entities in the doc."""
        text = clean_text(text, trans=self.trans)
        return super().find_entities(text)


PIPELINE = Pipeline()
