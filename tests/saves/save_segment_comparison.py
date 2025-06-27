import unittest

from anoplura.rules.save.segment_comparison import SegmentComparison
from tests.setup import parse


class TestSegmentComparison(unittest.TestCase):
    def test_segment_comparison_01(self):
        self.assertEqual(
            parse(
                "basal segment larger than other segments and slightly longer than wide"
            ),
            [
                SegmentComparison(
                    segment_position="basal",
                    segment_comparison="larger than other segments",
                    segment_shape="slightly longer than wide",
                    start=0,
                    end=70,
                )
            ],
        )
