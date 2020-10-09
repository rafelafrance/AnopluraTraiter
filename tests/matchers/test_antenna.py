"""Test antenna trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestAntenna(unittest.TestCase):
    """Test range trait matcher."""

    def test_antenna_01(self):
        self.assertEqual(
            NLP('Head suboval; antennae unmodified in males.'),
            [{'part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'unmodified in males',
              'trait': 'antenna', 'start': 14, 'end': 43}]
        )

    def test_antenna_02(self):
        self.assertEqual(
            NLP(shorten("""
                Antennae five-segmented with basal segment wider than long and
                much larger than second segment; fourth segment slightly
                extended posterolaterally.
                """)),
            [{'description': ('five-segmented with basal segment wider than '
                              'long and much larger than second segment'),
              'trait': 'antenna', 'start': 0, 'end': 95}]
        )

    def test_antenna_03(self):
        self.assertEqual(
            NLP(shorten("""
                Head lacking eyes, with 5-segmented antennae which are often
                sexually dimorphic.
                """)),
            [{'end': 4, 'part': 'head', 'start': 0, 'trait': 'body_part'},
             {'description': '5-segmented which are often sexually dimorphic',
              'trait': 'antenna', 'start': 24, 'end': 80}]
        )

    def test_antenna_04(self):
        self.assertEqual(
            NLP(shorten("""
                third antennal segment modified with anterodorsal projection.
                """)),
            [{'description': ('third antennal segment modified with '
                              'anterodorsal projection'),
              'trait': 'antenna', 'start': 0, 'end': 61}]
        )

    def test_antenna_05(self):
        self.assertEqual(
            NLP(shorten("""Antennal segments 3-5 not fused;""")),
            [{'description': 'antennal segments 3-5 not fused',
              'trait': 'antenna', 'start': 0, 'end': 32}]
        )
