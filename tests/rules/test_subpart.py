import unittest

from anoplura.rules.part import Part
from anoplura.rules.position import Position
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [
                Position(
                    start=0, end=6, body_part="part", which="head", position="dorsal"
                ),
                Part(start=7, end=11, part="head"),
                Subpart(subpart="suture", start=12, end=18),
            ],
        )

    def test_subpart_02(self):
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(start=0, end=4, part="head"),
                Position(
                    start=10,
                    end=23,
                    body_part="subpart",
                    which="lobe",
                    position="anterolateral",
                ),
                Subpart(start=24, end=28, subpart="lobe"),
            ],
        )

    def test_subpart_03(self):
        self.assertEqual(
            parse("small posterior spur"),
            [
                Position(
                    start=6,
                    end=15,
                    body_part="subpart",
                    which="spur",
                    position="posterior",
                ),
                Subpart(subpart="spur", start=16, end=20),
            ],
        )
