import unittest

from anoplura.rules.base_rule import Link
from anoplura.rules.count import Count
from anoplura.rules.tergite import Tergite
from tests.setup import parse, unlinked


class TestDeleteUnlinked(unittest.TestCase):
    def test_delete_unlinked_01(self) -> None:
        self.assertEqual(
            parse("1 word"),
            [],
        )

        self.assertEqual(
            unlinked("1 word"),
            [
                Count(start=0, end=1, count_low=1),
            ],
        )

    def test_delete_unlinked_02(self) -> None:
        self.assertEqual(
            parse("1 tergite"),
            [
                Count(start=0, end=1, count_low=1),
                Tergite(
                    start=2,
                    end=9,
                    part="tergite",
                    links=[Link(start=0, end=1, trait="count")],
                ),
            ],
        )

        self.assertEqual(
            unlinked("1 tergite"),
            [],
        )
