"""Create a trait pipeline."""

from traiter.matchers.rule import Rule
# from traiter.matchers.split import Split
from traiter.matchers.term import Term
from traiter.pipeline import SpacyPipeline
from traiter.sentencizer import Sentencizer
from traiter.to_entities import ToEntities

from .body_part import BODY_PART
from .body_part_count import BODY_PART_COUNT
from .description import description  # DESCRIPTION
from .length import LENGTH
from .max_width import MAX_WIDTH
from .numeric import NUMERIC
from .sci_name import SCI_NAME
from .seta_count import SETA_COUNT
from .size import SIZE
from ..pylib.consts import ABBREVS, ATTACH_STEP, DESCRIPTION_STEP, GROUP_STEP, \
    NUMERIC_STEP, TERMS, TRAIT_STEP

MATCHERS = [
    BODY_PART, BODY_PART_COUNT, LENGTH, MAX_WIDTH, NUMERIC,
    SCI_NAME, SETA_COUNT, SIZE]  # , DESCRIPTION]


class Pipeline(SpacyPipeline):
    """Build a traiter pipeline."""

    def __init__(self):
        super().__init__()

        self.nlp.max_length *= 2
        self.nlp.disable_pipes(['ner'])

        token2entity = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP, DESCRIPTION_STEP}
        entities2keep = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP}

        Term.add_pipes(self.nlp, TERMS, before='parser')
        Sentencizer.add_pipe(
            self.nlp, abbrevs=ABBREVS, headings='heading', before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, NUMERIC_STEP)
        Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP)
        Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP)
        Rule.add_pipe(self.nlp, MATCHERS, ATTACH_STEP)
        # Split.add_pipe(self.nlp, MATCHERS, DESCRIPTION_STEP)
        ToEntities.add_pipe(self.nlp, entities2keep, token2entity)
        self.nlp.add_pipe(description)
