import unittest

from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.rule import Link
from anoplura.rules.sclerotization import Sclerotization
from tests.setup import parse


class TestSclerotized(unittest.TestCase):
    def test_sclerotized_01(self) -> None:
        self.assertEqual(
            parse("Head, thorax, and abdomen moderately sclerotized"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(trait="sclerotization", start=26, end=48)],
                    part="head",
                ),
                Part(
                    start=6,
                    end=12,
                    links=[Link(trait="sclerotization", start=26, end=48)],
                    part="thorax",
                ),
                Part(
                    start=18,
                    end=25,
                    links=[Link(trait="sclerotization", start=26, end=48)],
                    part="abdomen",
                ),
                Sclerotization(
                    start=26, end=48, sclerotization="moderately sclerotized"
                ),
            ],
        )

    def test_sclerotized_02(self) -> None:
        self.assertEqual(
            parse("Genitalia with well-sclerotized subgenital plate"),
            [
                Part(
                    start=0,
                    end=9,
                    links=[Link(trait="sclerotization", start=15, end=31)],
                    part="genitalia",
                ),
                Sclerotization(start=15, end=31, sclerotization="well-sclerotized"),
                Plate(
                    start=32,
                    end=48,
                    links=[Link(trait="sclerotization", start=15, end=31)],
                    part="subgenital plate",
                ),
            ],
        )
