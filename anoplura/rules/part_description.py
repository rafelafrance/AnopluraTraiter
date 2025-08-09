from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class PartDescription(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    other_parts: ClassVar[list[str]] = [
        "gonopods",
        "plates",
        "segments",
        "sternites",
        "tergites",
    ]
    # ----------------------

    part: str | None = None
    which: str | list[str] | list[int] | None = None
    description: list[str] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_description_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_descr_patterns",
            compiler=cls.part_descr_patterns(),
            overwrite=["shape_term", "size_term", "position", *cls.other_parts],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_description_patterns",
            compiler=cls.part_description_patterns(),
            overwrite=["part_descr"],
        )
        add.cleanup_pipe(nlp, name="part_description_cleanup")

    @classmethod
    def part_descr_patterns(cls):
        return [
            Compiler(
                label="part_descr",
                is_temp=True,
                on_match="part_descr_match",
                decoder={
                    "adj": {"POS": {"IN": ["ADJ", "ADV"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "other_parts": {"ENT_TYPE": {"IN": cls.other_parts}},
                    "shape": {"ENT_TYPE": {"IN": ["shape_term", "size_term"]}},
                },
                patterns=[
                    " adj* pos+ ",
                    " adj* shape+ pos* ",
                    " adj* shape+ other_parts* ",
                ],
            ),
        ]

    @classmethod
    def part_description_patterns(cls):
        return [
            Compiler(
                label="part_description",
                on_match="part_description_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "descr": {"ENT_TYPE": "part_descr"},
                },
                patterns=[
                    " descr+ part+ ",
                    " part+  descr+ ",
                    " part+  descr+ ,+ descr+ ",
                ],
            ),
        ]

    @classmethod
    def part_descr_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def part_description_match(cls, ent):
        part, which = None, None
        descr = []

        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "part_descr":
                descr.append(e.text.lower())

        return cls.from_ent(ent, part=part, which=which, description=descr)


@registry.misc("part_description_match")
def part_description_match(ent):
    return PartDescription.part_description_match(ent)


@registry.misc("part_descr_match")
def part_descr_match(ent):
    return PartDescription.part_descr_match(ent)
