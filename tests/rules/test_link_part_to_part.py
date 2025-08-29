import unittest

from anoplura.rules.part_count import PartCount
from anoplura.rules.segment import Segment
from anoplura.rules.sternite import Sternite
from tests.setup import parse


class TestLinkPart(unittest.TestCase):
    def test_link_part_to_part_01(self) -> None:
        self.assertEqual(
            parse("1 small sternite on segment 1"),
            [
                PartCount(
                    start=0,
                    end=7,
                    part="sternite",
                    count_low=1,
                    description="small",
                ),
                Sternite(
                    start=8,
                    end=16,
                    part="sternite",
                    reference_part="segment",
                    reference_which=[1],
                ),
                Segment(
                    start=20,
                    end=29,
                    part="segment",
                    which=[1],
                ),
            ],
        )
