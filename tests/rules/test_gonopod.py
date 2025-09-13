import unittest

from anoplura.rules.gonopod import Gonopod
from tests.setup import parse


class TestGonopod(unittest.TestCase):
    def test_gonopod_01(self) -> None:
        self.assertEqual(
            parse("gonopods IX"),
            [Gonopod(part="gonopod", number=[9], start=0, end=11)],
        )
