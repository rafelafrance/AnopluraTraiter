import unittest

from anoplura.rules.row import Row
from tests.setup import parse


class TestRow(unittest.TestCase):
    def test_row_01(self):
        self.assertEqual(
            parse("anterior row"),
            [
                Row(position="anterior", start=0, end=12),
            ],
        )
