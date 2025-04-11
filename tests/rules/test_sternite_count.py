import unittest

from anoplura.rules.sternite_count import SterniteCount
from tests.setup import parse


class TestSterniteCount(unittest.TestCase):
    def test_sternite_count_01(self):
        self.assertEqual(
            parse("3 long, narrow sternites"),
            [SterniteCount(sternite_count_low=3, start=0, end=24)],
        )

    def test_sternite_count_02(self):
        self.assertEqual(
            parse("2 elongate sternites (nos. 2 and 3)"),
            [SterniteCount(sternite_count_low=2, sternites=[2, 3], start=0, end=35)],
        )
