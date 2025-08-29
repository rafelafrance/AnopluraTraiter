import unittest

from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self) -> None:
        self.assertEqual(
            parse("dorsal head suture"),
            [
                Subpart(
                    subpart="suture",
                    part="head",
                    which="dorsal",
                    start=0,
                    end=18,
                ),
            ],
        )

    def test_subpart_02(self) -> None:
        self.assertEqual(
            parse("small posterior spur"),
            [
                Subpart(
                    subpart="spur", position="posterior", size="small", start=0, end=20
                ),
            ],
        )

    def test_subpart_03(self) -> None:
        self.assertEqual(
            parse("basal apodeme"),
            [
                Subpart(subpart="apodeme", position="basal", start=0, end=13),
            ],
        )
