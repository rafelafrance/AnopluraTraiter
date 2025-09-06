import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from tests.setup import parse


class TestSetaCount(unittest.TestCase):
    def test_seta_count_01(self) -> None:
        self.assertEqual(
            parse("4 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    seta_part="abdomen",
                    count_low=4,
                    start=0,
                    end=1,
                ),
                Seta(
                    start=2,
                    end=6,
                    seta_part="abdomen",
                    seta="dorsal central abdominal setae",
                ),
            ],
        )

    def test_seta_count_02(self) -> None:
        self.assertEqual(
            parse("5 pairs of DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    seta_part="abdomen",
                    count_low=5,
                    count_group="pairs of",
                    start=0,
                    end=10,
                ),
                Seta(
                    start=11,
                    end=15,
                    seta="dorsal central abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )

    def test_seta_count_03(self) -> None:
        self.assertEqual(
            parse("6-7 DCAS,"),
            [
                SetaCount(
                    seta="dorsal central abdominal setae",
                    seta_part="abdomen",
                    count_low=6,
                    count_high=7,
                    start=0,
                    end=3,
                ),
                Seta(
                    start=4,
                    end=8,
                    seta="dorsal central abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )

    def test_seta_count_04(self) -> None:
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

    def test_seta_count_05(self) -> None:
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
                    seta_part="head",
                    count_low=3,
                    count_high=4,
                ),
                Seta(
                    start=7,
                    end=24,
                    seta="apical head setae",
                    seta_part="head",
                ),
                SetaCount(
                    seta="dorsal preantennal head setae",
                    seta_part="head",
                    count_low=1,
                    start=26,
                    end=27,
                ),
                Seta(
                    start=28,
                    end=56,
                    seta_part="head",
                    seta="dorsal preantennal head setae",
                ),
            ],
        )

    def test_seta_count_06(self) -> None:
        self.assertEqual(
            parse("1 short dorsal accessory head seta"),
            [
                SetaCount(
                    seta="dorsal accessory head setae",
                    seta_part="head",
                    description="short",
                    count_low=1,
                    start=0,
                    end=7,
                ),
                Seta(
                    start=8,
                    end=34,
                    seta="dorsal accessory head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_seta_count_07(self) -> None:
        self.assertEqual(
            parse("2 lateral StAS on each side"),
            [
                SetaCount(
                    start=0,
                    end=9,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=2,
                    description="lateral",
                ),
                Seta(
                    start=10,
                    end=14,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                ),
                SetaCount(
                    start=15,
                    end=27,
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                    count_low=2,
                ),
            ],
        )

    def test_seta_count_08(self) -> None:
        self.assertEqual(
            parse("1 fairly long ventral principal head seta"),
            [
                SetaCount(
                    seta="ventral principal head setae",
                    seta_part="head",
                    description="fairly long",
                    count_low=1,
                    start=0,
                    end=13,
                ),
                Seta(
                    start=14,
                    end=41,
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_seta_count_09(self) -> None:
        self.assertEqual(
            parse("1 (posterior row) setae"),
            [
                SetaCount(
                    start=0,
                    end=17,
                    seta="setae",
                    count_low=1,
                    description="posterior row",
                ),
                Seta(
                    start=18,
                    end=23,
                    seta="setae",
                ),
            ],
        )

    def test_seta_count_10(self) -> None:
        self.assertEqual(
            parse("setae (2 on 1 side, 3 on the other)"),
            [
                Seta(
                    start=0,
                    end=5,
                    seta="setae",
                ),
                SetaCount(
                    start=7,
                    end=18,
                    seta="setae",
                    count_low=2,
                    count_group="on 1 side",
                ),
                SetaCount(
                    start=20,
                    end=34,
                    seta="setae",
                    count_low=3,
                    count_group="on the other",
                ),
            ],
        )
