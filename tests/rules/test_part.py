import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_description import PartDescription
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger"),
            [
                Part(part="leg", start=0, end=4),
                PartDescription(
                    start=5, end=25, part="leg", shape="progressively larger"
                ),
            ],
        )

    def test_part_02(self) -> None:
        self.assertEqual(
            parse("Antennae 5-segmented"),
            [
                Part(
                    start=0,
                    end=8,
                    part="antenna",
                ),
                PartDescription(
                    start=9,
                    end=20,
                    morphology="5-segmented",
                    part="antenna",
                ),
            ],
        )

    def test_part_03(self) -> None:
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(
                    start=0,
                    end=4,
                    part="head",
                ),
                PartDescription(
                    start=5,
                    end=41,
                    shape="with anterolateral lobe on each side",
                    part="head",
                ),
            ],
        )
