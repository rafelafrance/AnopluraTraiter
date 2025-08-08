import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_description import PartDescription
from tests.setup import parse


class TestPartDescription(unittest.TestCase):
    def test_part_description_01(self):
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                PartDescription(
                    start=0,
                    end=13,
                    part="coxa",
                    shape=["subtriangular"],
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
                PartDescription(
                    start=5,
                    end=49,
                    part="head",
                    shape=["longer than wide", "broadly rounded anteriorly"],
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
                PartDescription(
                    start=14,
                    end=70,
                    part="segment",
                    which="basal",
                    shape=["larger than other segments", "slightly longer than wide"],
                ),
            ],
        )
