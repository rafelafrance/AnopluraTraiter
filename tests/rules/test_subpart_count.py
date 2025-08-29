import unittest

from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_count import SubpartCount
from tests.setup import parse


class TestSubpartCount(unittest.TestCase):
    def test_subpart_count_01(self) -> None:
        self.assertEqual(
            parse("One small lobe"),
            [
                SubpartCount(
                    start=0,
                    end=3,
                    subpart="lobe",
                    count_low=1,
                ),
                Subpart(start=4, end=14, subpart="lobe", size="small"),
            ],
        )
