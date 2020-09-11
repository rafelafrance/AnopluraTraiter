"""Test sclerotized trait matcher."""

import unittest

from src.pylib.pipeline import PIPELINE
from traiter.pylib.util import shorten

NLP = PIPELINE.test_traits


class TestSclerotized(unittest.TestCase):
    """Test range trait matcher."""

    def test_sclerotized_01(self):
        self.assertEqual(
            NLP('Head, thorax, and abdomen lightly sclerotized.'),
            [{'part': ['head', 'thorax', 'abdomen'],
              'sclerotized': 'lightly',
              'trait': 'sclerotized_part', 'start': 0, 'end': 45}]
        )

    def test_sclerotized_02(self):
        self.assertEqual(
            NLP('Head: More heavily sclerotized along anterior margin;'),
            [{'part': 'head', 'sclerotized': 'heavily',
              'trait': 'sclerotized_part', 'start': 0, 'end': 30}]
        )

    def test_sclerotized_03(self):
        self.assertEqual(
            NLP(shorten("""
                Eight lightly sclerotized plates present on each side
                associated with abdominal segments II–IX.
                """)),
            [{'sclerotized': 'lightly', 'part': 'abdominal segments',
              'location': 'each side',
              'trait': 'sclerotized_part', 'start': 6, 'end': 88}]
        )

    def test_sclerotized_04(self):
        self.assertEqual(
            NLP(shorten("""
                Genitalia (Fig 9) with moderately sclerotised subgenital plate,
                """)),
            [{'part': 'genitalia', 'trait': 'body_part', 'start': 0, 'end': 9},
             {'sclerotized': 'moderately', 'part': 'subgenital plate',
              'trait': 'sclerotized_part', 'start': 23, 'end': 62}]
        )

    def test_sclerotized_05(self):
        self.assertEqual(
            NLP(shorten("""
                Postantennal head margins with heavily sclerotized
                """)),
            [{'sclerotized': 'heavily', 'part': 'postantennal head margins',
              'trait': 'sclerotized_part', 'start': 0, 'end': 50}]
        )
