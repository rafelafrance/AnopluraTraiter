import unittest

from anoplura.rules.sex_count import SexCount
from tests.setup import parse


class TestSexCount(unittest.TestCase):
    def test_sex_count_01(self) -> None:
        self.assertEqual(
            parse("(23♂, 28♀)"),
            [
                SexCount(sex="male", count_low=23, start=1, end=4),
                SexCount(sex="female", count_low=28, start=6, end=9),
            ],
        )
