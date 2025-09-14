import unittest

from anoplura.rules.description import Description
from anoplura.rules.part import Part
from anoplura.rules.plate import Plate
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestDescription(unittest.TestCase):
    def test_description_01(self) -> None:
        self.assertEqual(
            parse("subtriangular coxae"),
            [
                Description(start=0, end=13, description="subtriangular"),
                Part(start=14, end=19, part="coxa"),
            ],
        )

    def test_description_02(self) -> None:
        self.assertEqual(
            parse("Head longer than wide, broadly rounded anteriorly;"),
            [
                Part(start=0, end=4, part="head"),
                Description(
                    start=5,
                    end=49,
                    description="longer than wide, broadly rounded anteriorly",
                ),
            ],
        )

    def test_description_03(self) -> None:
        self.assertEqual(
            parse(
                """
                basal segment larger than other segments and slightly longer than wide;
                """
            ),
            [
                Segment(start=0, end=13, part="basal segment"),
                Description(start=14, end=25, description="larger than"),
                Segment(start=26, end=40, sex=None, part="segment"),
                Description(start=45, end=70, description="slightly longer than wide"),
            ],
        )

    def test_description_04(self) -> None:
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                Description(start=0, end=13, description="subtriangular"),
                Part(start=14, end=19, sex=None, part="coxa"),
                Description(start=20, end=44, description="proximally and acuminate"),
                Subpart(start=45, end=50, subpart="claw"),
                Description(start=51, end=61, description="terminally"),
            ],
        )

    def test_description_05(self) -> None:
        self.assertEqual(
            parse("Legs progressively larger from anterior to posterior,"),
            [
                Part(start=0, end=4, part="leg"),
                Description(
                    start=5,
                    end=52,
                    description="progressively larger from anterior to posterior",
                ),
            ],
        )

    def test_description_06(self) -> None:
        self.maxDiff = None
        self.assertEqual(
            parse("Abdomen wider than thorax."),
            [
                Part(start=0, end=7, part="abdomen"),
                Description(start=8, end=18, description="wider than"),
                Part(start=19, end=25, part="thorax"),
            ],
        )

    def test_description_07(self) -> None:
        self.assertEqual(
            parse("""Thoracic sternal plate club-shaped with rounded anterolateral
                margins, broadly acuminate anterior apex, and elongate posterior
                extension with squarish posterior apex,"""),
            [
                Plate(start=0, end=22, part="thoracic sternal plate"),
                Description(start=23, end=47, description="club-shaped with rounded"),
                Subpart(start=48, end=69, subpart="anterolateral margin"),
                Description(start=71, end=88, description="broadly acuminate"),
                Subpart(start=89, end=102, subpart="anterior apex"),
                Description(start=108, end=116, description="elongate"),
                Subpart(start=117, end=136, subpart="posterior extension"),
                Description(start=142, end=150, description="squarish"),
                Subpart(start=151, end=165, subpart="posterior apex"),
            ],
        )

    def test_description_08(self) -> None:
        self.assertEqual(
            parse("""hind femora with relatively broad spur-like ridge posteriorly"""),
            [
                Part(start=0, end=11, part="hind femur"),
                Description(start=17, end=43, description="relatively broad spur-like"),
                Subpart(start=44, end=49, subpart="ridge"),
                Description(start=50, end=61, description="posteriorly"),
            ],
        )

    def test_description_09(self) -> None:
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(
                    start=0, end=4, seta="dorsal marginal head setae", seta_part="head"
                ),
                Description(
                    start=5, end=37, description="inserted anteriorly and close to"
                ),
                Subpart(start=38, end=56, subpart="dorsal head suture"),
            ],
        )

    def test_description_10(self) -> None:
        self.assertEqual(
            parse("DMHS inserted posteriorly and lateral to DPHS;"),
            [
                Seta(
                    start=0, end=4, seta="dorsal marginal head setae", seta_part="head"
                ),
                Description(
                    start=5, end=37, description="inserted posteriorly and lateral"
                ),
                Seta(
                    start=41,
                    end=45,
                    seta="dorsal principal head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_position_11(self) -> None:
        self.assertEqual(
            parse("(VPHS) ventrally on each side"),
            [
                Seta(
                    start=1,
                    end=5,
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
                Description(start=7, end=29, description="ventrally on each side"),
            ],
        )

    def test_description_12(self) -> None:
        self.assertEqual(
            parse("narrow central setae and stout lateral setae"),
            [
                Description(start=0, end=14, description="narrow central"),
                Seta(start=15, end=20, seta="setae"),
                Description(start=25, end=38, description="stout lateral"),
                Seta(start=39, end=44, seta="setae"),
            ],
        )

    def test_description_13(self) -> None:
        self.assertEqual(
            parse("""rounded anterolateral margins"""),
            [
                Description(start=0, end=7, description="rounded"),
                Subpart(start=8, end=29, subpart="anterolateral margin"),
            ],
        )

    def test_description_14(self) -> None:
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                Description(start=0, end=15, description="broad spur-like"),
                Subpart(start=16, end=21, subpart="ridge"),
                Description(start=22, end=33, description="posteriorly"),
            ],
        )

    def test_description_15(self) -> None:
        self.assertEqual(
            parse("""curved and terminating in acuminate apex."""),
            [
                Description(
                    start=0, end=35, description="curved and terminating in acuminate"
                ),
                Subpart(start=36, end=40, subpart="apex"),
            ],
        )

    def test_description_16(self) -> None:
        self.assertEqual(
            parse("""fairly long"""),
            [
                Description(start=0, end=11, description="fairly long"),
            ],
        )

    def test_description_17(self) -> None:
        self.assertEqual(
            parse("""twice as long as"""),
            [
                Description(start=0, end=13, description="twice as long"),
            ],
        )

    def test_description_18(self) -> None:
        self.assertEqual(
            parse("""each articulating with corresponding"""),
            [
                Description(
                    start=0, end=36, description="each articulating with corresponding"
                ),
            ],
        )

    def test_description_19(self) -> None:
        self.assertEqual(
            parse("""on each side"""),
            [
                Description(start=0, end=12, description="on each side"),
            ],
        )

    def test_description_20(self) -> None:
        self.assertEqual(
            parse("""distinctly shorter than lateral"""),
            [
                Description(
                    start=0, end=31, description="distinctly shorter than lateral"
                ),
            ],
        )

    def test_description_21(self) -> None:
        self.assertEqual(
            parse("""moderate length and about equal in size;"""),
            [
                Description(start=0, end=15, description="moderate length"),
                Description(start=20, end=39, description="about equal in size"),
            ],
        )
