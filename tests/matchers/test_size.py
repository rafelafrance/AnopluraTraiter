"""Test louse size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from lice.matchers.matcher import Matcher

MATCHER = Matcher()


class TestSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_size_01(self):
        self.assertEqual(
            MATCHER.parse('DPTS length 0.120–0.127 mm, mean 0.124 mm (n = 3)'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 5, 'end': 26,
                            'low': 23.0,
                            'high': 34.0,
                            'width_units': 'mm'}]}
        )
