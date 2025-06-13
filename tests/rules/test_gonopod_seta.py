import unittest

from anoplura.rules.gonopod_seta import GonopodSeta
from tests.setup import parse


class TestGonopodSeta(unittest.TestCase):
    def test_gonopod_seta_01(self):
        self.assertEqual(
            parse("1 seta inserted immediately lateral to gonopods IX on each side;"),
            [
                GonopodSeta(
                    gonopods=[9],
                    seta_count_low=1,
                    seta_count_group="on each side",
                    seta="seta",
                    seta_count_position="lateral",
                    start=0,
                    end=63,
                )
            ],
        )

    def test_gonopod_seta_02(self):
        self.assertEqual(
            parse("3 rows of setae immediately anterior to gonopods IX on each side;"),
            [
                GonopodSeta(
                    gonopods=[9],
                    seta_count_low=3,
                    seta_count_group="on each side",
                    seta_count_position="anterior",
                    seta="setae",
                    start=0,
                    end=64,
                )
            ],
        )
