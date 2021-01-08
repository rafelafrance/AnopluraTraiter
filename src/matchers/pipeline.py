"""Create a trait pipeline."""

from traiter.pylib.pipeline import SpacyPipeline
# from traiter.pylib.sentencizer import SpacySentencizer
from traiter.pylib.to_entities import ToEntities

# from .description_old import description
from .matcher import Matcher
from ..pylib.consts import ABBREVS, ATTACH_STEP, DESCRIPTION_STEP, GROUP_STEP, \
    TRAIT_STEP


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    token2entity = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP}
    entities2keep = {TRAIT_STEP, ATTACH_STEP, DESCRIPTION_STEP}

    def __init__(self):
        super().__init__()

        self.nlp.max_length *= 2
        self.nlp.disable_pipes(['ner'])

        matcher = Matcher(self.nlp)
        # sentencizer = SpacySentencizer(ABBREVS, headings='heading')
        to_entities = ToEntities(self.entities2keep, self.token2entity)

        # self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(matcher, last=True)
        self.nlp.add_pipe(to_entities, last=True)
        # self.nlp.add_pipe(description, last=True)
