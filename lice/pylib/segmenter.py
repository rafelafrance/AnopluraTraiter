"""Custom sentence splitter."""

import re
from traiter.spacy_nlp import spacy_nlp  # pylint: disable=import-error

FLAGS = re.MULTILINE | re.VERBOSE

ABBREVS = '|'.join("""
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    mm cm m
    Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Hist IUCN Inst Int
    Lond Me´m Mol Mus Nat Physiol Rep Sci Soc Syst Zool
    """.split())
ABBREVS = re.compile(fr'(?: {ABBREVS} ) $', flags=re.VERBOSE)

TRANS_TABLE = {'¼': '='}
TRANS = str.maketrans(TRANS_TABLE)


def clean_pdf(text):
    """Remove headers & footers and join hyphenated words etc."""
    # Clean up chars
    text = text.translate(TRANS)

    # Remove headers and footers
    text = re.sub(r'^ \s* \d+ \s* $', '', text, flags=FLAGS)
    text = re.sub(r'^ \s* Journal \s+ of .* $', '', text, flags=FLAGS)

    # Remove figure notations
    text = re.sub(r'^ \s* Fig\. .+ $', '', text, flags=FLAGS)

    # Joining hyphens has to happen after the removal of headers & footers
    text = re.sub(r' [–-] \n ([a-z]) ', r'\1', text, flags=FLAGS)

    # Space normalize text
    return ' '.join(text.split())


def custom_sentencizer(doc):
    """Break the text into sentences."""
    for i, token in enumerate(doc[:-1]):
        prev_token = doc[i-1] if i > 0 else None
        next_token = doc[i+1]
        if (token.text == '.' and re.match(r'[A-Z]', next_token.prefix_)
                and not ABBREVS.match(next_token.text)
                and len(next_token) > 1 and len(prev_token) > 1):
            next_token.is_sent_start = True
        else:
            next_token.is_sent_start = False

    return doc


NLP = spacy_nlp(['ner'])
NLP.add_pipe(custom_sentencizer, before='parser')
