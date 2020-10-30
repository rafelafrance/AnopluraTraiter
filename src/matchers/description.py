"""Look for trait descriptions in sentences."""

import re

from spacy.tokens import Span

from ..pylib.util import DESCRIPTION_STEP

PHRASE_SEP = re.compile(
    r' \s* (?: [;.]+ | , \s* with ) \s* ',
    flags=re.IGNORECASE | re.VERBOSE)

DESCRIPTION_SEP = re.compile(
    r' \s* [,:]+ \s* ',
    flags=re.IGNORECASE | re.VERBOSE)


def description(doc):
    """Look for trait descriptions in sentences."""
    entities = []

    start = 0
    for sent in doc.sents:
        for match in PHRASE_SEP.finditer(sent.text):
            phrase = sent.char_span(start, match.start())
            if not phrase:
                continue
            entities += phrase_ents(phrase)
            start = match.end()

        if start != len(sent.text):
            phrase = sent.char_span(start, len(sent.text))
            entities += phrase_ents(phrase)

    doc.ents = tuple(entities)

    return doc


def phrase_ents(phrase):
    """Split the sentence into phrases."""
    if (len(phrase.ents) < 1 or len(phrase.ents) > 1
            or phrase.ents[0].label_ != 'body_part'):
        return list(phrase.ents)

    body_part = phrase.ents[0]
    entities = [body_part]

    start = 0
    for match in DESCRIPTION_SEP.finditer(phrase.text):
        desc = phrase.char_span(start, match.start())
        if not desc:
            continue
        start = match.end()
        entities += new_ents(desc, body_part)

    if start != len(phrase.text):
        desc = phrase.char_span(start, len(phrase.text))
        entities += new_ents(desc, body_part)

    return entities


def new_ents(desc, body_part):
    """Remove possible overlapping trait."""
    if not desc.ents:
        return [new_ent(desc, desc.start, desc.end, body_part)]
    elif desc.start == body_part.start:
        return [new_ent(desc, body_part.end, desc.end, body_part)]
    elif desc.end == body_part.end:
        return [new_ent(desc, desc.start, body_part.start, body_part)]
    return [
        new_ent(desc, desc.start, body_part.start, body_part),
        new_ent(desc, body_part.end, desc.end, body_part),
    ]


def new_ent(desc, start, end, body_part):
    """Build a description entity."""
    entity = Span(desc.doc, start, end, label=DESCRIPTION_STEP)
    entity._.data = {
        'description': entity.text,
        'body_part': body_part._.data['body_part'],
        'trait': DESCRIPTION_STEP,
        'start': entity.start_char,
        'end': entity.end_char,
    }
    entity._.step = DESCRIPTION_STEP
    return entity
