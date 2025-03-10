import unittest

from anoplura.rules.seta import Seta
from tests.setup import parse


class TestSeta(unittest.TestCase):
    def test_seta_01(self):
        self.assertEqual(
            parse("dachs"),
            [Seta(seta="dorsal accessory head setae", start=0, end=5)],
        )

    def test_seta_02(self):
        self.assertEqual(
            parse("dorsal accessory head setae"),
            [Seta(seta="dorsal accessory head setae", start=0, end=27)],
        )


#     # def test_body_part_01(self):
#     #     self.assertEqual(
#     #         parse("head, thorax, abdomen"),
#     #         [
#     #             {
#     #                 "body_part": "head, thorax, abdomen",
#     #                 "trait": "body_part",
#     #                 "start": 0,
#     #                 "end": 21,
#     #             }
#     #         ],
#     #     )
#     #
#     # def test_body_part_02(self):
#     #     self.assertEqual(
#     #         parse("missing eyes"),
#     #         [
#     #             {
#     #                 "body_part": "missing eye",
#     #                 "missing": True,
#     #                 "trait": "body_part",
#     #                 "start": 0,
#     #                 "end": 12,
#     #             }
#     #         ],
#     #     )
#
#     # def test_body_part_01(self):
#     #     self.assertEqual(
#     #         parse("fourth segment"),
#     #         [
#     #             {
#     #                 "body_part": "fourth segment",
#     #                 "trait": "body_part",
#     #                 "start": 0,
#     #                 "end": 14,
#     #             }
#     #         ],
#     #     )
