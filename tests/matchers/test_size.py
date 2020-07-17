"""Test louse size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from src.pylib.pipeline import parse


class TestSize(unittest.TestCase):
    """Test louse size trait matcher."""

    def test_size_01(self):
        self.assertEqual(
            parse('0.120–0.127 mm, mean 0.124 mm (n = 3)'),
            {'size': [{'start': 0, 'end': 37,
                       'low': 0.12, 'high': 0.127, 'units': 'mm',
                       'mean': 0.124, 'mean_units': 'mm',
                       'n': 3}]}
        )

    def test_size_02(self):
        self.assertEqual(
            parse('length 0.137 mm (n = 1)'),
            {'size': [{'n': 1, 'start': 7, 'end': 23,
                       'low': 0.137, 'units': 'mm'}]}
        )
