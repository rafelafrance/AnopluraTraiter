import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_morphology import SetaMorphology
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSetaPosition(unittest.TestCase):
    def test_seta_position_01(self) -> None:
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(
                    start=0, end=4, seta="dorsal marginal head setae", seta_part="head"
                ),
                SetaMorphology(
                    start=5,
                    end=37,
                    seta="dorsal marginal head setae",
                    seta_part="head",
                    position="inserted anteriorly and close to",
                    subpart="suture",
                ),
                Subpart(
                    start=38,
                    end=56,
                    subpart="suture",
                    part="head",
                    position="dorsal",
                ),
            ],
        )

    def test_seta_position_02(self) -> None:
        self.assertEqual(
            parse("DMHS inserted posteriorly and lateral to DPHS;"),
            [
                Seta(
                    start=0,
                    end=4,
                    seta="dorsal marginal head setae",
                    seta_part="head",
                ),
                SetaMorphology(
                    start=5,
                    end=40,
                    seta="dorsal marginal head setae",
                    seta_part="head",
                    position="inserted posteriorly and lateral to",
                    subpart="dorsal principal head setae",
                ),
                Seta(
                    start=41,
                    end=45,
                    seta="dorsal principal head setae",
                    seta_part="head",
                ),
            ],
        )

    def test_seta_position_03(self) -> None:
        self.assertEqual(
            parse("(VPHS) ventrally on each side"),
            [
                Seta(
                    start=1,
                    end=5,
                    seta="ventral principal head setae",
                    seta_part="head",
                ),
                SetaMorphology(
                    start=7,
                    end=29,
                    seta="ventral principal head setae",
                    seta_part="head",
                    position="ventrally on each side",
                ),
            ],
        )

    def test_seta_position_04(self) -> None:
        self.assertEqual(
            parse("stout lateral setae"),
            [
                SetaMorphology(
                    start=0,
                    end=13,
                    seta="setae",
                    position="stout lateral",
                ),
                Seta(
                    start=14,
                    end=19,
                    seta="setae",
                ),
            ],
        )
