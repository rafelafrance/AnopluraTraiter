"""Test body part trait matcher."""

import unittest

from tests.setup import test_traits


class TestBodyPart(unittest.TestCase):
    """Test body part trait matcher."""

    def test_body_part_01(self):
        self.assertEqual(
            test_traits('fourth segment'),
            [{'body_part': 'fourth segment',
              'trait': 'body_part', 'start': 0, 'end': 14}]
        )
