"""Test range trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from anoplura.pylib.pipeline import parse


class TestRange(unittest.TestCase):
    """Test range trait matcher."""

    def test_range_01(self):
        self.assertEqual(
            parse('0.120–0.127 mm'),
            {'size': [{'start': 0, 'end': 14,
                       'low': 0.12, 'high': 0.127, 'units': 'mm'}]}
        )
