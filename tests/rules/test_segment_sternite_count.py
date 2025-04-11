import unittest

from anoplura.rules.segment_sternite_count import SegmentSterniteCount
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
