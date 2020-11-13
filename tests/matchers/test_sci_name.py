"""Test scientific name trait matcher."""

import unittest

from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestSciName(unittest.TestCase):
    """Test range trait matcher."""

    def test_sci_name_01(self):
        self.assertEqual(
            test_traits(shorten("""
                 females of L. CLAYTONI sp. nov., .""")),
            [{'sci_name': 'L. claytoni', 'group': 'anoplura',
              'trait': 'sci_name', 'start': 11, 'end': 22}]
        )

    def test_sci_name_02(self):
        self.assertEqual(
            test_traits(shorten("""
                 four known species of Abrocomaphthirus""")),
            [{'genus': 'Abrocomaphthirus', 'group': 'anoplura',
              'trait': 'genus', 'start': 22, 'end': 38}]
        )
