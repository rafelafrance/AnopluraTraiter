import unittest

from anoplura.rules.gonopod import Gonopod
from anoplura.rules.group import Group
from anoplura.rules.part_seta import PartSeta
from anoplura.rules.plate import Plate
from anoplura.rules.position import Position
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.sternite import Sternite
from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestPartSeta(unittest.TestCase):
    def test_part_seta_01(self):
        self.assertEqual(
            parse("1 seta inserted immediately lateral to gonopods IX on each side;"),
            [
                SetaCount(start=0, end=1, seta="seta", count_low=1),
                Seta(start=2, end=6, seta="seta"),
                Position(start=16, end=35, position="immediately lateral"),
                Gonopod(start=39, end=50, part="gonopod", which=[9]),
                Group(start=51, end=63, group="on each side"),
            ],
        )

    def test_part_seta_02(self):
        self.assertEqual(
            parse("3 rows of setae immediately anterior to gonopods IX on each side;"),
            [
                PartSeta(
                    start=0,
                    end=15,
                    part="gonopod",
                    which=[9],
                    seta="setae",
                    count_low=3,
                    count_group="rows of",
                    position="immediately anterior",
                    group="on each side",
                ),
                Position(
                    start=16,
                    end=36,
                    position="immediately anterior",
                ),
                Gonopod(
                    start=40,
                    end=51,
                    part="gonopod",
                    which=[9],
                ),
                Group(
                    start=52,
                    end=64,
                    group="on each side",
                ),
            ],
        )

    def test_part_seta_03(self):
        self.assertEqual(
            parse("plates VI and VII each with 2 long apical setae"),
            [
                Plate(start=0, end=17, part="plate", which=[6, 7]),
                PartSeta(
                    start=18,
                    end=29,
                    part="plate",
                    which=[6, 7],
                    seta="long apical setae",
                    count_low=2,
                    count_group="each with",
                ),
                Seta(start=30, end=47, seta="long apical setae"),
            ],
        )

    def test_part_seta_04(self):
        self.assertEqual(
            parse("sternites 4-10 each with 6-8 StAS"),
            [
                Sternite(
                    start=0,
                    end=14,
                    part="sternite",
                    which=[4, 5, 6, 7, 8, 9, 10],
                ),
                PartSeta(
                    start=15,
                    end=28,
                    part="sternite",
                    which=[4, 5, 6, 7, 8, 9, 10],
                    seta="sternal abdominal setae",
                    count_low=6,
                    count_high=8,
                    count_group="each with",
                ),
                Seta(
                    start=29,
                    end=33,
                    seta="sternal abdominal setae",
                ),
            ],
        )

    def test_part_seta_05(self):
        self.assertEqual(
            parse("sternite 1 lacking setae;"),
            [
                Sternite(
                    start=0,
                    end=10,
                    part="sternite",
                    which=[1],
                ),
                PartSeta(
                    start=11,
                    end=18,
                    part="sternite",
                    which=[1],
                    seta="setae",
                    count_low=0,
                ),
                Seta(
                    start=19,
                    end=24,
                    seta="setae",
                ),
            ],
        )

    def test_part_seta_06(self):
        self.assertEqual(
            parse(" (VLAS) lateral to sternite 10 on each side."),
            [
                PartSeta(
                    start=1,
                    end=5,
                    part="sternite",
                    which=[10],
                    seta="ventral lateral abdominal setae",
                    position="lateral",
                    group="on each side",
                ),
                Position(
                    start=7,
                    end=14,
                    position="lateral",
                ),
                Sternite(
                    start=18,
                    end=29,
                    part="sternite",
                    which=[10],
                ),
                Group(
                    start=30,
                    end=42,
                    group="on each side",
                ),
            ],
        )

    def test_part_seta_07(self):
        self.assertEqual(
            parse("tergites 3-6 each with 8-11 TeAS;"),
            [
                Tergite(
                    start=0,
                    end=12,
                    part="tergite",
                    which=[3, 4, 5, 6],
                ),
                PartSeta(
                    start=13,
                    end=27,
                    part="tergite",
                    which=[3, 4, 5, 6],
                    seta="tergal abdominal setae",
                    count_low=8,
                    count_high=11,
                    count_group="each with",
                ),
                Seta(
                    start=28,
                    end=32,
                    seta="tergal abdominal setae",
                ),
            ],
        )
