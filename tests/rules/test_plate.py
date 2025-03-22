import unittest

from anoplura.rules.plate import Plate
from tests.setup import parse


class TestPlate(unittest.TestCase):
    def test_plate_01(self):
        self.assertEqual(
            parse("plate VII"),
            [Plate(plates=[7], start=0, end=9)],
        )

    def test_plate_02(self):
        self.assertEqual(
            parse("plates II-VI"),
            [
                Plate(
                    plates=[2, 3, 4, 5, 6],
                    start=0,
                    end=12,
                )
            ],
        )

    def test_plate_03(self):
        self.assertEqual(
            parse("Thoracic sternal plate"),
            [Plate(position="thoracic sternal", start=0, end=22)],
        )
