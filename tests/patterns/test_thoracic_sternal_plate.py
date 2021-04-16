"""Test sternal thoracic plate trait matcher."""

import unittest

from tests.setup import test_traits


class TestThoracicSternalPlate(unittest.TestCase):
    """Test range trait matcher."""

    def test_sternal_plate_01(self):
        self.assertEqual(
            test_traits("""
                Thoracic sternal plate subrectangular, about 3⫻ as wide as
                long; thorax rounded."""),
            [{'body_part': 'thoracic sternal plate',
              'trait': 'body_part', 'start': 0, 'end': 22,
              'description': 'subrectangular, about 3× as wide as long'},
              {'body_part': 'thorax',
               'trait': 'body_part', 'start': 65, 'end': 71,
               'description': 'rounded'}]
        )
