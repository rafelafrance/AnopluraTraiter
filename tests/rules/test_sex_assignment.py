import unittest

from anoplura.rules.seta import Seta
from anoplura.rules.sex import Sex
from tests.setup import parse


class TestSexAssignment(unittest.TestCase):
    def test_sex_assignment_01(self):
        self.assertEqual(
            parse("male dachs"),
            [
                Sex(sex="male", start=0, end=4),
                Seta(seta="dorsal accessory head setae", sex="male", start=5, end=10),
            ],
        )
