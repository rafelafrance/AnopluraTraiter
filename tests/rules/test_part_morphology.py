import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_morphology import PartMorphology
from tests.setup import parse


class TestPartDescription(unittest.TestCase):
    def test_part_description_01(self):
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                PartMorphology(
                    start=0,
                    end=13,
                    part="coxa",
                    morphology=["subtriangular"],
                ),
                Part(
                    start=14,
                    end=19,
                    part="coxa",
                ),
            ],
        )

    def test_part_description_02(self):
        self.assertEqual(
            parse("Head longer than wide, broadly rounded anteriorly;"),
            [
                Part(
                    start=0,
                    end=4,
                    part="head",
                ),
                PartMorphology(
                    start=5,
                    end=49,
                    part="head",
                    morphology=["longer than wide", "broadly rounded anteriorly"],
                ),
            ],
        )

    def test_part_description_03(self):
        self.assertEqual(
            parse(
                """
                basal segment larger than other segments and slightly longer than wide;
                """
            ),
            [
                Part(
                    start=0,
                    end=13,
                    part="segment",
                    which="basal",
                ),
                PartMorphology(
                    start=14,
                    end=70,
                    part="segment",
                    which="basal",
                    morphology=[
                        "larger than other segments",
                        "slightly longer than wide",
                    ],
                ),
            ],
        )

    def test_part_description_04(self):
        self.assertEqual(
            parse(
                """
                basal segment larger than other segments and slightly longer than wide;
                """
            ),
            [
                Part(
                    start=0,
                    end=13,
                    part="segment",
                    which="basal",
                ),
                PartMorphology(
                    start=14,
                    end=70,
                    part="segment",
                    which="basal",
                    morphology=[
                        "larger than other segments",
                        "slightly longer than wide",
                    ],
                ),
            ],
        )

    def test_part_description_05(self):
        self.assertEqual(
            parse("Mesothoracic spiracle"),
            [
                PartMorphology(
                    start=0,
                    end=12,
                    part="spiracle",
                    morphology=["mesothoracic"],
                ),
                Part(
                    start=13,
                    end=21,
                    part="spiracle",
                ),
            ],
        )

    def test_part_description_06(self):
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                PartMorphology(
                    start=0,
                    end=13,
                    part="coxa",
                    morphology=["subtriangular"],
                ),
                Part(
                    start=14,
                    end=19,
                    part="coxa",
                ),
                PartMorphology(
                    start=20,
                    end=44,
                    part="claw",
                    morphology=["proximally and acuminate"],
                ),
                Part(
                    start=45,
                    end=50,
                    part="claw",
                ),
                PartMorphology(
                    start=51,
                    end=61,
                    part="claw",
                    morphology=["terminally"],
                ),
            ],
        )

    def test_part_description_07(self):
        self.assertEqual(
            parse("Legs progressively larger from anterior to posterior,"),
            [
                Part(
                    start=0,
                    end=4,
                    part="leg",
                ),
                PartMorphology(
                    start=5,
                    end=52,
                    part="leg",
                    morphology=["progressively larger", "from anterior to posterior"],
                ),
            ],
        )
