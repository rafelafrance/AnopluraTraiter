import unittest

from anoplura.rules.plate_seta import PlateSeta
from tests.setup import parse


class TestPlateSeta(unittest.TestCase):
    def test_plate_seta_01(self):
        self.assertEqual(
            parse("plates VI and VII each with 2 long apical setae"),
            [
                PlateSeta(
                    plates=[6, 7],
                    seta="long apical setae",
                    seta_count_low=2,
                    seta_count_group="each with",
                    start=0,
                    end=47,
                )
            ],
        )
