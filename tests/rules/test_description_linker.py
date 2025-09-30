import unittest

from anoplura.rules.base import Link
from anoplura.rules.description import Description
from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.seta import Seta
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
                    links=[Link(start=6, end=23, trait="description")],
                    seta="setae",
                ),
                Description(start=6, end=23, description="present except on"),
                Part(
                    start=24,
                    end=28,
                    links=[Link(start=0, end=5, trait="seta")],
                    part="leg",
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
                Description(
                    start=18,
                    end=39,
                    description="broadly subtriangular",
                ),
            ],
        )

    def test_description_linker_03(self) -> None:
        self.assertEqual(
            parse("seta on each side on posterior margin of subgenital plate."),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[Link(start=5, end=17, trait="description")],
                    seta="setae",
                ),
                Description(start=5, end=17, description="on each side"),
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
        self.assertEqual(
            parse("""Thoracic sternal plate club-shaped with rounded anterolateral
                margins, broadly acuminate anterior apex, and elongate posterior
                extension with squarish posterior apex."""),
            [
                Plate(
                    start=0,
                    end=22,
                    links=[
                        Link(trait="description", start=23, end=47),
                        Link(trait="subpart", start=48, end=69),
                        Link(trait="subpart", start=89, end=102),
                        Link(trait="subpart", start=117, end=136),
                        Link(trait="subpart", start=151, end=165),
                    ],
                    part="thoracic sternal plate",
                ),
                Description(start=23, end=47, description="club-shaped with rounded"),
                Subpart(
                    start=48,
                    end=69,
                    links=[Link(trait="description", start=71, end=88)],
                    subpart="anterolateral margin",
                ),
                Description(start=71, end=88, description="broadly acuminate"),
                Subpart(
                    start=89,
                    end=102,
                    links=[Link(trait="description", start=108, end=116)],
                    subpart="anterior apex",
                ),
                Description(start=108, end=116, description="elongate"),
                Subpart(
                    start=117,
                    end=136,
                    links=[Link(trait="description", start=142, end=150)],
                    subpart="posterior extension",
                ),
                Description(start=142, end=150, description="squarish"),
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
                        Link(start=17, end=43, trait="description"),
                        Link(start=44, end=49, trait="subpart"),
                    ],
                    part="hind femur",
                ),
                Description(
                    start=17,
                    end=43,
                    description="relatively broad spur-like",
                ),
                Subpart(
                    start=44,
                    end=49,
                    links=[Link(start=50, end=61, trait="description")],
                    subpart="ridge",
                ),
                Description(start=50, end=61, description="posteriorly"),
            ],
        )

    def test_description_linker_06(self) -> None:
        self.assertEqual(
            parse("""(DPoCHS) dorsally on each side;"""),
            [
                Seta(
                    start=1,
                    end=7,
                    links=[Link(start=9, end=30, trait="description")],
                    seta="dorsal posterior central head setae",
                    seta_part="head",
                ),
                Description(start=9, end=30, description="dorsally on each side"),
            ],
        )

    def test_description_linker_07(self) -> None:
        self.assertEqual(
            parse("""apical setae of moderate length and about equal in size;"""),
            [
                Seta(
                    start=0,
                    end=12,
                    links=[
                        Link(start=16, end=31, trait="description"),
                        Link(start=36, end=55, trait="description"),
                    ],
                    seta="apical setae",
                ),
                Description(start=16, end=31, description="moderate length"),
                Description(start=36, end=55, description="about equal in size"),
            ],
        )

    def test_description_linker_08(self) -> None:
        self.assertEqual(
            parse("""StAS, all relatively long,"""),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[Link(start=10, end=25, trait="description")],
                    seta="sternal abdominal setae",
                    seta_part="abdomen",
                ),
                Description(start=10, end=25, description="relatively long"),
            ],
        )

    def test_description_linker_09(self) -> None:
        self.assertEqual(
            parse("""small setae arranged more or less centrally"""),
            [
                Description(start=0, end=5, description="small"),
                Seta(
                    start=6,
                    end=11,
                    links=[
                        Link(start=0, end=5, trait="description"),
                        Link(start=21, end=43, trait="description"),
                    ],
                    seta="setae",
                ),
                Description(start=21, end=43, description="more or less centrally"),
            ],
        )
