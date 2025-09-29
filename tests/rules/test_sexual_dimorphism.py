import unittest

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
                    links=[
                        SexualDimorphism(
                            start=26, end=36, reference_sex="male", description="as in"
                        )
                    ],
                    part="head",
                ),
                Part(
                    start=6,
                    end=12,
                    links=[
                        SexualDimorphism(
                            start=26, end=36, reference_sex="male", description="as in"
                        )
                    ],
                    part="thorax",
                ),
                Part(
                    start=18,
                    end=25,
                    links=[
                        SexualDimorphism(
                            start=26, end=36, reference_sex="male", description="as in"
                        )
                    ],
                    part="abdomen",
                ),
                SexualDimorphism(
                    start=26,
                    end=36,
                    links=[
                        Part(start=0, end=4, part="head"),
                        Part(start=6, end=12, part="thorax"),
                        Part(start=18, end=25, part="abdomen"),
                    ],
                    reference_sex="male",
                    description="as in",
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
                    links=[
                        SexualDimorphism(
                            start=7,
                            end=26,
                            reference_sex="male",
                            description="longer than in",
                        )
                    ],
                    part="femur",
                ),
                SexualDimorphism(
                    start=7,
                    end=26,
                    links=[Part(start=0, end=6, part="femur")],
                    reference_sex="male",
                    description="longer than in",
                ),
            ],
        )

    def test_sexual_dimorphism_03(self) -> None:
        self.assertEqual(
            parse("similar to those of male"),
            [
                SexualDimorphism(
                    start=0,
                    end=24,
                    links=[],
                    reference_sex="male",
                    description="similar to those of",
                )
            ],
        )
