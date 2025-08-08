import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_position import SetaPosition
from anoplura.rules.subpart import Subpart
from tests.setup import parse


class TestSetaPosition(unittest.TestCase):
    def test_seta_position_01(self):
        self.assertEqual(
            parse("DMHS inserted anteriorly and close to dorsal head suture"),
            [
                Seta(start=0, end=4, seta="dorsal marginal head setae", part="head"),
                SetaPosition(
                    start=5,
                    end=37,
                    seta="dorsal marginal head setae",
                    part="head",
                    position="inserted anteriorly and close to",
                    other="suture",
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

    def test_seta_position_02(self):
        self.assertEqual(
            parse("DMHS inserted posteriorly and lateral to DPHS;"),
            [
                Seta(
                    start=0,
                    end=4,
                    seta="dorsal marginal head setae",
                    part="head",
                ),
                SetaPosition(
                    start=5,
                    end=40,
                    seta="dorsal marginal head setae",
                    part="head",
                    position="inserted posteriorly and lateral to",
                    other="dorsal principal head setae",
                ),
                Seta(
                    start=41,
                    end=45,
                    seta="dorsal principal head setae",
                    part="head",
                ),
            ],
        )

    def test_seta_position_03(self):
        self.assertEqual(
            parse("(VPHS) ventrally on each side"),
            [
                Seta(
                    start=1,
                    end=5,
                    seta="ventral principal head setae",
                    part="head",
                ),
                SetaPosition(
                    start=7,
                    end=29,
                    seta="ventral principal head setae",
                    part="head",
                    position="ventrally on each side",
                ),
            ],
        )
