"""Test scientific name trait matcher."""

import unittest

from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestSciName(unittest.TestCase):
    """Test range trait matcher."""

    def qq_test_sci_name_01(self):
        self.assertEqual(
            test_traits(shorten("""
                 females of L. claytoni sp. nov., .""")),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'suboval', 'body_part': 'head',
              'trait': 'description', 'start': 5, 'end': 12},
             {'body_part': 'antenna', 'trait': 'body_part',
              'start': 14, 'end': 22},
             {'description': 'unmodified in males', 'body_part': 'antenna',
              'trait': 'description', 'start': 23, 'end': 42}]
        )
