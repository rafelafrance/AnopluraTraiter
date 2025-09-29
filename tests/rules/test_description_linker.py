import unittest

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
                    links=[
                        Description(start=6, end=23, description="present except on"),
                        Part(start=24, end=28, part="leg"),
                    ],
                    seta="setae",
                ),
                Description(
                    start=6,
                    end=23,
                    links=[
                        Seta(_trait="seta", _text="setae", start=0, end=5, seta="setae")
                    ],
                    description="present except on",
                ),
                Part(
                    start=24,
                    end=28,
                    links=[Seta(start=0, end=5, seta="setae")],
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
                    links=[
                        Description(
                            start=18, end=39, description="broadly subtriangular"
                        )
                    ],
                    part="plate",
                    number=[1],
                ),
                Description(
                    start=18,
                    end=39,
                    links=[Plate(start=0, end=7, part="plate", number=[1])],
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
                    links=[
                        Description(start=5, end=17, description="on each side"),
                        Subpart(start=21, end=37, subpart="posterior margin"),
                        Plate(start=41, end=57, part="subgenital plate"),
                    ],
                    seta="setae",
                ),
                Description(
                    start=5,
                    end=17,
                    links=[Seta(start=0, end=4, seta="setae")],
                    description="on each side",
                ),
                Subpart(
                    start=21,
                    end=37,
                    links=[
                        Seta(start=0, end=4, seta="setae"),
                        Plate(start=41, end=57, part="subgenital plate"),
                    ],
                    subpart="posterior margin",
                ),
                Plate(
                    start=41,
                    end=57,
                    links=[
                        Seta(start=0, end=4, seta="setae"),
                        Subpart(start=21, end=37, subpart="posterior margin"),
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
                        Description(
                            start=23, end=47, description="club-shaped with rounded"
                        ),
                        Subpart(start=48, end=69, subpart="anterolateral margin"),
                        Subpart(start=89, end=102, subpart="anterior apex"),
                        Subpart(start=117, end=136, subpart="posterior extension"),
                        Subpart(start=151, end=165, subpart="posterior apex"),
                    ],
                    part="thoracic sternal plate",
                ),
                Description(
                    start=23,
                    end=47,
                    links=[Plate(start=0, end=22, part="thoracic sternal plate")],
                    description="club-shaped with rounded",
                ),
                Subpart(
                    start=48,
                    end=69,
                    links=[
                        Description(start=71, end=88, description="broadly acuminate"),
                        Plate(start=0, end=22, part="thoracic sternal plate"),
                    ],
                    subpart="anterolateral margin",
                ),
                Description(
                    _trait="description",
                    _text="broadly acuminate",
                    start=71,
                    end=88,
                    links=[Subpart(start=48, end=69, subpart="anterolateral margin")],
                    description="broadly acuminate",
                ),
                Subpart(
                    start=89,
                    end=102,
                    links=[
                        Description(start=108, end=116, description="elongate"),
                        Plate(start=0, end=22, part="thoracic sternal plate"),
                    ],
                    subpart="anterior apex",
                ),
                Description(
                    start=108,
                    end=116,
                    links=[Subpart(start=89, end=102, subpart="anterior apex")],
                    description="elongate",
                ),
                Subpart(
                    start=117,
                    end=136,
                    links=[
                        Description(start=142, end=150, description="squarish"),
                        Plate(start=0, end=22, part="thoracic sternal plate"),
                    ],
                    subpart="posterior extension",
                ),
                Description(
                    start=142,
                    end=150,
                    links=[Subpart(start=117, end=136, subpart="posterior extension")],
                    description="squarish",
                ),
                Subpart(
                    start=151,
                    end=165,
                    links=[Plate(start=0, end=22, part="thoracic sternal plate")],
                    subpart="posterior apex",
                ),
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
                        Description(
                            start=17, end=43, description="relatively broad spur-like"
                        ),
                        Subpart(start=44, end=49, subpart="ridge"),
                    ],
                    part="hind femur",
                ),
                Description(
                    start=17,
                    end=43,
                    links=[Part(start=0, end=11, part="hind femur")],
                    description="relatively broad spur-like",
                ),
                Subpart(
                    start=44,
                    end=49,
                    links=[
                        Description(start=50, end=61, description="posteriorly"),
                        Part(start=0, end=11, part="hind femur"),
                    ],
                    subpart="ridge",
                ),
                Description(
                    start=50,
                    end=61,
                    links=[Subpart(start=44, end=49, subpart="ridge")],
                    description="posteriorly",
                ),
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
                        Description(
                            start=9, end=30, description="dorsally on each side"
                        )
                    ],
                    seta="dorsal posterior central head setae",
                    seta_part="head",
                ),
                Description(
                    start=9,
                    end=30,
                    links=[
                        Seta(
                            start=1,
                            end=7,
                            seta="dorsal posterior central head setae",
                            seta_part="head",
                        )
                    ],
                    description="dorsally on each side",
                ),
            ],
        )

    def test_description_linker_07(self) -> None:
        self.assertEqual(
            parse("""setae of moderate length and about equal in size; """),
            [
                Seta(
                    start=0,
                    end=5,
                    links=[
                        Description(start=9, end=24, description="moderate length"),
                        Description(
                            start=29, end=48, description="about equal in size"
                        ),
                    ],
                    seta="setae",
                ),
                Description(
                    start=9,
                    end=24,
                    links=[Seta(start=0, end=5, seta="setae")],
                    description="moderate length",
                ),
                Description(
                    start=29,
                    end=48,
                    links=[Seta(start=0, end=5, seta="setae")],
                    description="about equal in size",
                ),
            ],
        )
