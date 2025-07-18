import unittest

from anoplura.rules.group import Group
from anoplura.rules.part import Part
from anoplura.rules.position import Position
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
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

    def test_subpart_02(self):
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(
                    start=0,
                    end=4,
                    part="head",
                ),
                Position(
                    start=10,
                    end=23,
                    position="anterolateral",
                ),
                Subpart(
                    start=24,
                    end=28,
                    subpart="lobe",
                    part="head",
                    position="anterolateral",
                    group="on each side",
                ),
                Group(
                    start=29,
                    end=41,
                    group="on each side",
                ),
            ],
        )

    def test_subpart_03(self):
        self.assertEqual(
            parse("small posterior spur"),
            [
                Position(start=6, end=15, position="posterior"),
                Subpart(subpart="spur", start=16, end=20),
            ],
        )
