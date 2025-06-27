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
            [Plate(start=17, end=22)],
        )

    def test_plate_04(self):
        self.assertEqual(
            parse("plates VI and VII"),
            [Plate(plates=[6, 7], start=0, end=17)],
        )

    def test_plate_05(self):
        self.assertEqual(
            parse("paratergal plate I"),
            [Plate(plates=[1], start=11, end=18)],
        )
