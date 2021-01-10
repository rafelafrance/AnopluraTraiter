"""Setup for all tests."""

from typing import Dict, List

from traiter.util import clean_text, shorten

from src.matchers.pipeline import Pipeline

TEST_PIPELINE = Pipeline()  # Singleton for testing

TRANS = str.maketrans({'¼': '=', '⫻': '×', '#': '♂', '$': '♀'})


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    text = clean_text(text, trans=TRANS)
    return TEST_PIPELINE.test_traits(text)
