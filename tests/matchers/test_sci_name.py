"""Test scientific name trait matcher."""

import unittest

from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestSciName(unittest.TestCase):
    """Test range trait matcher."""

    def test_sci_name_01(self):
        self.assertEqual(
            test_traits(shorten("""
                 females of L. claytoni sp. nov., .""")),
            [{'sci_name': 'l. claytoni', 'group': 'anoplura',
              'trait': 'sci_name', 'start': 11, 'end': 22}]
        )
