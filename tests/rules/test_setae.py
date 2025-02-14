import unittest

from anoplura.pylib.rules.setae import Setae
from tests.setup import parse


class TestSetae(unittest.TestCase):
    def test_setae_01(self):
        self.assertEqual(
            parse("dachs"),
            [Setae(setae="dorsal accessory head setae", start=0, end=5)],
        )

    def test_setae_02(self):
        self.assertEqual(
            parse("dorsal accessory head setae"),
            [Setae(setae="dorsal accessory head setae", start=0, end=27)],
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
