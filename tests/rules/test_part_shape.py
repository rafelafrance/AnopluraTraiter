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

    def test_part_shape_02(self):
        self.assertEqual(
            parse("Head slightly longer than wide, relatively blunt anteriorly"),
            [
                PartShape(
                    part="head",
                    part_shape="slightly longer than wide, relatively blunt",
                    part_shape_position="anteriorly",
                    start=0,
                    end=59,
                )
            ],
        )

    def test_part_shape_03(self):
        self.assertEqual(
            parse("Head longer than wide, broadly rounded anteriorly"),
            [
                PartShape(
                    part="head",
                    part_shape="longer than wide, broadly rounded",
                    part_shape_position="anteriorly",
                    start=0,
                    end=49,
                )
            ],
        )
