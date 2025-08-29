import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.seta_position import SetaPosition
from tests.setup import parse


class TestSeta(unittest.TestCase):
    def test_seta_01(self) -> None:
        self.assertEqual(
            parse("dachs"),
            [
                Seta(
                    seta="dorsal accessory head setae",
                    seta_part="head",
                    start=0,
                    end=5,
                )
            ],
        )

    def test_seta_02(self) -> None:
        self.assertEqual(
            parse("dorsal accessory head setae"),
            [
                Seta(
                    seta="dorsal accessory head setae",
                    seta_part="head",
                    start=0,
                    end=27,
                )
            ],
        )

    def test_setae_03(self) -> None:
        self.assertEqual(
            parse("Dorsal Mesothoracic Setae;"),
            [
                Seta(
                    seta="dorsal mesothoracic setae",
                    seta_part="thorax",
                    start=0,
                    end=25,
                ),
            ],
        )

    def test_setae_04(self) -> None:
        self.assertEqual(
            parse("Long curved Setae;"),
            [
                SetaPosition(
                    start=0,
                    end=11,
                    seta="setae",
                    position="long curved",
                ),
                Seta(
                    start=12,
                    end=17,
                    seta="setae",
                ),
            ],
        )
