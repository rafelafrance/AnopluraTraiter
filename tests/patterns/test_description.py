"""Test description trait matcher."""

import unittest

from tests.setup import test_traits


class TestDescription(unittest.TestCase):
    """Test description trait matcher."""

    def test_description_01(self):
        self.assertEqual(
            test_traits("""
                Head: More heavily sclerotized along anterior margin; 
                longer than broad with squarish, slightly convex anterior margin.
                """),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'More heavily sclerotized along anterior margin',
              'body_part': 'head', 'trait': 'description', 'start': 6, 'end': 52}]
        )
