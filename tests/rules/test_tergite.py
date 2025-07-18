import unittest

from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestTergite(unittest.TestCase):
    def test_tergite_01(self):
        self.assertEqual(
            parse("Tergites 1, 2, and 17"),
            [Tergite(part="tergite", which=[1, 2, 17], start=0, end=21)],
        )
