"""Test range trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.spacy_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMeasurement(unittest.TestCase):
    """Test range trait matcher."""

    def test_antenna_01(self):
        self.assertEqual(
            NLP('antennae unmodified in males.'),
            [{'description': 'unmodified in males',
              'trait': 'antenna', 'start': 0, 'end': 29}]
        )

    def test_antenna_02(self):
        self.assertEqual(
            NLP(shorten("""
                Antennae five-segmented with basal segment wider than long and
                much larger than second segment; fourth segment slightly
                extended posterolaterally.
                """)),
            [{'description': ('five-segmented with basal segment wider than '
                              'long and much larger than second segment'),
              'trait': 'antenna', 'start': 0, 'end': 95}]
        )

    def test_antenna_03(self):
        self.assertEqual(
            NLP(shorten("""
                Head lacking eyes, with 5-segmented antennae which are often
                sexually dimorphic.
                """)),
            [{'end': 4, 'part': 'head', 'start': 0, 'trait': 'body_part'},
             {'description': '5-segmented which are often sexually dimorphic',
              'trait': 'antenna', 'start': 24, 'end': 80}]
        )
