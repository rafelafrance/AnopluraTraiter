import unittest

from anoplura.pylib.rules.body_part import BodyPart
from tests.setup import parse


class TestBodyPart(unittest.TestCase):
    def test_body_part_01(self):
        self.assertEqual(
            parse("dachs"),
            [BodyPart(body_part="dorsal accessory head setae", start=0, end=5)],
        )


#
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
