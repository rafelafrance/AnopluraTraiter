import unittest

from anoplura.rules.gonopod import Gonopod
from anoplura.rules.group import Group
from anoplura.rules.part_seta import PartSeta
from anoplura.rules.position import Position
from tests.setup import parse


class TestPartSeta(unittest.TestCase):
    def test_part_seta_01(self):
        self.assertEqual(
            parse("1 seta inserted immediately lateral to gonopods IX on each side;"),
            [
                PartSeta(
                    start=0,
                    end=6,
                    part="gonopod",
                    which=[9],
                    seta="seta",
                    count_low=1,
                    group="on each side",
                    position="immediately lateral",
                ),
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
                    seta="seta",
                    count_low=3,
                    count_high=None,
                    count_group="rows of",
                    position="immediately anterior",
                    group="on each side",
                ),
                Position(start=16, end=36, position="immediately anterior"),
                Gonopod(start=40, end=51, part="gonopod", which=[9]),
                Group(start=52, end=64, group="on each side"),
            ],
        )
