import unittest

from anoplura.rules.sternite import Sternite
from tests.setup import parse


class TestSternite(unittest.TestCase):
    def test_sternite_01(self):
        self.assertEqual(
            parse("sternite 2"),
            [Sternite(part="sternite", which=[2], start=0, end=10)],
        )

    def test_sternite_02(self):
        self.assertEqual(
            parse("sternites 4-16"),
            [
                Sternite(
                    part="sternite",
                    which=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    start=0,
                    end=14,
                )
            ],
        )

    def test_sternite_03(self):
        self.assertEqual(
            parse("sternites (nos. 2 and 3)"),
            [
                Sternite(
                    part="sternite",
                    which=[2, 3],
                    start=0,
                    end=24,
                )
            ],
        )

    def test_sternite_04(self):
        self.assertEqual(
            parse("sternite (no. 4)"),
            [
                Sternite(
                    part="sternite",
                    which=[4],
                    start=0,
                    end=16,
                )
            ],
        )
