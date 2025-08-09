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
                    part="abdomen",
                    count_low=4,
                    start=0,
                    end=1,
                ),
                Seta(
                    start=2,
                    end=6,
                    part="abdomen",
                    seta="dorsal central abdominal setae",
                ),
            ],
        )

    def test_seta_count_02(self):
        self.assertEqual(
            parse("5 pairs of DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    part="abdomen",
                    count_low=5,
                    count_group="pairs of",
                    start=0,
                    end=10,
                ),
                Seta(
                    start=11,
                    end=15,
                    seta="dorsal central abdominal setae",
                    part="abdomen",
                ),
            ],
        )

    def test_seta_count_03(self):
        self.assertEqual(
            parse("6-7 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    part="abdomen",
                    count_low=6,
                    count_high=7,
                    start=0,
                    end=3,
                ),
                Seta(
                    start=4,
                    end=8,
                    seta="dorsal central abdominal setae",
                    part="abdomen",
                ),
            ],
        )

    def test_seta_count_04(self):
        self.assertEqual(
            parse("1 seta"),
            [
                SetaCount(
                    seta="setae",
                    count_low=1,
                    start=0,
                    end=1,
                ),
                Seta(start=2, end=6, seta="setae"),
            ],
        )

    def test_seta_count_05(self):
        self.maxDiff = None
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
                    part="head",
                    count_low=3,
                    count_high=4,
                ),
                Seta(
                    start=7,
                    end=24,
                    seta="apical head setae",
                    part="head",
                ),
                SetaCount(
                    seta="dorsal preantennal head setae",
                    part="head",
                    count_low=1,
                    start=26,
                    end=27,
                ),
                Seta(
                    start=28, end=56, part="head", seta="dorsal preantennal head setae"
                ),
            ],
        )

    def test_seta_count_06(self):
        self.assertEqual(
            parse("1 short dorsal accessory head seta"),
            [
                SetaCount(
                    seta="dorsal accessory head setae",
                    part="head",
                    description="short",
                    count_low=1,
                    start=0,
                    end=7,
                ),
                Seta(start=8, end=34, seta="dorsal accessory head setae", part="head"),
            ],
        )

    def test_seta_count_07(self):
        self.maxDiff = None
        self.assertEqual(
            parse("2 lateral StAS on each side"),
            [
                SetaCount(
                    start=0,
                    end=9,
                    seta="sternal abdominal setae",
                    part="abdomen",
                    count_low=2,
                    description="lateral",
                ),
                Seta(
                    start=10,
                    end=14,
                    seta="sternal abdominal setae",
                    part="abdomen",
                ),
                SetaCount(
                    start=15,
                    end=27,
                    seta="sternal abdominal setae",
                    part="abdomen",
                    count_low=2,
                    description="on each side",
                ),
            ],
        )

    def test_seta_count_08(self):
        self.maxDiff = None
        self.assertEqual(
            parse("1 fairly long ventral principal head seta"),
            [
                SetaCount(
                    seta="ventral principal head setae",
                    part="head",
                    description="fairly long",
                    count_low=1,
                    start=0,
                    end=13,
                ),
                Seta(
                    start=14, end=41, seta="ventral principal head setae", part="head"
                ),
            ],
        )
