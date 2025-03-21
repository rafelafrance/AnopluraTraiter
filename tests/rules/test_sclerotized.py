import unittest

from anoplura.rules.sclerotized import Sclerotized
from tests.setup import parse


class TestSclerotized(unittest.TestCase):
    def test_sclerotized_01(self):
        self.assertEqual(
            parse("Head, thorax, and abdomen moderately sclerotized"),
            [
                Sclerotized(
                    part=["head", "thorax", "abdomen"],
                    amount="moderately",
                    start=0,
                    end=48,
                )
            ],
        )
