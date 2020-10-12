"""Test sclerotized trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestSclerotized(unittest.TestCase):
    """Test range trait matcher."""

    def test_sclerotized_01(self):
        self.assertEqual(
            NLP('Head, thorax, and abdomen lightly sclerotized.'),
            [{'body_part': ['head', 'thorax', 'abdomen'],
              'trait': 'body_part', 'start': 0, 'end': 25},
             {'description': 'lightly sclerotized',
              'body_part': ['head', 'thorax', 'abdomen'],
              'trait': 'description', 'start': 26, 'end': 45}]
        )

    def test_sclerotized_02(self):
        self.assertEqual(
            NLP('Head: More heavily sclerotized along anterior margin;'),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'More heavily sclerotized along anterior margin',
              'body_part': 'head', 'trait': 'description',
              'start': 6, 'end': 52}]
        )

    def test_sclerotized_03(self):
        self.assertEqual(
            NLP(shorten("""
                Eight lightly sclerotized plates present on each side
                associated with abdominal segments II–IX.
                """)),
            [{'description': 'Eight lightly sclerotized plates present on '
                             'each side associated with',
              'body_part': 'abdominal', 'trait': 'description',
              'start': 0, 'end': 69},
             {'body_part': 'abdominal', 'trait': 'body_part',
              'start': 70, 'end': 79},
             {'description': 'segments II–IX',
              'body_part': 'abdominal', 'trait': 'description',
              'start': 80, 'end': 94}]
        )

    def test_sclerotized_04(self):
        self.assertEqual(
            NLP(shorten("""
                Genitalia (Fig 9) with moderately sclerotised subgenital plate,
                """)),
            [{'body_part': 'genitalia', 'trait': 'body_part',
              'start': 0, 'end': 9},
             {'body_part': ['subgenital', 'plate'],
              'trait': 'body_part', 'start': 46, 'end': 62}]
        )

    def test_sclerotized_05(self):
        self.assertEqual(
            NLP(shorten("""
                Postantennal head margins with heavily sclerotized
                """)),
            [{'body_part': ['postantennal', 'head', 'margins'],
              'trait': 'body_part', 'start': 0, 'end': 25},
             {'description': 'with heavily sclerotized',
              'body_part': ['postantennal', 'head', 'margins'],
              'trait': 'description',
              'start': 26,
              'end': 50}]
        )
