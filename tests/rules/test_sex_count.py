import unittest

from anoplura.rules.sex_count import SexCount
from tests.setup import parse


class TestSubpartCount(unittest.TestCase):
    def test_subpart_count_01(self):
        self.assertEqual(
            parse("(23♂, 28♀)"),
            [
                SexCount(sex="male", sex_count=23, start=1, end=4),
                SexCount(sex="female", sex_count=28, start=6, end=9),
            ],
        )
