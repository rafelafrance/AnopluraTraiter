import unittest

from anoplura.rules.save.segment_sternite_count import SegmentSterniteCount
from tests.setup import parse


class TestSegmentSterniteCount(unittest.TestCase):
    def test_segment_sternite_count_01(self):
        self.assertEqual(
            parse("1 small sternite ventrally on segment 1;"),
            [
                SegmentSterniteCount(
                    segments=[1],
                    sternite_count_low=1,
                    segment_sternite_count_position="ventrally",
                    start=0,
                    end=39,
                )
            ],
        )

    def test_segment_sternite_count_02(self):
        self.assertEqual(
            parse("2 sternites on each of segments 4-6;"),
            [
                SegmentSterniteCount(
                    segments=[4, 5, 6],
                    sternite_count_low=2,
                    segment_sternite_count_group="on each of",
                    start=0,
                    end=35,
                )
            ],
        )
