import unittest

from anoplura.rules.position import Position
from tests.setup import parse


class TestPosition(unittest.TestCase):
    def test_position_01(self):
        self.assertEqual(
            parse("inserted immediately lateral"),
            [
                Position(start=9, end=28, position="immediately lateral"),
            ],
        )
