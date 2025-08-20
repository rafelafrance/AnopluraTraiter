import unittest

from anoplura.rules.segment import Segment
from tests.setup import parse


class TestSegment(unittest.TestCase):
    def test_segment_01(self) -> None:
        self.assertEqual(
            parse("segment 2"),
            [Segment(which=[2], start=0, end=9)],
        )

    def test_segment_02(self) -> None:
        self.assertEqual(
            parse("segments 4-16"),
            [
                Segment(
                    which=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    start=0,
                    end=13,
                )
            ],
        )

    def test_segment_03(self) -> None:
        self.assertEqual(
            parse("first antennal segment"),
            [
                Segment(start=0, end=22, which="first antennal"),
            ],
        )
