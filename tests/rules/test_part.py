import unittest

from anoplura.rules.base import Link
from anoplura.rules.group import Group
from anoplura.rules.morphology import Morphology
from anoplura.rules.part import Part
from anoplura.rules.shape import Shape
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(start=5, end=25, trait="size_description")],
                    part="leg",
                ),
                SizeDescription(
                    start=5,
                    end=25,
                    size_description="progressively larger",
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
                    links=[Link(start=9, end=20, trait="morphology")],
                    part="antenna",
                ),
                Morphology(start=9, end=20, morphology="5-segmented"),
            ],
        )

    def test_part_03(self) -> None:
        self.assertEqual(
            parse("head with anterolateral lobe on each side"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(trait="subpart", start=10, end=28)],
                    part="head",
                ),
                Subpart(
                    start=10,
                    end=28,
                    links=[Link(trait="group", start=29, end=41)],
                    subpart="anterolateral lobe",
                ),
                Group(start=29, end=41, group="on each side"),
            ],
        )

    def test_part_04(self) -> None:
        self.assertEqual(
            parse("Mesothoracic spiracle"),
            [
                Part(start=0, end=21, part="mesothoracic spiracle"),
            ],
        )

    def test_part_05(self) -> None:
        self.assertEqual(
            parse("forelegs small with narrow acuminate claw;"),
            [
                Part(
                    start=0,
                    end=8,
                    links=[
                        Link(trait="size_description", start=9, end=14),
                        Link(trait="subpart", start=37, end=41),
                    ],
                    part="foreleg",
                ),
                SizeDescription(start=9, end=14, size_description="small"),
                Shape(start=20, end=36, shape="narrow acuminate"),
                Subpart(
                    start=37,
                    end=41,
                    links=[Link(trait="shape", start=20, end=36)],
                    subpart="claw",
                ),
            ],
        )
