import unittest

from anoplura.rules.save.tergite_seta import TergiteSeta
from tests.setup import parse


class TestTergiteSeta(unittest.TestCase):
    def test_tergite_seta_01(self):
        self.assertEqual(
            parse("tergites 3-6 each with 8-11 TeAS;"),
            [
                TergiteSeta(
                    tergites=[3, 4, 5, 6],
                    seta_count_low=8,
                    seta_count_high=11,
                    seta="tergal abdominal setae",
                    seta_count_group="each with",
                    start=0,
                    end=32,
                )
            ],
        )
