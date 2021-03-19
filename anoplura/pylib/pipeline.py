"""Create a trait pipeline."""

import spacy
from traiter.patterns.matcher_patterns import add_ruler_patterns, as_dicts
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cache import CACHE_LABEL
from traiter.pipes.cleanup import CLEANUP
from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS
from traiter.pipes.sentence import SENTENCE
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

from anoplura.patterns.body_part import BODY_PART
from anoplura.patterns.body_part_count import BODY_PART_COUNT
from anoplura.patterns.length import LENGTH, MEAN, MEASUREMENT, SAMPLE
from anoplura.patterns.max_width import MAX_WIDTH
from anoplura.patterns.sci_name import GENUS, SCI_NAME
from anoplura.patterns.seta_count import MULTIPLE_SETA, SETAE, SETAE_ABBREV, SETA_COUNT
from anoplura.pylib.const import ABBREVS, FORGET, TERMS

GROUPERS = [BODY_PART, GENUS, SCI_NAME, SETAE, SETAE_ABBREV, MEAN, MEASUREMENT, SAMPLE]
MATCHERS = [BODY_PART_COUNT, MAX_WIDTH, MULTIPLE_SETA, SETA_COUNT, LENGTH]

DEBUG_COUNT = 0  # Used to rename debug pipes


def pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # Add a set of pipes to identify phrases and patterns as base-level traits
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(CACHE_LABEL, name='term_cache')

    # Sentence parsing should happen early but it may depend on terms
    nlp.add_pipe(SENTENCE, before='parser', config={'automatic': ['heading']})

    # Add a set of pipes to group terms into larger traits
    config = {'overwrite_ents': True}
    group_ruler = nlp.add_pipe('entity_ruler', name='group_ruler', config=config)
    add_ruler_patterns(group_ruler, GROUPERS)
    nlp.add_pipe(CACHE_LABEL, name='group_cache')
    nlp.add_pipe('merge_entities', name='group_merger')

    # Add a pipe to group tokens into larger traits
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, MATCHERS)

    nlp.add_pipe(CLEANUP, config={'entities': FORGET})

    config = {'patterns': as_dicts(GROUPERS + MATCHERS)}
    nlp.add_pipe(ADD_ENTITY_DATA, config=config)

    # config = {'patterns': as_dict(PART_LINKER, SEX_LINKER, SUBPART_LINKER)}
    # nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    return nlp


def add_debug_pipes(nlp, message='', tokens=True, entities=False, **kwargs):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    if tokens:
        nlp.add_pipe(
            DEBUG_TOKENS,
            name=f'debug_tokens{DEBUG_COUNT}',
            config=config,
            **kwargs,
        )
    if entities:
        nlp.add_pipe(
            DEBUG_ENTITIES,
            name=f'debug_entities{DEBUG_COUNT}',
            config=config,
            **kwargs,
        )
