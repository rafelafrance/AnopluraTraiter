import unittest

from anoplura.rules.part import Part
from anoplura.rules.part_shape import PartShape
from tests.setup import parse


class TestPartShape(unittest.TestCase):
    def test_part_shape_01(self):
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                PartShape(
                    start=0,
                    end=13,
                    part="coxa",
                    shape="subtriangular",
                ),
                Part(
                    start=14,
                    end=19,
                    part="coxa",
                ),
            ],
        )
