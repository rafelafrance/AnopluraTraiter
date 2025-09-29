import unittest

from anoplura.rules.plate import Plate
from tests.setup import parse


class TestPlate(unittest.TestCase):
    def test_plate_01(self) -> None:
        self.assertEqual(
            parse("plate VII"),
            [Plate(part="plate", number=[7], start=0, end=9)],
        )

    def test_plate_02(self) -> None:
        self.assertEqual(
            parse("plates II-VI"),
            [Plate(part="plate", number=[2, 3, 4, 5, 6], start=0, end=12)],
        )

    def test_plate_03(self) -> None:
        self.assertEqual(
            parse("Thoracic sternal plate"),
            [
                Plate(part="thoracic sternal plate", start=0, end=22),
            ],
        )

    def test_plate_04(self) -> None:
        self.assertEqual(
            parse("plates VI and VII"),
            [Plate(part="plate", number=[6, 7], start=0, end=17)],
        )

    def test_plate_05(self) -> None:
        self.assertEqual(
            parse("paratergal plate I"),
            [
                Plate(part="paratergal plate", number=[1], start=0, end=18),
            ],
        )
