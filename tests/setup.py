"""Setup for all tests."""

from typing import Dict, List

from traiter.pylib.util import clean_text

from src.matchers.pipeline import Pipeline
from src.pylib.util import TRANS

TEST_PIPELINE = Pipeline()  # Singleton for testing


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = clean_text(text, trans=TRANS['custom'])
    return TEST_PIPELINE.test_traits(text)
