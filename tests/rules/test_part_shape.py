import unittest

from anoplura.rules.part_shape import PartShape
from tests.setup import parse


class TestPartShape(unittest.TestCase):
    def test_part_shape_01(self):
        self.assertEqual(
            parse("subtriangular coxae proximally"),
            [
                PartShape(
                    part="coxa",
                    part_shape="subtriangular",
                    part_shape_position="proximally",
                    start=0,
                    end=30,
                )
            ],
        )
