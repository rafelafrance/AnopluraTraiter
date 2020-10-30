"""Test length trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestLength(unittest.TestCase):
    """Test length trait matcher."""

    def test_length_01(self):
        self.assertEqual(
            NLP('Total body length: 0.99–1.16 mm; mean, 1.09 mm (n = 4).'),
            [{'n': 4, 'mean': 1.09, 'mean_units': 'mm', 'body_part': 'body',
              'low': 0.99, 'high': 1.16, 'length_units': 'mm',
              'trait': 'total_length', 'start': 0, 'end': 54}]
        )

    def test_length_02(self):
        self.assertEqual(
            NLP(shorten("""
                DPTS length 0.137 mm (n = 1)
                (only one unbroken DPTS present).
                """)),
            [{'n': 1, 'low': 0.137, 'length_units': 'mm',
              'body_part': 'dorsal principal thoracic seta',
              'trait': 'length', 'start': 0, 'end': 28}]
        )
