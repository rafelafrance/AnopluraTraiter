"""Test max body width trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestMaxWidth(unittest.TestCase):
    """Test louse size trait matcher."""

    def test_max_width_01(self):
        self.assertEqual(
            test_traits(
                'Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4).'),
            [{'n': 4, 'mean': 0.17, 'mean_units': 'mm',
              'low': 0.150, 'high': 0.163, 'length_units': 'mm',
              'part': 'head', 'trait': 'max_width', 'start': 0, 'end': 57}]
        )

    def test_length_02(self):
        self.assertEqual(
            test_traits(shorten("""
                Maximum thorax width, 0.193–0.228 mm (mean, 0.210, n = 4).
                """)),
            [{'part': 'thorax', 'n': 4, 'mean': 0.21, 'low': 0.193, 'high': 0.228,
              'length_units': 'mm', 'trait': 'max_width', 'start': 0, 'end': 57}]
        )
