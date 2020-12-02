"""Create a pipeline for splitting sentences only."""

from traiter.pylib.pipeline import SpacyPipeline
from traiter.pylib.to_entities import ToEntities
from traiter.pylib.sentencizer import SpacySentencizer

from .term_matcher import TermMatcher
from ..pylib.util import ABBREVS, ATTACH_STEP, DESCRIPTION_STEP, GROUP_STEP, \
    TRAIT_STEP


class SentencePipeline(SpacyPipeline):
    """Create a pipeline for splitting sentences only."""

    token2entity = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP}
    entities2keep = {TRAIT_STEP, ATTACH_STEP, DESCRIPTION_STEP}

    def __init__(self):
        super().__init__()

        self.nlp.max_length *= 2
        self.nlp.disable_pipes(['ner'])

        self.term_matcher = TermMatcher(self.nlp)
        to_entities = ToEntities(self.entities2keep, self.token2entity)
        sentencizer = SpacySentencizer(ABBREVS, headings='heading')

        self.nlp.add_pipe(self.term_matcher, before='parser')
        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(to_entities, last=True)
