import unittest

from anoplura.rules.base import Link
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self) -> None:
        self.assertEqual(
            parse("dorsal head suture"),
            [
                Subpart(subpart="dorsal head suture", start=0, end=18),
            ],
        )

    def test_subpart_02(self) -> None:
        self.assertEqual(
            parse("small posterior spur"),
            [
                SizeDescription(start=0, end=5, size_description="small"),
                Subpart(
                    start=6,
                    end=20,
                    links=[Link(trait="description", start=0, end=5)],
                    subpart="posterior spur",
                ),
            ],
        )

    def test_subpart_03(self) -> None:
        self.assertEqual(
            parse("basal apodeme"),
            [
                Subpart(subpart="basal apodeme", start=0, end=13),
            ],
        )
