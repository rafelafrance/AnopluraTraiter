import unittest

from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_description import SubpartDescription
from tests.setup import parse


class TestSubpartDescription(unittest.TestCase):
    def test_subpart_description_01(self):
        self.assertEqual(
            parse("""rounded anterolateral margins"""),
            [
                SubpartDescription(
                    start=0,
                    end=7,
                    subpart="margin",
                    description=["rounded"],
                    position="anterolateral",
                ),
                Subpart(
                    start=8,
                    end=29,
                    subpart="margin",
                    position="anterolateral",
                ),
            ],
        )

    def test_subpart_description_02(self):
        self.assertEqual(
            parse("""broad spur-like ridge posteriorly"""),
            [
                SubpartDescription(
                    start=0,
                    end=15,
                    subpart="ridge",
                    description=["broad spur-like"],
                ),
                Subpart(
                    start=16,
                    end=21,
                    subpart="ridge",
                ),
            ],
        )
