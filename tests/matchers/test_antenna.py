"""Test antenna trait matcher."""

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestAntenna(unittest.TestCase):
    """Test range trait matcher."""

    def test_antenna_01(self):
        self.assertEqual(
            #    0123456789 123
            NLP('Head suboval; antennae unmodified in males;.'),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'suboval', 'body_part': 'head',
              'trait': 'description', 'start': 5, 'end': 12},
             {'body_part': 'antenna', 'trait': 'body_part',
              'start': 14, 'end': 22},
             {'description': 'unmodified in males', 'body_part': 'antenna',
              'trait': 'description', 'start': 23, 'end': 42}]
        )

    def test_antenna_02(self):
        self.assertEqual(
            NLP(shorten("""
                Antennae five-segmented with basal segment wider than long and
                much larger than second segment; fourth segment slightly
                extended posterolaterally.
                """)),
            [{'body_part': 'antenna', 'trait': 'body_part',
              'start': 0, 'end': 8},
             {
                 'description': shorten("""
                    five-segmented with basal segment wider than
                    long and much larger than second segment
                    """),
                 'body_part': 'antenna', 'trait': 'description',
                 'start': 9, 'end': 94}]
        )

    def test_antenna_03(self):
        self.assertEqual(
            NLP(shorten("""
                Head lacking eyes, with 5-segmented antennae which are often
                sexually dimorphic.
                """)),
            [{'body_part': 'head', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'description': 'lacking eyes', 'body_part': 'head',
              'trait': 'description', 'start': 5, 'end': 17},
             {'body_part': '5-segmented antennae',
              'trait': 'body_part', 'start': 24, 'end': 44},
             {'description': 'which are often sexually dimorphic',
              'body_part': '5-segmented antennae',
              'trait': 'description', 'start': 45, 'end': 79}]
        )

    def test_antenna_04(self):
        self.assertEqual(
            NLP(shorten("""
                third antennal segment modified with anterodorsal projection.
                """)),
            [{'body_part': 'third antennal segment',
              'trait': 'body_part', 'start': 0, 'end': 22},
             {'description': 'modified with anterodorsal projection',
              'body_part': 'third antennal segment',
              'trait': 'description', 'start': 23, 'end': 60}]
        )

    def test_antenna_05(self):
        self.assertEqual(
            NLP(shorten("""Antennal segments 3-5 not fused;""")),
            [{'body_part': 'antennal segments 3-5',
              'trait': 'body_part', 'start': 0, 'end': 21},
             {'description': 'not fused',
              'body_part': 'antennal segments 3-5',
              'trait': 'description', 'start': 22, 'end': 31}]
        )
