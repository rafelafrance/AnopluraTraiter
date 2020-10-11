"""Test sternal thoracic plate trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestThoracicSternalPlate(unittest.TestCase):
    """Test range trait matcher."""

    def test_sternal_plate_01(self):
        self.assertEqual(
            NLP(shorten("""
                Thoracic sternal plate subrectangular, about 3⫻ as wide as
                long; thorax rounded.""")),
            [{'body_part': 'thoracic sternal plate',
              'trait': 'body_part', 'start': 0, 'end': 22},
             {'description': 'subrectangular',
              'body_part': 'thoracic sternal plate',
              'trait': 'description', 'start': 23, 'end': 37},
             {'description': 'about 3× as wide as long',
              'body_part': 'thoracic sternal plate',
              'trait': 'description', 'start': 39, 'end': 63},
             {'body_part': 'thorax',
              'trait': 'body_part', 'start': 65, 'end': 71},
             {'description': 'rounded', 'body_part': 'thorax',
              'trait': 'description', 'start': 72, 'end': 79}]
        )
