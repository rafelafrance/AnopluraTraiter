"""Setup for all tests."""

from typing import Dict, List

# from spacy import displacy
from traiter.util import clean_text, shorten

from src.pylib.pipeline import trait_pipeline

NLP = trait_pipeline()  # Singleton for testing

TRANS = str.maketrans({'¼': '=', '⫻': '×', '#': '♂', '$': '♀'})


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    text = clean_text(text, trans=TRANS)

    doc = NLP(text)

    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    # displacy.serve(doc)

    return traits
