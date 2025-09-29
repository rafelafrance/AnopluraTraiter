import unittest

from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
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
                    links=[
                        Sclerotization(
                            start=26, end=48, sclerotization="moderately sclerotized"
                        ),
                        Part(start=6, end=12, part="thorax"),
                        Part(start=18, end=25, part="abdomen"),
                    ],
                    part="head",
                ),
                Part(
                    start=6,
                    end=12,
                    links=[
                        Sclerotization(
                            start=26, end=48, sclerotization="moderately sclerotized"
                        ),
                        Part(start=0, end=4, part="head"),
                        Part(start=18, end=25, part="abdomen"),
                    ],
                    part="thorax",
                ),
                Part(
                    start=18,
                    end=25,
                    links=[
                        Sclerotization(
                            start=26, end=48, sclerotization="moderately sclerotized"
                        ),
                        Part(start=0, end=4, part="head"),
                        Part(start=6, end=12, part="thorax"),
                    ],
                    part="abdomen",
                ),
                Sclerotization(
                    start=26,
                    end=48,
                    links=[
                        Part(start=0, end=4, part="head"),
                        Part(start=6, end=12, part="thorax"),
                        Part(start=18, end=25, part="abdomen"),
                    ],
                    sclerotization="moderately sclerotized",
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
                    links=[
                        Sclerotization(
                            start=15, end=31, sclerotization="well-sclerotized"
                        )
                    ],
                    part="genitalia",
                ),
                Sclerotization(
                    start=15,
                    end=31,
                    links=[
                        Part(start=0, end=9, part="genitalia"),
                        Plate(start=32, end=48, part="subgenital plate"),
                    ],
                    sclerotization="well-sclerotized",
                ),
                Plate(
                    start=32,
                    end=48,
                    links=[
                        Sclerotization(
                            start=15,
                            end=31,
                            links=None,
                            sclerotization="well-sclerotized",
                        )
                    ],
                    part="subgenital plate",
                ),
            ],
        )
