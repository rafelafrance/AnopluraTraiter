"""Create a trait pipeline."""

import spacy
from traiter.patterns import add_ruler_patterns

from src.patterns.body_part import BODY_PART
from src.patterns.body_part_count import BODY_PART_COUNT
from src.patterns.length import LENGTH
from src.patterns.max_width import MAX_WIDTH
from src.patterns.numeric import NUMERIC
from src.patterns.sci_name import SCI_NAME
from src.patterns.seta_count import SETA_COUNT
from src.patterns.size import SIZE
from src.pylib.consts import TERMS


MATCHERS = [
    BODY_PART, BODY_PART_COUNT, LENGTH, MAX_WIDTH, NUMERIC,
    SCI_NAME, SETA_COUNT, SIZE]

MATCHERS1 = [NUMERIC]


def trait_pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])

    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())

    nlp.add_pipe('merge_entities', name='term_merger')

    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='numeric_ruler', config=config)
    add_ruler_patterns(match_ruler, *MATCHERS1)

    return nlp


def sentence_pipeline():
    """Setup the pipeline for extracting sentences."""
    nlp = spacy.blank('en')

    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe('entity_ruler', config=config)
    # add_ruler_patterns(term_ruler)

    nlp.add_pipe('merge_entities')

    abbrevs = """
        Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
        mm cm m
        al Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Figs Hist
        IUCN Inst Int Lond Me´m Mol Mus Nat nov Physiol Rep Sci Soc sp Syst Zool
        """.split()

    config = {'abbrevs': abbrevs, 'headings': ['heading']}
    nlp.add_pipe('sentence', config=config)

    # print(nlp.pipe_names)
    return nlp


# class Pipeline(SpacyPipeline):
#     """Build a traiter pipeline."""
#
#     def __init__(self):
#         super().__init__()
#
#         self.nlp.max_length *= 2
#         self.nlp.disable_pipes(['ner'])
#
#         token2entity = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP, DESCRIPTION_STEP}
#         entities2keep = {GROUP_STEP, TRAIT_STEP, ATTACH_STEP}
#
#         Term.add_pipes(self.nlp, TERMS, before='parser')
#         Sentencizer.add_pipe(
#             self.nlp, abbrevs=ABBREVS, headings='heading', before='parser')
#         Rule.add_pipe(self.nlp, MATCHERS, NUMERIC_STEP)
#         Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP)
#         Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP)
#         Rule.add_pipe(self.nlp, MATCHERS, ATTACH_STEP)
#         # Split.add_pipe(self.nlp, MATCHERS, DESCRIPTION_STEP)
#         ToEntities.add_pipe(self.nlp, entities2keep, token2entity)
#         self.nlp.add_pipe(description)
