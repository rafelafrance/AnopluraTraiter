import spacy
from traiter.pylib.pipes import extensions, sentence, tokenizer


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    return nlp


# """Create a trait pipeline."""
# import spacy
# from traiter.old_pipes.add_entity_data import ADD_ENTITY_DATA
# from traiter.old_pipes.cache import CACHE_LABEL
# from traiter.old_pipes.cleanup import CLEANUP
# from traiter.old_pipes.sentence import SENTENCE
# from traiter.old_pipes.update_entity_data import UPDATE_ENTITY_DATA
# from traiter.patterns.matcher_patterns import add_ruler_patterns
# from traiter.patterns.matcher_patterns import as_dicts
# from traiter.patterns.matcher_patterns import patterns_to_dispatch
# from traiter.tokenizer_util import append_abbrevs
# from traiter.tokenizer_util import append_tokenizer_regexes
#
# from ..patterns.body_part import BODY_PART
# from ..patterns.description import DESCRIPTION
# from ..patterns.measurement import LENGTH
# from ..patterns.measurement import MAX_WIDTH
# from ..patterns.measurement import MEAN
# from ..patterns.measurement import MEASUREMENT
# from ..patterns.measurement import SAMPLE
# from ..patterns.sci_name import GENUS
# from ..patterns.sci_name import SCI_NAME
# from ..patterns.seta_count import MULTIPLE_SETA
# from ..patterns.seta_count import SETA_COUNT
# from ..patterns.seta_count import SETAE
# from ..patterns.seta_count import SETAE_ABBREV
# from ..pylib.actions import ACTIONS
# from ..pylib.const import ABBREVS
# from ..pylib.const import FORGET
# from ..pylib.const import TERMS
#
# # from traiter.pipes.debug import debug_ents, debug_tokens
#
# GROUPERS =[BODY_PART, GENUS, SCI_NAME, SETAE, SETAE_ABBREV, MEAN, MEASUREMENT, SAMPLE]
# MATCHERS = [LENGTH, MAX_WIDTH, MULTIPLE_SETA, SETA_COUNT]
#
#
# def pipeline():
#     """Setup the pipeline for extracting traits."""
#     nlp = spacy.load("en_core_web_sm", exclude=["ner", "lemmatizer"])
#     append_tokenizer_regexes(nlp)
#     append_abbrevs(nlp, ABBREVS)
#
#     # Add a set of pipes to identify phrases and patterns as base-level traits
#     config = {"phrase_matcher_attr": "LOWER"}
#     term_ruler = nlp.add_pipe(
#         "entity_ruler", name="term_ruler", config=config, before="parser"
#     )
#     term_ruler.add_patterns(TERMS.for_entity_ruler())
#     nlp.add_pipe("merge_entities", name="term_merger")
#     nlp.add_pipe(CACHE_LABEL, name="term_cache")
#
#     # Sentence parsing should happen early but it may depend on terms
#     nlp.add_pipe(SENTENCE, before="parser", config={"automatic": ["heading"]})
#
#     # Add a set of pipes to group terms into larger traits
#     config = {"overwrite_ents": True}
#     group_ruler = nlp.add_pipe("entity_ruler", name="group_ruler", config=config)
#     add_ruler_patterns(group_ruler, GROUPERS)
#
#     nlp.add_pipe(CACHE_LABEL, name="group_cache")
#     nlp.add_pipe("merge_entities", name="group_merger")
#
#     # Add a pipe to group tokens into larger traits
#     config = {"overwrite_ents": True}
#     match_ruler = nlp.add_pipe("entity_ruler", name="match_ruler", config=config)
#     add_ruler_patterns(match_ruler, MATCHERS)
#
#     config = {"dispatch": patterns_to_dispatch(GROUPERS + MATCHERS) | ACTIONS}
#     nlp.add_pipe(ADD_ENTITY_DATA, config=config)
#
#     # Add a set of pipes to add descriptions to terms
#     config = {"patterns": as_dicts(DESCRIPTION)}
#     nlp.add_pipe(UPDATE_ENTITY_DATA, config=config)
#
#     # Remove unused entities
#     nlp.add_pipe(CLEANUP, config={"forget": FORGET})
#
#     # config = {'patterns': as_dict(PART_LINKER, SEX_LINKER, SUBPART_LINKER)}
#     # nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)
#
#     return nlp
