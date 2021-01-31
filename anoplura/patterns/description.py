"""Look for trait descriptions in sentences."""

from spacy.tokens import Span

from ..pylib.consts import DESCRIPTION_STEP


def description(doc):
    """Look for trait descriptions in sentences."""
    entities = []

    for sent in doc.sents:
        start = sent.start

        tokens = iter(sent[1:])  # Want to mess with the iteration in the loop
        for token in tokens:
            # No slice here we mess with the iterator in the loop
            if token.text in '.;':
                phrase = Span(doc, start, token.i)
                entities += phrase_ents(phrase)
                start = token.i + 1
            elif (token.text == ','
                  and token.i < sent.end - 1
                  and doc[token.i + 1].lower_ == 'with'):
                phrase = Span(doc, start, token.i)
                entities += phrase_ents(phrase)
                start = token.i + 2
                next(tokens)  # Skip past "with"

        if start < sent.end:
            phrase = Span(doc, start, sent.end)
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

    start = phrase.start
    for token in phrase[1:]:
        if token.text in ',:':
            if token.i - start > 1:
                desc = Span(phrase.doc, start, token.i)
                entities += new_ents(desc, body_part)
            start = token.i + 1

    if start != phrase.end:
        desc = Span(phrase.doc, start, phrase.end)
        entities += new_ents(desc, body_part)

    return entities


def new_ents(desc, body_part):
    """Remove possible overlapping trait."""
    if body_part.start == desc.start and body_part.end == desc.end:
        return []

    if not desc.ents:
        return [new_ent(desc, desc.start, desc.end, body_part)]

    if desc.start == body_part.start:
        return [new_ent(desc, body_part.end, desc.end, body_part)]

    if desc.end == body_part.end:
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
