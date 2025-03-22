import unittest

from anoplura.rules.sternite import Sternite
from tests.setup import parse


class TestSternite(unittest.TestCase):
    def test_sternite_01(self):
        self.assertEqual(
            parse("sternite 2"),
            [Sternite(sternites=[2], start=0, end=10)],
        )

    def test_sternite_02(self):
        self.assertEqual(
            parse("sternites 4-16"),
            [
                Sternite(
                    sternites=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    start=0,
                    end=14,
                )
            ],
        )
