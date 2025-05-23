import unittest

from traiter.pylib.rules.elevation import Elevation

from tests.setup import parse


class TestElevation(unittest.TestCase):
    def test_elevation_01(self):
        self.assertEqual(
            parse("elevation 1,500 m"),
            [
                Elevation(
                    elevation=1500.0,
                    units="m",
                    start=0,
                    end=17,
                )
            ],
        )
