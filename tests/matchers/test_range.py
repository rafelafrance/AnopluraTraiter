"""Test range trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from lice.matchers.matcher import Matcher

MATCHER = Matcher()


class TestRange(unittest.TestCase):
    """Test range trait matcher."""

    def test_range_01(self):
        self.assertEqual(
            MATCHER.parse('0.120–0.127 mm'),
            {'size': [{'start': 0, 'end': 14,
                       'low': 0.12, 'high': 0.127, 'units': 'mm'}]}
        )
