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
                    part="head",
                ),
                Part(
                    start=6,
                    end=12,
                    part="thorax",
                ),
                Part(
                    start=18,
                    end=25,
                    part="abdomen",
                ),
                SexualDimorphism(
                    reference_sex="male",
                    parts=["head", "thorax", "abdomen"],
                    description="as in",
                    start=26,
                    end=36,
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
                    part="femur",
                ),
                SexualDimorphism(
                    reference_sex="male",
                    parts=["femur"],
                    description="longer than in",
                    start=7,
                    end=26,
                ),
            ],
        )

    def test_sexual_dimorphism_03(self) -> None:
        self.assertEqual(
            parse("similar to those of male"),
            [
                SexualDimorphism(
                    reference_sex="male",
                    parts=[],
                    description="similar to those of",
                    start=0,
                    end=24,
                ),
            ],
        )
