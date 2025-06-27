import unittest

from anoplura.rules.save.part_sclerotization import PartSclerotization
from tests.setup import parse


class TestSclerotized(unittest.TestCase):
    def test_sclerotized_01(self):
        self.assertEqual(
            parse("Head, thorax, and abdomen moderately sclerotized"),
            [
                PartSclerotization(
                    part=["head", "thorax", "abdomen"],
                    amount_sclerotized="moderately",
                    start=0,
                    end=48,
                )
            ],
        )
