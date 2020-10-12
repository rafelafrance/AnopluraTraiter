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
            [{'count': 1, 'setae': 'setae',
              'type': 'dorsal principal head',
              'trait': 'setae_count', 'start': 0, 'end': 42}]
        )

    def test_setae_count_02(self):
        self.assertEqual(
            NLP(shorten(""" no Dorsal Mesothoracic Setae (DMsS); """)),
            [{'count': 0, 'type': 'dorsal mesothoracic', 'setae': 'setae',
              'trait': 'setae_count', 'start': 0, 'end': 35}]
        )

    def test_setae_count_03(self):
        self.assertEqual(
            NLP(shorten(""" with pair of long setae """)),
            [{'count': 2, 'setae': 'setae',
              'trait': 'setae_count', 'start': 5, 'end': 23}]
        )

    def test_setae_count_04(self):
        self.assertEqual(
            NLP(shorten("""
                with 16–18 contiguous curved setae on each side;
                """)),
            [{'low': 16, 'high': 18, 'setae': 'setae', 'group': 'each side',
              'trait': 'setae_count', 'start': 5, 'end': 47}]
        )

    def test_setae_count_05(self):
        self.assertEqual(
            NLP(shorten("""
                One long and one tiny seta immediately posterior to
                """)),
            [{'setae': 'seta', 'count': 2,
              'trait': 'setae_count', 'start': 0, 'end': 26}]
        )

    def test_setae_count_06(self):
        self.assertEqual(
            NLP(shorten("""
                next four spiracles each with tiny posterior seta only.
                """)),
            [{'type': 'posterior', 'setae': 'seta', 'present': True,
              'trait': 'setae_count', 'start': 35, 'end': 49}]
        )
