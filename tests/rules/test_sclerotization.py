import unittest

from anoplura.rules.part import Part
from anoplura.rules.sclerotization import Sclerotization
from tests.setup import parse


class TestSclerotized(unittest.TestCase):
    def test_sclerotized_01(self) -> None:
        self.assertEqual(
            parse("Head, thorax, and abdomen moderately sclerotized"),
            [
                Part(start=0, end=4, part="head"),
                Part(start=6, end=12, part="thorax"),
                Part(start=18, end=25, part="abdomen"),
                Sclerotization(
                    start=26,
                    end=48,
                    sclerotization="moderately sclerotized",
                ),
            ],
        )
