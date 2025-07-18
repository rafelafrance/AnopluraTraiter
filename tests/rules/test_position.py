import unittest

from anoplura.rules.part import Part
from anoplura.rules.position import Position
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestPosition(unittest.TestCase):
    def test_position_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [
                Position(start=0, end=6, position="dorsal"),
                Part(start=7, end=11, part="head"),
                Subpart(
                    subpart="suture",
                    part="head",
                    position="dorsal",
                    start=12,
                    end=18,
                ),
            ],
        )

    def test_position_02(self):
        self.assertEqual(
            parse("inserted immediately lateral"),
            [
                Position(start=9, end=28, position="immediately lateral"),
            ],
        )
