import unittest

from traiter.rules.elevation import Elevation

from anoplura.rules.base import as_dict
from tests.setup import parse


class TestElevation(unittest.TestCase):
    def test_elevation_01(self) -> None:
        traits = parse("elevation 1,500 m")
        self.assertEqual(
            traits,
            [Elevation(elevation=1500.0, units="m", start=0, end=17)],
        )
        self.assertEqual(as_dict(traits[0]), {"elevation": 1500.0, "units": "m"})
