import unittest

from anoplura.rules.sexual_dimorphism import SexualDimorphism
from tests.setup import parse


class TestSetaPosition(unittest.TestCase):
    def test_seta_position_01(self):
        self.assertEqual(
            parse("Head, thorax, and abdomen as in male"),
            [
                SexualDimorphism(
                    reference_sex="male",
                    body_parts=["head", "thorax", "abdomen"],
                    start=0,
                    end=36,
                ),
            ],
        )
