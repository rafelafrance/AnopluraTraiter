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
            [{'n': 4, 'mean': 0.17, 'mean_units': 'mm',
              'low': 0.150, 'high': 0.163, 'length_units': 'mm',
              'part': 'head', 'trait': 'max_width', 'start': 0, 'end': 57}]
        )
