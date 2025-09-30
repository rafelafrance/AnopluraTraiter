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
                Part(start=0, end=4, part="head"),
                Part(start=6, end=12, part="thorax"),
                Part(start=18, end=25, part="abdomen"),
                SexualDimorphism(
                    _trait="sexual_dimorphism",
                    _text="as in male",
                    start=26,
                    end=36,
                    sex=None,
                    links=[
                        Link(trait="part", start=0, end=4),
                        Link(trait="part", start=6, end=12),
                        Link(trait="part", start=18, end=25),
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
                Part(start=0, end=6, part="femur"),
                SexualDimorphism(
                    start=7,
                    end=26,
                    links=[Link(trait="part", start=0, end=6)],
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
