import unittest

from anoplura.rules.base import Link
from anoplura.rules.part import Part
from anoplura.rules.sexual_dimorphism import SexualDimorphism
from tests.setup import parse


class TestSexualDimorphism(unittest.TestCase):
    def test_sexual_dimorphism_01(self) -> None:
        self.assertEqual(
            parse("Head, thorax, and abdomen as in male"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(trait="sexual_dimorphism", start=26, end=36)],
                    part="head",
                ),
                Part(
                    start=6,
                    end=12,
                    links=[Link(trait="sexual_dimorphism", start=26, end=36)],
                    part="thorax",
                ),
                Part(
                    start=18,
                    end=25,
                    links=[Link(trait="sexual_dimorphism", start=26, end=36)],
                    part="abdomen",
                ),
                SexualDimorphism(
                    start=26, end=36, reference_sex="male", description="as in"
                ),
            ],
        )

    def test_sexual_dimorphism_02(self) -> None:
        self.assertEqual(
            parse("femora longer than in male"),
            [
                Part(
                    start=0,
                    end=6,
                    links=[Link(trait="sexual_dimorphism", start=7, end=26)],
                    part="femur",
                ),
                SexualDimorphism(
                    start=7, end=26, reference_sex="male", description="longer than in"
                ),
            ],
        )

    def test_sexual_dimorphism_03(self) -> None:
        self.assertEqual(
            parse("head similar to those of male"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(trait="sexual_dimorphism", start=5, end=29)],
                    part="head",
                ),
                SexualDimorphism(
                    start=5,
                    end=29,
                    reference_sex="male",
                    description="similar to those of",
                ),
            ],
        )
