import unittest

from anoplura.rules.base import Link
from anoplura.rules.count import Count
from anoplura.rules.description import Description
from anoplura.rules.gonopod import Gonopod
from anoplura.rules.part import Part
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from anoplura.rules.tergite import Tergite
from tests.setup import parse


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self) -> None:
        self.assertEqual(
            parse("1 small sternite on segment 1;"),
            [
                Count(start=0, end=1, count_low=1),
                Description(
                    start=2,
                    end=7,
                    description="small",
                ),
                Sternite(
                    start=8,
                    end=16,
                    links=[
                        Link(start=2, end=7, trait="description"),
                        Link(start=0, end=1, trait="count"),
                    ],
                    part="sternite",
                ),
                Segment(
                    start=20,
                    end=29,
                    links=[Link(start=8, end=16, trait="sternite")],
                    part="segment",
                    number=[1],
                ),
            ],
        )

    def test_part_linker_02(self) -> None:
        self.assertEqual(
            parse("2 narrow tergites on segment 7;"),
            [
                Count(start=0, end=1, count_low=2),
                Description(start=2, end=8, description="narrow"),
                Tergite(
                    start=9,
                    end=17,
                    links=[
                        Link(start=2, end=8, trait="description"),
                        Link(start=0, end=1, trait="count"),
                    ],
                    part="tergite",
                ),
                Segment(
                    start=21,
                    end=30,
                    links=[Link(start=9, end=17, trait="tergite")],
                    part="segment",
                    number=[7],
                ),
            ],
        )

    def test_part_linker_03(self) -> None:
        self.assertEqual(
            parse("TeAS on tergites 3-5;"),
            [
                Seta(
                    start=0, end=4, seta="tergal abdominal setae", seta_part="abdomen"
                ),
                Tergite(
                    start=8,
                    end=20,
                    links=[Link(start=0, end=4, trait="seta")],
                    part="tergite",
                    number=[3, 4, 5],
                ),
            ],
        )

    def test_part_linker_04(self) -> None:
        self.assertEqual(
            parse("Genitalia with basal apodeme about twice as long as parameres;"),
            [
                Part(
                    start=0,
                    end=9,
                    links=[Link(trait="subpart", start=15, end=28)],
                    part="genitalia",
                ),
                Subpart(
                    start=15,
                    end=28,
                    links=[Link(trait="description", start=29, end=51)],
                    subpart="basal apodeme",
                ),
                Description(start=29, end=51, description="about twice as long as"),
                Part(
                    start=52,
                    end=61,
                    links=[Link(trait="subpart", start=15, end=28)],
                    part="paramere",
                ),
            ],
        )

    def test_part_linker_05(self) -> None:
        self.assertEqual(
            parse("sternite ventrally on segment 1;"),
            [
                Sternite(
                    start=0,
                    end=8,
                    links=[
                        Link(start=9, end=18, trait="description"),
                    ],
                    part="sternite",
                ),
                Description(
                    start=9,
                    end=18,
                    description="ventrally",
                ),
                Segment(
                    start=22,
                    end=31,
                    links=[Link(start=0, end=8, trait="sternite")],
                    part="segment",
                    number=[1],
                ),
            ],
        )

    def test_part_linker_06(self) -> None:
        self.assertEqual(
            parse("Gonopods and vulvar fimbriae distinct;"),
            [
                Gonopod(start=0, end=8, part="gonopod"),
                Part(start=13, end=28, part="vulvar fimbriae"),
            ],
        )

    def test_part_linker_07(self) -> None:
        self.assertEqual(
            parse("setae present between gonopods IX."),
            [
                Seta(start=0, end=5, seta="setae"),
                Gonopod(
                    start=22,
                    end=33,
                    links=[Link(start=0, end=5, trait="setae")],
                    part="gonopod",
                    number=[9],
                ),
            ],
        )
