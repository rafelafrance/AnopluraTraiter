"""Test max body width trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMaxWidth(unittest.TestCase):
    """Test louse size trait matcher."""

    def test_max_width_01(self):
        self.assertEqual(
            NLP('Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4).'),
            [{'n': 4, 'mean': 1.09, 'mean_units': 'mm',
              'low': 0.99, 'high': 1.16, 'length_units': 'mm',
              'trait': 'body_length', 'start': 0, 'end': 54}]
        )
