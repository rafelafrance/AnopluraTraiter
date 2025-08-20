import unittest

from anoplura.rules.specimen_type import SpecimenType
from tests.setup import parse


class TestSpecimenType(unittest.TestCase):
    def test_specimen_type_01(self) -> None:
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

    def test_specimen_type_02(self) -> None:
        self.assertEqual(
            parse("Other paratypes are in the collections"),
            [
                SpecimenType(
                    specimen_type="paratypes",
                    specimen_type_other="other",
                    start=0,
                    end=15,
                ),
            ],
        )
