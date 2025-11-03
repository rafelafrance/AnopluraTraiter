import unittest

from anoplura.rules.base import Link
from anoplura.rules.count import Count
from anoplura.rules.group import Group
from anoplura.rules.group_prefix import GroupPrefix
from anoplura.rules.morphology import Morphology
from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.position import Position
from anoplura.rules.relative_position import RelativePosition
from anoplura.rules.relative_size import RelativeSize
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.shape import Shape
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestDescription(unittest.TestCase):
    def test_description_01(self) -> None:
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                Shape(start=0, end=13, shape="subtriangular"),
                Part(
                    start=14,
                    end=19,
                    links=[Link(start=0, end=13, trait="shape")],
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
                    links=[
                        Link(trait="relative_size", start=14, end=40),
                        Link(trait="size_description", start=45, end=70),
                    ],
                    part="basal segment",
                ),
                RelativeSize(
                    start=14,
                    end=40,
                    relative_size="larger than other",
                    relative_part="segment",
                ),
                SizeDescription(
                    start=45, end=70, size_description="slightly longer than wide"
                ),
            ],
        )

    def test_description_03(self) -> None:
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                Shape(start=0, end=13, shape="subtriangular"),
                Part(
                    start=14,
                    end=19,
                    links=[
                        Link(trait="shape", start=0, end=13),
                        Link(trait="position", start=20, end=30),
                        Link(trait="subpart", start=45, end=50),
                    ],
                    part="coxa",
                ),
                Position(start=20, end=30, position="proximally"),
                Shape(start=35, end=44, shape="acuminate"),
                Subpart(
                    start=45,
                    end=50,
                    links=[
                        Link(trait="shape", start=35, end=44),
                        Link(trait="position", start=51, end=61),
                    ],
                    subpart="claw",
                ),
                Position(start=51, end=61, position="terminally"),
            ],
        )

    def test_description_04(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger from anterior to posterior,"),
            [
                Part(
                    start=0,
                    end=4,
                    links=[
                        Link(start=5, end=25, trait="size_description"),
                        Link(start=31, end=52, trait="position"),
                    ],
                    part="leg",
                ),
                SizeDescription(
                    start=5, end=25, size_description="progressively larger"
                ),
                Position(start=31, end=52, position="anterior to posterior"),
            ],
        )

    def test_description_05(self) -> None:
        self.assertEqual(
            parse("Abdomen wider than thorax."),
            [
                Part(
                    start=0,
                    end=7,
                    links=[Link(trait="relative_size", start=8, end=25)],
                    part="abdomen",
                ),
                RelativeSize(
                    start=8, end=25, relative_size="wider than", relative_part="thorax"
                ),
            ],
        )

    def test_description_06(self) -> None:
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[
                        Link(trait="position", start=5, end=24),
                        Link(trait="relative_position", start=29, end=56),
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Position(start=5, end=24, position="inserted anteriorly"),
                RelativePosition(
                    start=29,
                    end=56,
                    relative_position="close to",
                    relative_part="dorsal head suture",
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
                        Link(start=5, end=25, trait="position"),
                        Link(start=30, end=45, trait="relative_position"),
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Position(start=5, end=25, position="inserted posteriorly"),
                RelativePosition(
                    start=30,
                    end=45,
                    relative_position="lateral to",
                    relative_part="dorsal principal head setae",
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
                    links=[
                        Link(trait="position", start=7, end=16),
                        Link(trait="group", start=17, end=29),
                    ],
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
                Position(start=7, end=16, position="ventrally"),
                Group(start=17, end=29, group="on each side"),
            ],
        )

    def test_description_09(self) -> None:
        self.assertEqual(
            parse("narrow central setae and stout lateral setae"),
            [
                Shape(start=0, end=6, shape="narrow"),
                Seta(
                    start=7,
                    end=20,
                    links=[Link(trait="shape", start=0, end=6, _text="narrow")],
                    seta="central setae",
                ),
                Shape(start=25, end=30, shape="stout"),
                Seta(
                    start=31,
                    end=44,
                    links=[Link(trait="shape", start=25, end=30, _text="stout")],
                    seta="lateral setae",
                ),
            ],
        )

    def test_description_10(self) -> None:
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                Shape(start=0, end=15, shape="broad spur-like"),
                Subpart(
                    start=16,
                    end=21,
                    links=[
                        Link(start=0, end=15, trait="shape"),
                        Link(start=22, end=33, trait="position"),
                    ],
                    subpart="ridge",
                ),
                Position(start=22, end=33, position="posteriorly"),
            ],
        )

    def test_description_11(self) -> None:
        self.assertEqual(
            parse("""basal apodeme about twice as long as parameres;"""),
            [
                Subpart(
                    start=0,
                    end=13,
                    links=[Link(trait="relative_size", start=14, end=46)],
                    subpart="basal apodeme",
                ),
                RelativeSize(
                    start=14,
                    end=46,
                    relative_size="about twice as long as",
                    relative_part="paramere",
                ),
            ],
        )

    def test_description_12(self) -> None:
        self.assertEqual(
            parse("""each articulating with corresponding paratergal plate """),
            [
                Morphology(start=5, end=17, morphology="articulating"),
                Plate(
                    start=23,
                    end=53,
                    links=[Link(start=5, end=17, trait="morphology")],
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
                    links=[
                        Link(trait="shape", start=10, end=47),
                        Link(trait="position", start=48, end=59),
                    ],
                    part="paramere",
                ),
                Shape(start=10, end=47, shape="relatively broad and curved, tapering"),
                Position(start=48, end=59, position="posteriorly"),
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
                    links=[Link(trait="count", start=0, end=1)],
                    part="sternite",
                ),
                GroupPrefix(
                    start=12,
                    end=22,
                    group="on each of",
                ),
                Segment(
                    start=23,
                    end=35,
                    links=[Link(trait="group_prefix", start=12, end=22)],
                    part="segment",
                    number=[4, 5, 6],
                ),
            ],
        )
