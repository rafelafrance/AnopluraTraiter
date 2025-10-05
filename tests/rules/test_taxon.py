import unittest

from anoplura.rules.sex import Sex
from anoplura.rules.taxon import Taxon
from tests.setup import parse


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self) -> None:
        self.assertEqual(
            parse("females of L. CLAYTONI sp. nov., ."),
            [
                Sex(sex="female", start=0, end=7),
                Taxon(
                    taxon="Lemurpediculus claytoni",
                    rank="species",
                    start=11,
                    end=22,
                ),
            ],
        )

    def test_taxon_02(self) -> None:
        self.assertEqual(
            parse("four known species of Abrocomaphthirus"),
            [
                Taxon(
                    taxon="Abrocomaphthirus",
                    rank="genus",
                    start=22,
                    end=38,
                ),
            ],
        )
