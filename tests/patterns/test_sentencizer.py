# """Test the header matcher."""
# # pylint: disable=missing-function-docstring
# import unittest
#
# from traiter.util import shorten
#
# from tests.setup import NLP
#
#
# class TestSegmenter(unittest.TestCase):
#     """Test the plant color trait parser."""
#
#     def test_sentencizer_01(self):
#         text = shorten(
#             """
#             It was common “along a tiny stream.” Argia apicalis.
#         """
#         )
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 2)
#
#     def test_sentencizer_02(self):
#         text = shorten("""(Dunn et al. 2009, Jørgensen 2015).""")
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 1)
#
#     def test_sentencizer_03(self):
#         text = """Abbreviated
#             when
#             subsequently mentioned."""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 1)
#
#     def test_sentencizer_04(self):
#         text = """Abstract more words."""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 1)
#
#     def test_sentencizer_05(self):
#         text = """abstract more words."""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 1)
#
#     def test_sentencizer_06(self):
#         text = """Something Abstract more words."""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 1)
#
#     def test_sentencizer_07(self):
#         text = """Something. Materials and Methods more words."""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 2)
#
#     #     def test_sentencizer_08(self):
#     #         text = """new lice. References Cited
#     # Blanco,"""
#     #         doc = NLP(text)
#     #         sents = list(doc.sents)
#     #         self.assertEqual(len(sents), 3)
#
#     def test_sentencizer_09(self):
#         text = """(2013). Ectoparasites"""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 2)
#
#     def test_sentencizer_10(self):
#         text = """earwig.
# The"""
#         doc = NLP(text)
#         sents = list(doc.sents)
#         self.assertEqual(len(sents), 2)
