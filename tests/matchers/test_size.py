"""Test louse size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from src.pylib.pipeline import PIPELINE

NLP = PIPELINE.trait_list


class TestSize(unittest.TestCase):
    """Test louse size trait matcher."""

    def test_size_01(self):
        self.assertEqual(
            NLP('0.120–0.127 mm, mean 0.124 mm (n = 3)'),
            [{'n': 3, 'mean': 0.124, 'mean_units': 'mm',
              'low': 0.12, 'high': 0.127, 'length_units': 'mm',
              'trait': 'size', 'start': 0, 'end': 37}]
        )

    def test_size_02(self):
        self.assertEqual(
            NLP('length 0.137 mm (n = 1)'),
            [{'n': 1, 'low': 0.137, 'length_units': 'mm',
              'trait': 'size', 'start': 7, 'end': 23}]
        )
