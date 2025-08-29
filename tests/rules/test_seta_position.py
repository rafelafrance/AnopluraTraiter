import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_position import SetaPosition
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
                SetaPosition(
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
                    which="dorsal",
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
                SetaPosition(
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
                SetaPosition(
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
            parse("narrow central setae and stout lateral setae"),
            [
                SetaPosition(
                    start=0,
                    end=14,
                    seta="setae",
                    position="narrow central",
                ),
                Seta(
                    start=15,
                    end=20,
                    seta="setae",
                ),
                SetaPosition(
                    start=25,
                    end=38,
                    seta="setae",
                    position="stout lateral",
                ),
                Seta(
                    start=39,
                    end=44,
                    seta="setae",
                ),
            ],
        )
