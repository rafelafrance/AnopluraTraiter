"""Create a trait pipeline."""
import spacy
from traiter.patterns.matcher_patterns import add_ruler_patterns
from traiter.patterns.matcher_patterns import as_dicts
from traiter.patterns.matcher_patterns import patterns_to_dispatch
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cache import CACHE_LABEL
from traiter.pipes.cleanup import CLEANUP
from traiter.pipes.sentence import SENTENCE
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs
from traiter.tokenizer_util import append_tokenizer_regexes

from anoplura.patterns.body_part import BODY_PART
from anoplura.patterns.description import DESCRIPTION
from anoplura.patterns.measurement import LENGTH
from anoplura.patterns.measurement import MAX_WIDTH
from anoplura.patterns.measurement import MEAN
from anoplura.patterns.measurement import MEASUREMENT
from anoplura.patterns.measurement import SAMPLE
from anoplura.patterns.sci_name import GENUS
from anoplura.patterns.sci_name import SCI_NAME
from anoplura.patterns.seta_count import MULTIPLE_SETA
from anoplura.patterns.seta_count import SETA_COUNT
from anoplura.patterns.seta_count import SETAE
from anoplura.patterns.seta_count import SETAE_ABBREV
from anoplura.pylib.actions import ACTIONS
from anoplura.pylib.const import ABBREVS
from anoplura.pylib.const import FORGET
from anoplura.pylib.const import TERMS

# from traiter.pipes.debug import debug_ents, debug_tokens

GROUPERS = [BODY_PART, GENUS, SCI_NAME, SETAE, SETAE_ABBREV, MEAN, MEASUREMENT, SAMPLE]
MATCHERS = [LENGTH, MAX_WIDTH, MULTIPLE_SETA, SETA_COUNT]


def pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "lemmatizer"])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # Add a set of pipes to identify phrases and patterns as base-level traits
    config = {"phrase_matcher_attr": "LOWER"}
    term_ruler = nlp.add_pipe(
        "entity_ruler", name="term_ruler", config=config, before="parser"
    )
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    nlp.add_pipe("merge_entities", name="term_merger")
    nlp.add_pipe(CACHE_LABEL, name="term_cache")

    # Sentence parsing should happen early but it may depend on terms
    nlp.add_pipe(SENTENCE, before="parser", config={"automatic": ["heading"]})

    # Add a set of pipes to group terms into larger traits
    config = {"overwrite_ents": True}
    group_ruler = nlp.add_pipe("entity_ruler", name="group_ruler", config=config)
    add_ruler_patterns(group_ruler, GROUPERS)

    nlp.add_pipe(CACHE_LABEL, name="group_cache")
    nlp.add_pipe("merge_entities", name="group_merger")

    # Add a pipe to group tokens into larger traits
    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="match_ruler", config=config)
    add_ruler_patterns(match_ruler, MATCHERS)

    # debug_tokens(nlp)

    config = {"dispatch": patterns_to_dispatch(GROUPERS + MATCHERS) | ACTIONS}
    nlp.add_pipe(ADD_ENTITY_DATA, config=config)

    # Add a set of pipes to add descriptions to terms
    config = {"patterns": as_dicts(DESCRIPTION)}
    nlp.add_pipe(UPDATE_ENTITY_DATA, config=config)

    # Remove unused entities
    nlp.add_pipe(CLEANUP, config={"entities": FORGET})

    # config = {'patterns': as_dict(PART_LINKER, SEX_LINKER, SUBPART_LINKER)}
    # nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    return nlp
