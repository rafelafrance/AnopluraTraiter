import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_count_01(self):
        self.assertEqual(
            parse("4 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=4,
                    start=0,
                    end=1,
                ),
                Seta(start=2, end=6, seta="dorsal central abdominal setae"),
            ],
        )

    def test_seta_count_02(self):
        self.assertEqual(
            parse("5 pairs of DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=5,
                    count_group="pairs of",
                    start=0,
                    end=10,
                ),
                Seta(start=11, end=15, seta="dorsal central abdominal setae"),
            ],
        )

    def test_seta_count_03(self):
        self.assertEqual(
            parse("6-7 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    count_low=6,
                    count_high=7,
                    start=0,
                    end=3,
                ),
                Seta(start=4, end=8, seta="dorsal central abdominal setae"),
            ],
        )

    def test_seta_count_04(self):
        self.assertEqual(
            parse("1 seta"),
            [
                SetaCount(
                    seta="seta",
                    count_low=1,
                    start=0,
                    end=1,
                ),
                Seta(start=2, end=6, seta="seta"),
            ],
        )

    def test_seta_count_05(self):
        self.assertEqual(
            parse(
                """
                3 or 4 apical head setae, 1 dorsal preantennal head seta
                """
            ),
            [
                SetaCount(
                    start=0,
                    end=6,
                    seta="apical head setae",
                    count_low=3,
                    count_high=4,
                ),
                Seta(
                    start=7,
                    end=24,
                    seta="apical head setae",
                ),
                SetaCount(
                    seta="dorsal preantennal head seta",
                    count_low=1,
                    start=26,
                    end=27,
                ),
                Seta(start=28, end=56, seta="dorsal preantennal head seta"),
            ],
        )
