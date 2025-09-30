import unittest

from anoplura.rules.base import Link
from anoplura.rules.count import Count
from anoplura.rules.description import Description
from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestDescription(unittest.TestCase):
    def test_description_01(self) -> None:
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                Description(start=0, end=13, description="subtriangular"),
                Part(
                    start=14,
                    end=19,
                    links=[Link(start=0, end=13, trait="description")],
                    part="coxa",
                ),
            ],
        )

    def test_description_02(self) -> None:
        self.assertEqual(
            parse(
                """
                basal segment larger than other segments and slightly longer than wide;
                """
            ),
            [
                Segment(
                    start=0,
                    end=13,
                    links=[Link(start=14, end=31, trait="description")],
                    part="basal segment",
                ),
                Description(start=14, end=31, description="larger than other"),
                Segment(
                    start=32,
                    end=40,
                    links=[Link(start=45, end=70, trait="description")],
                    part="segment",
                ),
                Description(start=45, end=70, description="slightly longer than wide"),
            ],
        )

    def test_description_03(self) -> None:
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                Description(start=0, end=13, description="subtriangular"),
                Part(
                    start=14,
                    end=19,
                    links=[
                        Link(trait="description", start=0, end=13),
                        Link(trait="description", start=20, end=44),
                        Link(trait="subpart", start=45, end=50),
                    ],
                    part="coxa",
                ),
                Description(start=20, end=44, description="proximally and acuminate"),
                Subpart(
                    start=45,
                    end=50,
                    links=[Link(trait="description", start=51, end=61)],
                    subpart="claw",
                ),
                Description(start=51, end=61, description="terminally"),
            ],
        )

    def test_description_04(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger from anterior to posterior,"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[Link(start=5, end=52, trait="description")],
                    part="leg",
                ),
                Description(
                    start=5,
                    end=52,
                    description="progressively larger from anterior to posterior",
                ),
            ],
        )

    def test_description_05(self) -> None:
        self.assertEqual(
            parse("Abdomen wider than thorax."),
            [
                Part(
                    start=0,
                    end=7,
                    links=[Link(start=8, end=18, trait="description")],
                    part="abdomen",
                ),
                Description(
                    start=8,
                    end=18,
                    description="wider than",
                ),
                Part(start=19, end=25, part="thorax"),
            ],
        )

    def test_description_06(self) -> None:
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[Link(start=5, end=37, trait="description")],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5, end=37, description="inserted anteriorly and close to"
                ),
                Subpart(
                    start=38,
                    end=56,
                    links=[Link(start=0, end=4, trait="seta")],
                    subpart="dorsal head suture",
                ),
            ],
        )

    def test_description_07(self) -> None:
        self.assertEqual(
            parse("DMHS inserted posteriorly and lateral to DPHS;"),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[
                        Link(start=5, end=40, trait="description"),
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5, end=40, description="inserted posteriorly and lateral to"
                ),
                Seta(
                    start=41,
                    end=45,
                    seta="dorsal principal head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_description_08(self) -> None:
        self.assertEqual(
            parse("(VPHS) ventrally on each side"),
            [
                Seta(
                    start=1,
                    end=5,
                    links=[Link(start=7, end=29, trait="description")],
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
                Description(start=7, end=29, description="ventrally on each side"),
            ],
        )

    def test_description_09(self) -> None:
        self.assertEqual(
            parse("narrow central setae and stout lateral setae"),
            [
                Description(start=0, end=6, description="narrow"),
                Seta(
                    start=7,
                    end=20,
                    links=[
                        Link(trait="description", start=0, end=6),
                        Link(trait="description", start=25, end=30),
                    ],
                    seta="central setae",
                ),
                Description(start=25, end=30, description="stout"),
                Seta(
                    start=31,
                    end=44,
                    links=[
                        Link(trait="description", start=0, end=6),
                        Link(trait="description", start=25, end=30),
                    ],
                    seta="lateral setae",
                ),
            ],
        )

    def test_description_10(self) -> None:
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                Description(start=0, end=15, description="broad spur-like"),
                Subpart(
                    start=16,
                    end=21,
                    links=[
                        Link(start=0, end=15, trait="description"),
                        Link(start=22, end=33, trait="description"),
                    ],
                    subpart="ridge",
                ),
                Description(start=22, end=33, description="posteriorly"),
            ],
        )

    def test_description_11(self) -> None:
        self.assertEqual(
            parse("""basal apodeme about twice as long as parameres;"""),
            [
                Subpart(
                    start=0,
                    end=13,
                    sex=None,
                    links=[
                        Link(start=14, end=36, trait="description"),
                    ],
                    subpart="basal apodeme",
                ),
                Description(
                    start=14,
                    end=36,
                    description="about twice as long as",
                ),
                Part(
                    start=37,
                    end=46,
                    links=[Link(start=0, end=13, trait="subpart")],
                    part="paramere",
                ),
            ],
        )

    def test_description_12(self) -> None:
        self.assertEqual(
            parse("""each articulating with corresponding paratergal plate """),
            [
                Description(start=5, end=17, description="articulating"),
                Plate(
                    start=23,
                    end=53,
                    links=[Link(start=5, end=17, trait="description")],
                    part="corresponding paratergal plate",
                ),
            ],
        )

    def test_description_13(self) -> None:
        self.assertEqual(
            parse("""parameres relatively broad and curved, tapering posteriorly;"""),
            [
                Part(
                    start=0,
                    end=9,
                    links=[Link(start=10, end=59, trait="description")],
                    part="paramere",
                ),
                Description(
                    start=10,
                    end=59,
                    description="relatively broad and curved, tapering posteriorly",
                ),
            ],
        )

    def test_description_14(self) -> None:
        self.assertEqual(
            parse("""2 sternites on each of segments 4-6;"""),
            [
                Count(start=0, end=1, count_low=2),
                Sternite(
                    start=2,
                    end=11,
                    links=[
                        Link(start=12, end=22, trait="description"),
                        Link(start=0, end=1, trait="count"),
                    ],
                    part="sternite",
                ),
                Description(
                    start=12,
                    end=22,
                    description="on each of",
                ),
                Segment(
                    start=23,
                    end=35,
                    links=[Link(start=2, end=11, trait="sternite")],
                    part="segment",
                    number=[4, 5, 6],
                ),
            ],
        )
