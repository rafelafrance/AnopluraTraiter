"""Look for trait descriptions in sentences."""

from spacy.tokens import Span

from ..pylib.util import DESCRIPTION_STEP


def description(doc):
    """Look for trait descriptions in sentences."""
    entities = []
    for sent in doc.sents:
        entities += phrases(sent)

    doc.ents = tuple(entities)

    return doc


def phrases(sent):
    """Split the sentence into phrases."""
    entities = []
    start = 0
    for token in sent:
        if token.ent_type_ == 'phrase_sep':
            span = sent[start:token.i]
            entities += phrase_entities(span,)
            start = token.i + 1

    if start < sent.end:
        span = sent[start:]
        entities += phrase_entities(span)

    return entities


def phrase_entities(phrase):
    """Extract phase entities."""
    body_part = [e for e in phrase.ents if e.label_ == 'body_part']

    if len(body_part) == 1:
        entities = body_part + descriptions(phrase, body_part[0])
    else:
        entities = list(phrase.ents)

    return entities


def descriptions(phrase, body_part):
    """Split a phrase into comma separated descriptions."""
    entities = []
    start, in_description = 0, False
    for token in phrase:
        if token.ent_type_ in ('description_sep', 'body_part'):
            if in_description:
                entities.append(new_ent(phrase, start, token.i, body_part))
            start = token.i + 1
            in_description = False
        elif token.is_punct and not in_description:
            start = token.i + 1
        else:
            in_description = True

    if start < phrase.end:
        entities.append(new_ent(phrase, start, phrase.end, body_part))

    return entities


def new_ent(phrase, start, end, body_part):
    """Build a description entity."""
    entity = Span(phrase.doc, start, end, label=DESCRIPTION_STEP)
    entity._.data = {
        'description': entity.text,
        'body_part': body_part[0]._.data['body_part'],
        'trait': DESCRIPTION_STEP,
        'start': entity.start_char,
        'end': entity.end_char,
    }
    entity._.step = DESCRIPTION_STEP
    return entity
