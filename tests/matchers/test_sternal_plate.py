"""Test sternal thoracic plate trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestSternalPlate(unittest.TestCase):
    """Test range trait matcher."""

    def test_sternal_plate_01(self):
        self.assertEqual(
            NLP(shorten("""
                Thoracic sternal plate subrectangular, about 3⫻ as wide as
                long; 4 DLAS""")),
            [{'description': 'subrectangular, about 3× as wide as long',
              'trait': 'thoracic_sternal_plate', 'start': 0, 'end': 64}]
        )
