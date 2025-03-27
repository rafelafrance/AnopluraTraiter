import unittest

from anoplura.rules.body_part import BodyPart
from tests.setup import parse


class TestSternite(unittest.TestCase):
    def test_sternite_seta_01(self):
        self.assertEqual(
            parse("dorsal head suture"),
            [BodyPart(body_part="dorsal head suture", start=0, end=18)],
        )
