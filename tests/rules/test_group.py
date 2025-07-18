import unittest

from anoplura.rules.gonopod import Gonopod
from anoplura.rules.group import Group
from tests.setup import parse


class TestGroup(unittest.TestCase):
    def test_group_01(self):
        self.assertEqual(
            parse("gonopods IX on each side"),
            [
                Gonopod(start=0, end=11, which=[9]),
                Group(group="on each side", start=12, end=24),
            ],
        )

    def test_group_02(self):
        self.assertEqual(
            parse("pairs of"),
            [
                Group(group="pairs of", start=0, end=8),
            ],
        )

    def test_group_03(self):
        self.assertEqual(
            parse("rows of junk on each side"),
            [
                Group(group="rows of", start=0, end=7),
                Group(group="on each side", start=13, end=25),
            ],
        )
