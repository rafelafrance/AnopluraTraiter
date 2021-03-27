"""Setup for all tests."""

from typing import Dict, List

from traiter.util import clean_text, shorten

from anoplura.pylib.pipeline import pipeline

NLP = pipeline()  # Singleton for testing

# Translate characters resulting from PDF madness
TRANS = str.maketrans({'¼': '=', '⫻': '×', '#': '♂', '$': '♀'})


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    text = clean_text(text, trans=TRANS)

    doc = NLP(text)

    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    # from spacy import displacy
    # options = {'collapse_punct': False, 'compact': True}
    # displacy.serve(doc, options=options)

    return traits
