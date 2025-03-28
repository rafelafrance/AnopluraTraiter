import unittest

from anoplura.rules.sternite_count import SterniteCount
from tests.setup import parse


class TestSterniteCount(unittest.TestCase):
    def test_sternite_count_01(self):
        self.assertEqual(
            parse("3 long, narrow sternites"),
            [SterniteCount(sternite_count_low=3, start=0, end=24)],
        )
