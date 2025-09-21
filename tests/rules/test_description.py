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
                        Description(
                            start=14,
                            end=70,
                            description=(
                                "larger than other segments and slightly "
                                "longer than wide"
                            ),
                        )
                    ],
                    part="basal segment",
                ),
                Description(
                    start=14,
                    end=70,
                    links=[Segment(start=0, end=13, part="basal segment")],
                    description=(
                        "larger than other segments and slightly longer than wide"
                    ),
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
                            start=20,
                            end=61,
                            description="proximally and acuminate claws terminally",
                        ),
                    ],
                    part="coxa",
                ),
                Description(
                    start=20,
                    end=61,
                    links=[Part(start=14, end=19, part="coxa")],
                    description="proximally and acuminate claws terminally",
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
        self.maxDiff = None
        self.assertEqual(
            parse("Abdomen wider than thorax."),
            [
                Part(
                    start=0,
                    end=7,
                    links=[
                        Description(start=8, end=25, description="wider than thorax")
                    ],
                    part="abdomen",
                ),
                Description(
                    start=8,
                    end=25,
                    links=[Part(start=0, end=7, part="abdomen")],
                    description="wider than thorax",
                ),
            ],
        )

    def test_description_06(self) -> None:
        self.assertEqual(
            parse("""Thoracic sternal plate club-shaped with rounded anterolateral
                margins, broadly acuminate anterior apex, and elongate posterior
                extension with squarish posterior apex,"""),
            [
                Plate(
                    start=0,
                    end=22,
                    links=[
                        Description(
                            start=23,
                            end=165,
                            description="club-shaped with rounded anterolateral "
                            "margins, broadly acuminate anterior "
                            "apex, and elongate posterior extension "
                            "with squarish posterior apex",
                        )
                    ],
                    part="thoracic sternal plate",
                ),
                Description(
                    start=23,
                    end=165,
                    links=[
                        Plate(
                            start=0,
                            end=22,
                            part="thoracic sternal plate",
                        )
                    ],
                    description="club-shaped with rounded anterolateral margins, "
                    "broadly acuminate anterior apex, and elongate "
                    "posterior extension with squarish posterior apex",
                ),
            ],
        )

    def test_description_07(self) -> None:
        self.assertEqual(
            parse("""hind femora with relatively broad spur-like ridge posteriorly"""),
            [
                Part(
                    start=0,
                    end=11,
                    links=[
                        Description(
                            start=17,
                            end=61,
                            description="relatively broad spur-like ridge posteriorly",
                        )
                    ],
                    part="hind femur",
                ),
                Description(
                    start=17,
                    end=61,
                    links=[Part(start=0, end=11, part="hind femur")],
                    description="relatively broad spur-like ridge posteriorly",
                ),
            ],
        )

    def test_description_08(self) -> None:
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[
                        Description(
                            start=5,
                            end=56,
                            description=(
                                "inserted anteriorly and close to dorsal head suture"
                            ),
                        )
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5,
                    end=56,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
                    description="inserted anteriorly and close to dorsal head suture",
                ),
            ],
        )

    def test_description_09(self) -> None:
        self.assertEqual(
            parse("DMHS inserted posteriorly and lateral to DPHS;"),
            [
                Seta(
                    start=0,
                    end=4,
                    links=[
                        Description(
                            start=5,
                            end=45,
                            description="inserted posteriorly and lateral to dphs",
                        )
                    ],
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                Description(
                    start=5,
                    end=45,
                    links=[
                        Seta(
                            start=0,
                            end=4,
                            seta="dorsal marginal head setae",
                            seta_part="head",
                        )
                    ],
                    description="inserted posteriorly and lateral to dphs",
                ),
            ],
        )

    def test_position_10(self) -> None:
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

    def test_description_11(self) -> None:
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

    def test_description_12(self) -> None:
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                Description(
                    start=0, end=33, description="broad spur-like ridge posteriorly"
                )
            ],
        )

    def test_description_13(self) -> None:
        self.assertEqual(
            parse("""basal apodeme about twice as long as parameres;"""),
            [
                Subpart(
                    start=0,
                    end=13,
                    links=[
                        Description(
                            start=14,
                            end=46,
                            description="about twice as long as parameres",
                        )
                    ],
                    subpart="basal apodeme",
                ),
                Description(
                    start=14,
                    end=46,
                    links=[Subpart(start=0, end=13, subpart="basal apodeme")],
                    description="about twice as long as parameres",
                ),
            ],
        )

    def test_description_14(self) -> None:
        self.assertEqual(
            parse("""each articulating with corresponding paratergal plate """),
            [
                Description(
                    start=0,
                    end=53,
                    description="each articulating with corresponding paratergal plate",
                )
            ],
        )

    def test_description_15(self) -> None:
        self.assertEqual(
            parse("""on each side"""),
            [
                Description(start=0, end=12, description="on each side"),
            ],
        )

    def test_description_16(self) -> None:
        self.assertEqual(
            parse("""distinctly shorter than lateral"""),
            [
                Description(
                    start=0, end=31, description="distinctly shorter than lateral"
                ),
            ],
        )

    def test_description_17(self) -> None:
        self.assertEqual(
            parse("""moderate length and about equal in size;"""),
            [
                Description(start=0, end=15, description="moderate length"),
                Description(start=20, end=39, description="about equal in size"),
            ],
        )
