import unittest

from anoplura.rules.seta_count import SetaCount
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_count_01(self):
        self.assertEqual(
            parse("1 DMHS"),
            [
                SetaCount(
                    seta="dorsal marginal head setae", seta_count_low=1, start=0, end=6
                ),
            ],
        )

    def test_setae_count_02(self):
        self.assertEqual(
            parse("no Dorsal Mesothoracic Setae;"),
            [
                SetaCount(
                    seta="dorsal mesothoracic setae",
                    seta_count_low=0,
                    start=0,
                    end=28,
                ),
            ],
        )

    def test_setae_count_03(self):
        self.assertEqual(
            parse("with pair of long setae"),
            [
                SetaCount(
                    seta="long setae",
                    seta_count_group="pair of",
                    seta_count_group_count=2,
                    start=5,
                    end=23,
                ),
            ],
        )

    def test_setae_count_04(self):
        self.assertEqual(
            parse("with 16–18 contiguous curved setae on each side;"),
            [
                SetaCount(
                    seta_count_low=16,
                    seta_count_high=18,
                    seta="contiguous curved setae",
                    seta_count_group="on each side",
                    seta_count_group_count=2,
                    start=5,
                    end=47,
                ),
            ],
        )

    def test_setae_count_05(self):
        self.assertEqual(
            parse("1 relatively short terminal seta on each side dorsally."),
            [
                SetaCount(
                    seta_count_low=1,
                    seta="short terminal seta",
                    seta_count_group="on each side",
                    seta_count_group_count=2,
                    start=0,
                    end=45,
                ),
            ],
        )

    def test_setae_count_06(self):
        self.assertEqual(
            parse("2 long apical setae."),
            [
                SetaCount(
                    seta_count_low=2,
                    seta="long apical setae",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_setae_count_07(self):
        self.assertEqual(
            parse("3 rows of setae"),
            [
                SetaCount(
                    seta="setae",
                    seta_count_group="rows of",
                    seta_count_group_count=3,
                    start=0,
                    end=15,
                ),
            ],
        )
