import unittest

from anoplura.rules.seta_position import SetaPosition
from tests.setup import parse


class TestSetaPosition(unittest.TestCase):
    def test_seta_position_01(self):
        self.assertEqual(
            parse("(VPHS) ventrally on each side."),
            [
                SetaPosition(
                    seta="ventral principal head setae",
                    seta_position="ventrally",
                    seta_position_group="on each side",
                    seta_position_group_count=2,
                    start=0,
                    end=29,
                ),
            ],
        )
