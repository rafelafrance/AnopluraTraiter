import unittest

from anoplura.rules.count import Count
from anoplura.rules.description import Description
from anoplura.rules.segment import Segment
from anoplura.rules.sternite import Sternite
from tests.setup import parse


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self) -> None:
        self.assertEqual(
            parse("1 small sternite on segment 1;"),
            [
                Count(
                    start=0,
                    end=1,
                    links=[Sternite(start=8, end=16, part="sternite")],
                    count_low=1,
                ),
                Description(
                    start=2,
                    end=7,
                    links=[Sternite(start=8, end=16, part="sternite")],
                    description="small",
                ),
                Sternite(
                    start=8,
                    end=16,
                    links=[
                        Description(start=2, end=7, description="small"),
                        Count(start=0, end=1, count_low=1),
                        Segment(start=20, end=29, part="segment", number=[1]),
                    ],
                    part="sternite",
                ),
                Segment(
                    start=20,
                    end=29,
                    links=[Sternite(start=8, end=16, part="sternite")],
                    part="segment",
                    number=[1],
                ),
            ],
        )
