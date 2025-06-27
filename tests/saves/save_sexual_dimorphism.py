import unittest

from anoplura.rules.save.sexual_dimorphism import SexualDimorphism
from tests.setup import parse


class TestSexualDimorphism(unittest.TestCase):
    def test_sexual_dimorphism_01(self):
        self.assertEqual(
            parse("Head, thorax, and abdomen as in male"),
            [
                SexualDimorphism(
                    reference_sex="male",
                    parts=["head", "thorax", "abdomen"],
                    start=0,
                    end=36,
                ),
            ],
        )
