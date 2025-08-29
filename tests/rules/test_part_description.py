import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_description import PartDescription
from anoplura.rules.plate import Plate
from anoplura.rules.segment import Segment
from tests.setup import parse


class TestPartDescription(unittest.TestCase):
    def test_part_description_01(self) -> None:
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                PartDescription(
                    start=0,
                    end=13,
                    part="coxa",
                    shape="subtriangular",
                ),
                Part(
                    start=14,
                    end=19,
                    part="coxa",
                ),
            ],
        )

    def test_part_description_02(self) -> None:
        self.assertEqual(
            parse("Head longer than wide, broadly rounded anteriorly;"),
            [
                Part(
                    start=0,
                    end=4,
                    part="head",
                ),
                PartDescription(
                    start=5,
                    end=49,
                    part="head",
                    shape="longer than wide, broadly rounded anteriorly",
                ),
            ],
        )

    def test_part_description_03(self) -> None:
        self.assertEqual(
            parse(
                """
                basal segment larger than other segments and slightly longer than wide;
                """
            ),
            [
                Segment(
                    start=0,
                    end=13,
                    part="segment",
                    which="basal",
                ),
                PartDescription(
                    start=14,
                    end=70,
                    part="segment",
                    which="basal",
                    shape="larger than other segments and slightly longer than wide",
                ),
            ],
        )

    def test_part_description_04(self) -> None:
        self.assertEqual(
            parse("Mesothoracic spiracle"),
            [
                Part(
                    start=0,
                    end=21,
                    part="spiracle",
                    which="mesothoracic",
                ),
            ],
        )

    def test_part_description_05(self) -> None:
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                PartDescription(
                    start=0,
                    end=13,
                    part="coxa",
                    shape="subtriangular",
                ),
                Part(
                    start=14,
                    end=19,
                    part="coxa",
                ),
                PartDescription(
                    start=20,
                    end=61,
                    part="coxa",
                    shape="proximally and acuminate claws terminally",
                ),
            ],
        )

    def test_part_description_06(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger from anterior to posterior,"),
            [
                Part(
                    start=0,
                    end=4,
                    part="leg",
                ),
                PartDescription(
                    start=5,
                    end=53,
                    part="leg",
                    shape="progressively larger from anterior to posterior",
                ),
            ],
        )

    def test_part_description_07(self) -> None:
        self.maxDiff = None
        self.assertEqual(
            parse("Abdomen wider than thorax."),
            [
                Part(
                    start=0,
                    end=7,
                    part="abdomen",
                ),
                PartDescription(
                    start=8,
                    end=18,
                    part="abdomen",
                    shape="wider than",
                    reference_part="thorax",
                ),
                Part(
                    start=19,
                    end=25,
                    part="thorax",
                ),
            ],
        )

    def test_part_description_08(self) -> None:
        self.assertEqual(
            parse("""Thoracic sternal plate club-shaped with rounded anterolateral
                margins, broadly acuminate anterior apex, and elongate posterior
                extension with squarish posterior apex,"""),
            [
                Plate(start=0, end=22, part="plate", position="thoracic sternal"),
                PartDescription(
                    start=23,
                    end=166,
                    part="plate",
                    shape=(
                        "club-shaped with rounded anterolateral margins, broadly "
                        "acuminate anterior apex, and elongate posterior extension "
                        "with squarish posterior apex"
                    ),
                ),
            ],
        )

    def test_part_description_09(self) -> None:
        self.assertEqual(
            parse("""hind femora with relatively broad spur-like ridge posteriorly"""),
            [
                Part(start=0, end=11, part="femur", which="hind"),
                PartDescription(
                    start=12,
                    end=61,
                    part="femur",
                    which="hind",
                    shape="with relatively broad spur-like ridge posteriorly",
                ),
            ],
        )
