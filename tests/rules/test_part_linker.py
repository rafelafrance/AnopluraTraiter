import unittest

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

    def test_part_linker_02(self) -> None:
        self.assertEqual(
            parse("2 narrow tergites on segment 7;"),
            [
                Count(
                    start=0,
                    end=1,
                    links=[Tergite(start=9, end=17, part="tergite")],
                    count_low=2,
                ),
                Description(
                    start=2,
                    end=8,
                    links=[Tergite(start=9, end=17, part="tergite")],
                    description="narrow",
                ),
                Tergite(
                    start=9,
                    end=17,
                    links=[
                        Description(start=2, end=8, description="narrow"),
                        Count(start=0, end=1, count_low=2),
                        Segment(start=21, end=30, part="segment", number=[7]),
                    ],
                    part="tergite",
                ),
                Segment(
                    start=21,
                    end=30,
                    links=[Tergite(start=9, end=17, part="tergite")],
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
                    start=0,
                    end=4,
                    links=[Tergite(start=8, end=20, part="tergite", number=[3, 4, 5])],
                    seta="tergal abdominal setae",
                    seta_part="abdomen",
                ),
                Tergite(
                    start=8,
                    end=20,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="tergal abdominal setae",
                            seta_part="abdomen",
                        )
                    ],
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
                    links=[
                        Subpart(start=15, end=28, subpart="basal apodeme"),
                        Part(start=52, end=61, part="paramere"),
                    ],
                    part="genitalia",
                ),
                Subpart(
                    start=15,
                    end=28,
                    links=[
                        Description(
                            start=29, end=51, description="about twice as long as"
                        ),
                        Part(start=0, end=9, part="genitalia"),
                        Part(start=52, end=61, part="paramere"),
                    ],
                    subpart="basal apodeme",
                ),
                Description(
                    start=29,
                    end=51,
                    links=[Subpart(start=15, end=28, subpart="basal apodeme")],
                    description="about twice as long as",
                ),
                Part(
                    start=52,
                    end=61,
                    links=[
                        Part(start=0, end=9, part="genitalia"),
                        Subpart(start=15, end=28, subpart="basal apodeme"),
                    ],
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
                        Description(start=9, end=18, description="ventrally"),
                        Segment(start=22, end=31, part="segment", number=[1]),
                    ],
                    part="sternite",
                ),
                Description(
                    start=9,
                    end=18,
                    links=[Sternite(start=0, end=8, part="sternite")],
                    description="ventrally",
                ),
                Segment(
                    start=22,
                    end=31,
                    links=[Sternite(start=0, end=8, part="sternite")],
                    part="segment",
                    number=[1],
                ),
            ],
        )

    def test_part_linker_06(self) -> None:
        self.assertEqual(
            parse("Gonopods and vulvar fimbriae distinct;"),
            [
                Gonopod(
                    start=0,
                    end=8,
                    links=[Part(start=13, end=28, part="vulvar fimbriae")],
                    part="gonopod",
                ),
                Part(
                    start=13,
                    end=28,
                    links=[Gonopod(start=0, end=8, part="gonopod")],
                    part="vulvar fimbriae",
                ),
            ],
        )

    def test_part_linker_07(self) -> None:
        self.assertEqual(
            parse("setae present between gonopods IX."),
            [
                Seta(
                    start=0,
                    end=5,
                    links=[Gonopod(start=22, end=33, part="gonopod", number=[9])],
                    seta="setae",
                ),
                Gonopod(
                    start=22,
                    end=33,
                    links=[Seta(start=0, end=5, seta="setae")],
                    part="gonopod",
                    number=[9],
                ),
            ],
        )
