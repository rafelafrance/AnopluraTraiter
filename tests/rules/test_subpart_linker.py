import unittest

from anoplura.rules.count import Count
from anoplura.rules.group_prefix import GroupPrefix
from anoplura.rules.rule import Link
from anoplura.rules.seta import Seta
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.subpart import Subpart
from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self) -> None:
        self.assertEqual(
            parse("Tergites 1, 2, and 17 each with 4 long TeAS;"),
            [
                Tergite(
                    start=0,
                    end=21,
                    part="tergite",
                    number=[1, 2, 17],
                ),
                GroupPrefix(start=22, end=31, group="each with"),
                Count(
                    start=32,
                    end=33,
                    links=[Link(trait="group_prefix", start=22, end=31)],
                    count_low=4,
                ),
                SizeDescription(start=34, end=38, size_description="long"),
                Seta(
                    start=39,
                    end=43,
                    links=[
                        Link(trait="size_description", start=34, end=38),
                        Link(trait="count", start=32, end=33),
                    ],
                    seta="tergal abdominal setae",
                    seta_part="abdomen",
                ),
            ],
        )

    def test_subpart_linker_02(self) -> None:
        self.assertEqual(
            parse("One small lobe with small seta,"),
            [
                Count(start=0, end=3, count_low=1),
                SizeDescription(start=4, end=9, size_description="small"),
                Subpart(
                    start=10,
                    end=14,
                    links=[
                        Link(trait="size_description", start=4, end=9),
                        Link(trait="count", start=0, end=3),
                    ],
                    subpart="lobe",
                ),
                SizeDescription(start=20, end=25, size_description="small"),
                Seta(
                    start=26,
                    end=30,
                    links=[
                        Link(trait="size_description", start=20, end=25),
                    ],
                    seta="setae",
                ),
            ],
        )
