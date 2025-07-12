import unittest

from anoplura.rules.count import Count
from anoplura.rules.sex import Sex
from anoplura.rules.taxon import Taxon
from tests.setup import parse


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        self.assertEqual(
            parse("females of L. CLAYTONI sp. nov., ."),
            [
                Sex(sex="female", start=0, end=7),
                Taxon(
                    taxon="Lemurpediculus claytoni",
                    rank="species",
                    group="anoplura",
                    start=11,
                    end=22,
                ),
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            parse("four known species of Abrocomaphthirus"),
            [
                Count(start=0, end=4, count_low=4),
                Taxon(
                    taxon="Abrocomaphthirus",
                    rank="genus",
                    group="anoplura",
                    start=22,
                    end=38,
                ),
            ],
        )
