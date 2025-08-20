import unittest

from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestTergite(unittest.TestCase):
    def test_tergite_01(self) -> None:
        self.assertEqual(
            parse("Tergites 1, 2, and 17"),
            [Tergite(part="tergite", which=[1, 2, 17], start=0, end=21)],
        )

    def test_tergite_02(self) -> None:
        self.assertEqual(
            parse("tergites (nos. 1 and 2)"),
            [Tergite(part="tergite", which=[1, 2], start=0, end=23)],
        )
