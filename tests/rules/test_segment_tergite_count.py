import unittest

from anoplura.rules.segment_tergite_count import SegmentTergiteCount
from tests.setup import parse


class TestSegmentTergiteCount(unittest.TestCase):
    def test_segment_tergite_count_01(self):
        self.assertEqual(
            parse("2 relatively broad tergites (nos. 1 and 2) on segment 2"),
            [
                SegmentTergiteCount(
                    segments=[2],
                    tergites=[1, 2],
                    tergite_count_low=2,
                    start=0,
                    end=55,
                )
            ],
        )

    def test_segment_tergite_count_02(self):
        self.assertEqual(
            parse("3 narrow tergites on each of segments 3"),
            [
                SegmentTergiteCount(
                    segments=[3],
                    tergite_count_low=3,
                    segment_tergite_count_group="on each of",
                    start=0,
                    end=39,
                )
            ],
        )
