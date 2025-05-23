import unittest

from traiter.pylib.rules.lat_long import LatLong

from tests.setup import parse


class TestLatLong(unittest.TestCase):
    def test_lat_long_01(self):
        self.assertEqual(
            parse("[10°18'N, 84°47'W],"),
            [
                LatLong(
                    lat_long="10° 18' N, 84° 47' W",
                    start=1,
                    end=18,
                )
            ],
        )
