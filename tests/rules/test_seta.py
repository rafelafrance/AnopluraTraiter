import unittest

from anoplura.rules.seta import Seta
from tests.setup import parse


class TestSeta(unittest.TestCase):
    def test_seta_01(self):
        self.assertEqual(
            parse("dachs"),
            [Seta(seta="dorsal accessory head setae", start=0, end=5)],
        )

    def test_seta_02(self):
        self.assertEqual(
            parse("dorsal accessory head setae"),
            [Seta(seta="dorsal accessory head setae", start=0, end=27)],
        )

    def test_setae_03(self):
        self.assertEqual(
            parse("Dorsal Mesothoracic Setae;"),
            [
                Seta(
                    seta="dorsal mesothoracic setae",
                    start=0,
                    end=25,
                ),
            ],
        )
