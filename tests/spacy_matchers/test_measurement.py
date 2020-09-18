"""Test range trait matcher."""

import unittest

from src.spacy_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMeasurement(unittest.TestCase):
    """Test range trait matcher."""

    def test_measurement_01(self):
        self.assertEqual(
            NLP('0.120–0.127 mm'),
            [{'low': 0.12, 'high': 0.127, 'length_units': 'mm',
              'trait': 'size', 'start': 0, 'end': 14}]
        )
