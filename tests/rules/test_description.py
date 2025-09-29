import unittest

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
                Description(
                    start=0,
                    end=13,
                    links=[Part(start=14, end=19, part="coxa")],
                    description="subtriangular",
                ),
                Part(
                    start=14,
                    end=19,
                    links=[Description(start=0, end=13, description="subtriangular")],
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
                        Description(start=14, end=31, description="larger than other"),
                        Segment(start=32, end=40, part="segment"),
                    ],
                    part="basal segment",
                ),
                Description(
                    start=14,
                    end=31,
                    links=[Segment(start=0, end=13, part="basal segment")],
                    description="larger than other",
                ),
                Segment(
                    start=32,
                    end=40,
                    links=[
                        Description(
                            start=45, end=70, description="slightly longer than wide"
                        ),
                        Segment(start=0, end=13, part="basal segment"),
                    ],
                    part="segment",
                ),
                Description(
                    start=45,
                    end=70,
                    links=[Segment(start=32, end=40, part="segment")],
                    description="slightly longer than wide",
                ),
            ],
        )

    def test_description_03(self) -> None:
        self.assertEqual(
            parse("""subtriangular coxae proximally and acuminate claws terminally"""),
            [
                Description(
                    start=0,
                    end=13,
                    links=[Part(start=14, end=19, part="coxa")],
                    description="subtriangular",
                ),
                Part(
                    start=14,
                    end=19,
                    links=[
                        Description(start=0, end=13, description="subtriangular"),
                        Description(
                            start=20, end=44, description="proximally and acuminate"
                        ),
                        Subpart(start=45, end=50, subpart="claw"),
                    ],
                    part="coxa",
                ),
                Description(
                    start=20,
                    end=44,
                    links=[Part(start=14, end=19, part="coxa")],
                    description="proximally and acuminate",
                ),
                Subpart(
                    start=45,
                    end=50,
                    links=[
                        Description(start=51, end=61, description="terminally"),
                        Part(start=14, end=19, part="coxa"),
                    ],
                    subpart="claw",
                ),
                Description(
                    start=51,
                    end=61,
                    links=[Subpart(start=45, end=50, subpart="claw")],
                    description="terminally",
                ),
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
                        Description(
                            start=5,
                            end=52,
                            description=(
                                "progressively larger from anterior to posterior"
                            ),
                        )
                    ],
                    part="leg",
                ),
                Description(
                    start=5,
                    end=52,
                    links=[Part(start=0, end=4, part="leg")],
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
                    links=[
                        Description(start=8, end=18, description="wider than"),
                        Part(start=19, end=25, part="thorax"),
                    ],
                    part="abdomen",
                ),
                Description(
                    start=8,
                    end=18,
                    links=[Part(start=0, end=7, part="abdomen")],
                    description="wider than",
                ),
                Part(
                    start=19,
                    end=25,
                    links=[Part(start=0, end=7, part="abdomen")],
                    part="thorax",
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
                        Description(
                            start=5,
                            end=37,
                            description="inserted anteriorly and close to",
                        ),
                        Subpart(start=38, end=56, subpart="dorsal head suture"),
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5,
                    end=37,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
                    description="inserted anteriorly and close to",
                ),
                Subpart(
                    start=38,
                    end=56,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
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
                        Description(
                            start=5,
                            end=40,
                            description="inserted posteriorly and lateral to",
                        ),
                        Seta(
                            start=41,
                            end=45,
                            seta="dorsal principal head setae",
                            seta_part="head",
                        ),
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5,
                    end=40,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
                    description="inserted posteriorly and lateral to",
                ),
                Seta(
                    start=41,
                    end=45,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
                    seta="dorsal principal head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_position_08(self) -> None:
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

    def test_description_09(self) -> None:
        self.assertEqual(
            parse("narrow central setae and stout lateral setae"),
            [
                Description(
                    start=0,
                    end=14,
                    links=[Seta(start=15, end=20, seta="setae")],
                    description="narrow central",
                ),
                Seta(
                    start=15,
                    end=20,
                    links=[Description(start=0, end=14, description="narrow central")],
                    seta="setae",
                ),
                Description(
                    start=25,
                    end=38,
                    links=[Seta(start=39, end=44, seta="setae")],
                    description="stout lateral",
                ),
                Seta(
                    start=39,
                    end=44,
                    links=[Description(start=25, end=38, description="stout lateral")],
                    seta="setae",
                ),
            ],
        )

    def test_description_10(self) -> None:
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                Description(
                    start=0,
                    end=15,
                    links=[Subpart(start=16, end=21, subpart="ridge")],
                    description="broad spur-like",
                ),
                Subpart(
                    start=16,
                    end=21,
                    links=[
                        Description(start=0, end=15, description="broad spur-like"),
                        Description(start=22, end=33, description="posteriorly"),
                    ],
                    subpart="ridge",
                ),
                Description(
                    start=22,
                    end=33,
                    links=[Subpart(start=16, end=21, subpart="ridge")],
                    description="posteriorly",
                ),
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
                        Description(
                            start=14, end=36, description="about twice as long as"
                        ),
                        Part(start=37, end=46, part="paramere"),
                    ],
                    subpart="basal apodeme",
                ),
                Description(
                    start=14,
                    end=36,
                    links=[Subpart(start=0, end=13, subpart="basal apodeme")],
                    description="about twice as long as",
                ),
                Part(
                    start=37,
                    end=46,
                    links=[Subpart(start=0, end=13, subpart="basal apodeme")],
                    part="paramere",
                ),
            ],
        )

    def test_description_12(self) -> None:
        self.assertEqual(
            parse("""each articulating with corresponding paratergal plate """),
            [
                Description(
                    start=5,
                    end=17,
                    links=[
                        Plate(start=23, end=53, part="corresponding paratergal plate")
                    ],
                    description="articulating",
                ),
                Plate(
                    start=23,
                    end=53,
                    links=[Description(start=5, end=17, description="articulating")],
                    part="corresponding paratergal plate",
                ),
            ],
        )

    def test_description_13(self) -> None:
        self.assertEqual(
            parse("""on each side"""),
            [
                Description(start=0, end=12, description="on each side"),
            ],
        )

    def test_description_14(self) -> None:
        self.assertEqual(
            parse("""distinctly shorter than lateral"""),
            [
                Description(
                    start=0, end=31, description="distinctly shorter than lateral"
                ),
            ],
        )

    def test_description_15(self) -> None:
        self.assertEqual(
            parse("""moderate length and about equal in size;"""),
            [
                Description(start=0, end=15, description="moderate length"),
                Description(start=20, end=39, description="about equal in size"),
            ],
        )

    def test_description_16(self) -> None:
        self.assertEqual(
            parse("""parameres relatively broad and curved, tapering posteriorly;"""),
            [
                Part(
                    start=0,
                    end=9,
                    links=[
                        Description(
                            start=10,
                            end=59,
                            description=(
                                "relatively broad and curved, tapering posteriorly"
                            ),
                        )
                    ],
                    part="paramere",
                ),
                Description(
                    start=10,
                    end=59,
                    links=[Part(start=0, end=9, part="paramere")],
                    description="relatively broad and curved, tapering posteriorly",
                ),
            ],
        )

    def test_description_17(self) -> None:
        self.assertEqual(
            parse("""2 sternites on each of segments 4-6;"""),
            [
                Count(
                    start=0,
                    end=1,
                    links=[Sternite(start=2, end=11, part="sternite")],
                    count_low=2,
                ),
                Sternite(
                    start=2,
                    end=11,
                    links=[
                        Description(start=12, end=22, description="on each of"),
                        Count(start=0, end=1, count_low=2),
                        Segment(
                            _trait="segment",
                            _text="segments 4-6",
                            start=23,
                            end=35,
                            part="segment",
                            number=[4, 5, 6],
                        ),
                    ],
                    part="sternite",
                ),
                Description(
                    start=12,
                    end=22,
                    links=[Sternite(start=2, end=11, part="sternite")],
                    description="on each of",
                ),
                Segment(
                    start=23,
                    end=35,
                    links=[Sternite(start=2, end=11, part="sternite")],
                    part="segment",
                    number=[4, 5, 6],
                ),
            ],
        )
