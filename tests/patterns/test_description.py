"""Test description trait matcher."""
import unittest

from tests.setup import test_traits


class TestDescription(unittest.TestCase):
    """Test description trait matcher."""

    # def test_description_01(self):
    #     self.assertEqual(
    #         test_traits(
    #             """
    #             Head: More heavily sclerotized along anterior margin;
    #             longer than broad with squarish, slightly convex anterior margin.
    #             """
    #         ),
    #         [
    #             {"body_part": "head", "trait": "body_part", "start": 0, "end": 4},
    #             {
    #                 "body_part": "anterior margin",
    #                 "trait": "body_part",
    #                 "start": 37,
    #                 "end": 52,
    #             },
    #             {
    #                 "body_part": "anterior margin",
    #                 "trait": "body_part",
    #                 "start": 103,
    #                 "end": 118,
    #                 "description": "longer than broad with squarish, slightly convex",
    #             },
    #         ],
    #     )

    # def test_description_02(self):
    #     self.assertEqual(
    #         test_traits(
    #             """
    #             Thorax slightly wider and elongate.
    #             Thoracic sternal plate extended anteriorly.
    #             """
    #         ),
    #         [
    #             {
    #                 "body_part": "thorax",
    #                 "trait": "body_part",
    #                 "start": 0,
    #                 "end": 6,
    #                 "description": "slightly wider and elongate",
    #             },
    #             {
    #                 "body_part": "thoracic sternal plate",
    #                 "trait": "body_part",
    #                 "start": 36,
    #                 "end": 58,
    #                 "description": "extended anteriorly",
    #             },
    #         ],
    #     )

    def test_description_03(self):
        self.assertEqual(
            test_traits("""Stuff on head."""),
            [
                {
                    "body_part": "head",
                    "trait": "body_part",
                    "start": 9,
                    "end": 13,
                    "description": "stuff on",
                }
            ],
        )

    def test_description_04(self):
        self.assertEqual(
            test_traits("""Stuff on head but not on top."""),
            [
                {
                    "body_part": "head",
                    "trait": "body_part",
                    "start": 9,
                    "end": 13,
                    "description": ["stuff on", "but not on top"],
                }
            ],
        )
