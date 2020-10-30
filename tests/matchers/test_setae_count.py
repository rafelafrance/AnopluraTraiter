"""Test setae count trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestRSetaeCount(unittest.TestCase):
    """Test range trait matcher."""

    def test_setae_count_01(self):
        self.assertEqual(
            NLP(shorten("""One long Dorsal Principal Head Seta (DPHS)""")),
            [{'count': 1, 'body_part': 'seta',
              'seta': 'dorsal principal head seta',
              'trait': 'seta_count', 'start': 0, 'end': 42}]
        )

    def test_setae_count_02(self):
        self.assertEqual(
            NLP(shorten(""" no Dorsal Mesothoracic Setae (DMsS); """)),
            [{'count': 0, 'seta': 'dorsal mesothoracic setae',
              'body_part': 'seta',
              'trait': 'seta_count', 'start': 0, 'end': 35}]
        )

    def test_setae_count_03(self):
        self.assertEqual(
            NLP(shorten(""" with pair of long setae """)),
            [{'body_part': 'seta', 'count': 2, 'seta': 'setae',
              'trait': 'seta_count', 'start': 5, 'end': 23}]
        )

    def test_setae_count_04(self):
        self.assertEqual(
            NLP(shorten("""
                with 16–18 contiguous curved setae on each side;
                """)),
            [{'low': 16, 'high': 18, 'seta': 'setae', 'group': 'each side',
              'body_part': 'seta',
              'trait': 'seta_count', 'start': 5, 'end': 47}]
        )

    def test_setae_count_05(self):
        self.assertEqual(
            NLP(shorten("""
                One long and one tiny seta immediately posterior to
                """)),
            [{'seta': 'seta', 'count': 2, 'body_part': 'seta',
              'trait': 'seta_count', 'start': 0, 'end': 26}]
        )

    def test_setae_count_06(self):
        self.assertEqual(
            NLP(shorten("""
                next four spiracles each with tiny posterior seta only.
                """)),
            [{'body_part': 'seta', 'count': 4, 'seta': 'posterior seta',
              'trait': 'seta_count', 'start': 5,  'end': 49}]
        )
