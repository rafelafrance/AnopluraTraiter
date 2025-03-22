import unittest

from anoplura.rules.segment import Segment
from tests.setup import parse


class TestSegment(unittest.TestCase):
    def test_segment_01(self):
        self.assertEqual(
            parse("segment 2"),
            [Segment(segments=[2], start=0, end=9)],
        )

    def test_segment_02(self):
        self.assertEqual(
            parse("segments 4-16"),
            [
                Segment(
                    segments=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    start=0,
                    end=13,
                )
            ],
        )
