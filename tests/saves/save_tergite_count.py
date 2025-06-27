import unittest

from anoplura.rules.save.tergite_count import TergiteCount
from tests.setup import parse


class TestTergiteCount(unittest.TestCase):
    def test_tergite_count_01(self):
        self.assertEqual(
            parse("2 relatively broad tergites (nos. 1 and 2)"),
            [TergiteCount(tergite_count_low=2, tergites=[1, 2], start=0, end=42)],
        )
