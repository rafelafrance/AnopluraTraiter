import unittest

from anoplura.rules.base_rule import Link
from anoplura.rules.group import Group
from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.position import Position
from anoplura.rules.relative_position import RelativePosition
from anoplura.rules.seta import Seta
from anoplura.rules.shape import Shape
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestDescriptionLinker(unittest.TestCase):
    def test_description_linker_01(self) -> None:
        self.assertEqual(
            parse("setae present except on legs."),
            [
                Seta(
                    start=0,
                    end=5,
                    links=[Link(trait="relative_position", start=6, end=28)],
                    seta="setae",
                ),
                RelativePosition(
                    start=6,
                    end=28,
                    relative_position="present except on",
                    relative_part="leg",
                ),
            ],
        )

    def test_description_linker_02(self) -> None:
        self.assertEqual(
            parse("plate I, which is broadly subtriangular"),
            [
                Plate(
                    start=0,
                    end=7,
                    links=[Link(start=18, end=39, trait="description")],
                    part="plate",
                    number=[1],
                ),
                Shape(start=18, end=39, shape="broadly subtriangular"),
            ],
        )

    def test_description_linker_03(self) -> None:
        self.assertEqual(
            parse("seta on each side on posterior margin of subgenital plate."),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[Link(start=5, end=17, trait="group")],
                    seta="setae",
                ),
                Group(start=5, end=17, group="on each side"),
                Subpart(
                    start=21,
                    end=37,
                    links=[Link(start=0, end=4, trait="seta")],
                    subpart="posterior margin",
                ),
                Plate(
                    start=41,
                    end=57,
                    links=[
                        Link(start=0, end=4, trait="seta"),
                        Link(start=21, end=37, trait="subpart"),
                    ],
                    part="subgenital plate",
                ),
            ],
        )

    def test_description_linker_04(self) -> None:
        # TODO: Last shape should link to the last subpart
        self.assertEqual(
            parse("""Thoracic sternal plate club-shaped with rounded anterolateral
                margins, broadly acuminate anterior apex, and elongate posterior
                extension with squarish posterior apex."""),
            [
                Plate(
                    start=0,
                    end=22,
                    links=[
                        Link(trait="shape", start=23, end=47),
                        Link(trait="subpart", start=48, end=69),
                        Link(trait="subpart", start=89, end=102),
                        Link(trait="subpart", start=117, end=136),
                        Link(trait="subpart", start=151, end=165),
                    ],
                    part="thoracic sternal plate",
                    number=None,
                ),
                Shape(start=23, end=47, shape="club-shaped with rounded"),
                Subpart(
                    start=48,
                    end=69,
                    links=[Link(trait="shape", start=71, end=88)],
                    subpart="anterolateral margin",
                ),
                Shape(start=71, end=88, shape="broadly acuminate"),
                Subpart(
                    start=89,
                    end=102,
                    links=[Link(trait="shape", start=108, end=116)],
                    subpart="anterior apex",
                ),
                Shape(start=108, end=116, shape="elongate"),
                Subpart(
                    start=117,
                    end=136,
                    links=[Link(trait="shape", start=142, end=150)],
                    subpart="posterior extension",
                ),
                Shape(start=142, end=150, shape="squarish"),
                Subpart(start=151, end=165, subpart="posterior apex"),
            ],
        )

    def test_description_linker_05(self) -> None:
        self.assertEqual(
            parse("""hind femora with relatively broad spur-like ridge posteriorly"""),
            [
                Part(
                    start=0,
                    end=11,
                    links=[
                        Link(start=17, end=43, trait="shape"),
                        Link(start=44, end=49, trait="subpart"),
                    ],
                    part="hind femur",
                ),
                Shape(
                    start=17,
                    end=43,
                    shape="relatively broad spur-like",
                ),
                Subpart(
                    start=44,
                    end=49,
                    links=[Link(start=50, end=61, trait="position")],
                    subpart="ridge",
                ),
                Position(start=50, end=61, position="posteriorly"),
            ],
        )

    def test_description_linker_06(self) -> None:
        self.assertEqual(
            parse("""(DPoCHS) dorsally on each side;"""),
            [
                Seta(
                    start=1,
                    end=7,
                    links=[
                        Link(trait="position", start=9, end=17),
                        Link(trait="group", start=18, end=30),
                    ],
                    seta="dorsal posterior central head setae",
                    seta_part="head",
                ),
                Position(start=9, end=17, position="dorsally"),
                Group(start=18, end=30, group="on each side"),
            ],
        )

    def test_description_linker_07(self) -> None:
        self.assertEqual(
            parse("""apical setae of moderate length and about equal in size;"""),
            [
                Seta(
                    start=0,
                    end=12,
                    links=[Link(trait="size_description", start=16, end=55)],
                    seta="apical setae",
                ),
                SizeDescription(
                    start=16,
                    end=55,
                    size_description="moderate length and about equal in size",
                ),
            ],
        )

    def test_description_linker_08(self) -> None:
        self.assertEqual(
            parse("""StAS, all relatively long,"""),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[Link(start=10, end=25, trait="size_description")],
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                ),
                SizeDescription(start=10, end=25, size_description="relatively long"),
            ],
        )

    def test_description_linker_09(self) -> None:
        self.assertEqual(
            parse("""small setae arranged more or less centrally"""),
            [
                SizeDescription(start=0, end=5, size_description="small"),
                Seta(
                    start=6,
                    end=11,
                    links=[
                        Link(trait="size_description", start=0, end=5),
                        Link(trait="position", start=12, end=43),
                    ],
                    seta="setae",
                ),
                Position(start=12, end=43, position="arranged more or less centrally"),
            ],
        )

    def test_description_linker_10(self) -> None:
        self.assertEqual(
            parse("with small seta,"),
            [
                SizeDescription(start=6, end=11, size_description="small"),
                Seta(
                    start=12,
                    end=16,
                    links=[Link(trait="size_description", start=6, end=11)],
                    seta="setae",
                ),
            ],
        )
