"""Test setae count trait matcher."""

import unittest

from src.pylib.pipeline import PIPELINE
from traiter.pylib.util import shorten

NLP = PIPELINE.test_traits


class TestRSetaeCount(unittest.TestCase):
    """Test range trait matcher."""

    def test_setae_count_01(self):
        self.assertEqual(
            NLP(shorten("""
                 One long Dorsal Principal Head Seta (DPHS),
                 one small Dorsal Accessory Head Seta (DAcHS)
                 anteromedial to DPHS,
                 one Dorsal Posterior Central Head Seta (DPoCHS),
                 two to three Dorsal Preantennal Head Setae (DPaHS),
                 two Sutural Head Setae (SHS),
                 three Dorsal Marginal Head Setae (DMHS),
                 three to four Apical Head Setae (ApHS),
                 and one fairly large Ventral Preantennal Head Seta (VPaHS).
                 """)),
            [{'count': 1, 'type': 'dorsal principal head', 'setae': 'setae',
              'trait': 'setae_count', 'start': 0, 'end': 42},
             {'count': 1, 'type': 'dorsal accessory head',
              'setae': 'setae',
              'trait': 'setae_count', 'start': 44, 'end': 88},
             {'count': 1, 'type': 'dorsal posterior central head',
              'setae': 'setae',
              'trait': 'setae_count', 'start': 111, 'end': 158},
             {'low': 2, 'high': 3, 'type': 'dorsal preantennal head',
              'setae': 'setae',
              'trait': 'setae_count', 'start': 160, 'end': 210},
             {'count': 2, 'type': 'sutural head', 'setae': 'setae',
              'trait': 'setae_count', 'start': 212, 'end': 240},
             {'count': 3, 'type': 'dorsal marginal head', 'setae': 'setae',
              'trait': 'setae_count', 'start': 242, 'end': 281},
             {'low': 3, 'high': 4, 'type': 'apical head', 'setae': 'setae',
              'trait': 'setae_count', 'start': 283, 'end': 321},
             {'count': 1, 'type': 'ventral preantennal head', 'setae': 'setae',
              'trait': 'setae_count', 'start': 327, 'end': 381}]
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
