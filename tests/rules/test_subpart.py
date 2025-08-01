import unittest

from anoplura.rules.part import Part
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [
                Subpart(
                    subpart="suture",
                    part="head",
                    position="dorsal",
                    start=0,
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
                Subpart(
                    start=10,
                    end=41,
                    subpart="lobe",
                    part="head",
                    position="anterolateral",
                    group="on each side",
                ),
            ],
        )

    def test_subpart_03(self):
        self.assertEqual(
            parse("small posterior spur"),
            [
                Subpart(subpart="spur", position="posterior", start=6, end=20),
            ],
        )

    def test_subpart_04(self):
        self.assertEqual(
            parse("basal apodeme"),
            [
                Subpart(subpart="apodeme", position="basal", start=0, end=13),
            ],
        )

    def test_subpart_05(self):
        self.assertEqual(
            parse("Antennae 5-segmented"),
            [
                Part(
                    start=0,
                    end=8,
                    part="antenna",
                ),
                Subpart(
                    start=9,
                    end=20,
                    subpart="5-segmented",
                    part="antenna",
                ),
            ],
        )
