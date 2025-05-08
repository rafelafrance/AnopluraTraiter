import unittest

from anoplura.rules.specimen_type import SpecimenType
from tests.setup import parse


class TestSpecimenType(unittest.TestCase):
    def test_specimen_type_01(self):
        self.assertEqual(
            parse("Holotype (female)"),
            [
                SpecimenType(
                    specimen_type="holotype",
                    specimen_sex="female",
                    start=0,
                    end=17,
                ),
            ],
        )
