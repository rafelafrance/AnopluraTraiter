"""Test range trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods
import unittest

from src.pylib.pipeline import PIPELINE

NLP = PIPELINE.trait_list


class TestRange(unittest.TestCase):
    """Test range trait matcher."""

    def test_range_01(self):
        self.assertEqual(
            NLP('0.120–0.127 mm'),
            [{'low': 0.12, 'high': 0.127, 'units': 'mm', 'trait': 'size',
              'start': 0, 'end': 14}]
        )
