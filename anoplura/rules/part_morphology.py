from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class PartMorphology(Base):
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
    morphology: list[str] | None = None
    reference_part: str | None = None
    reference_which: str | list[str] | list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_morphology_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_morph_patterns",
            compiler=cls.part_morph_patterns(),
            overwrite=["shape_term", "size_term", "position", *cls.other_parts],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_morphology_patterns",
            compiler=cls.part_morphology_patterns(),
            overwrite=["part_morph"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_morphology_patterns2",
            compiler=cls.part_morphology_patterns2(),
            overwrite=["part_morph"],
        )
        add.cleanup_pipe(nlp, name="part_morphology_cleanup")

    @classmethod
    def part_morph_patterns(cls):
        return [
            Compiler(
                label="part_morph",
                is_temp=True,
                on_match="part_morph_match",
                decoder={
                    "and": {"ENT_TYPE": "separator"},
                    "adj": {"POS": {"IN": ["ADJ", "ADV"]}},
                    "adp": {"POS": {"IN": ["ADP"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "other_parts": {"ENT_TYPE": {"IN": cls.other_parts}},
                    "shape": {"ENT_TYPE": {"IN": ["shape_term", "size_term"]}},
                },
                patterns=[
                    " adj* pos+ ",
                    " adj* shape+ pos* ",
                    " adj* shape+ other_parts* ",
                    " adj* pos+ and+ shape+ ",
                    " adp* pos+ adp* pos+ ",
                ],
            ),
        ]

    @classmethod
    def part_morphology_patterns(cls):
        return [
            Compiler(
                label="part_morphology",
                on_match="part_morphology_match",
                decoder={
                    "and": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "morph": {"ENT_TYPE": "part_morph"},
                },
                patterns=[
                    " part+  morph+ and* morph+ ",
                    " morph+ and* morph+ part+ ",
                    " morph+ part+ ",
                    " part+  morph+ ",
                    " part+ morph+ part+ ",
                ],
            ),
        ]

    @classmethod
    def part_morphology_patterns2(cls):
        return [
            Compiler(
                label="part_morphology",
                on_match="part_morphology_match2",
                decoder={
                    "prev_morph": {"ENT_TYPE": "part_morphology"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "morph": {"ENT_TYPE": "part_morph"},
                },
                patterns=[
                    " prev_morph+ part+ morph+ ",
                ],
            ),
        ]

    @classmethod
    def part_morph_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def part_morphology_match(cls, ent):
        part, which, ref_part, ref_which = None, None, None, None
        morph = []

        for e in ent.ents:
            if e.label_ in PARTS:
                if not part:
                    part = e._.trait.part
                    which = e._.trait.which
                else:
                    ref_part = e._.trait.part
                    ref_which = e._.trait.which

            elif e.label_ == "part_morph":
                morph.append(e.text.lower())

        return cls.from_ent(
            ent,
            part=part,
            which=which,
            morphology=morph,
            reference_part=ref_part,
            reference_which=ref_which,
        )

    @classmethod
    def part_morphology_match2(cls, ent):
        part, which, ref_part, ref_which = None, None, None, None
        morph = []

        for e in ent.ents:
            if e.label_ in PARTS:
                if not part:
                    part = e._.trait.part
                    which = e._.trait.which
                else:
                    ref_part = e._.trait.part
                    ref_which = e._.trait.which

            elif e.label_ == "part_morph":
                morph.append(e.text.lower())

        return cls.from_ent(
            ent,
            part=part,
            which=which,
            morphology=morph,
            reference_part=ref_part,
            reference_which=ref_which,
        )


@registry.misc("part_morphology_match")
def part_morphology_match(ent):
    return PartMorphology.part_morphology_match(ent)


@registry.misc("part_morph_match")
def part_morph_match(ent):
    return PartMorphology.part_morph_match(ent)


@registry.misc("part_morphology_match2")
def part_morphology_match2(ent):
    return PartMorphology.part_morphology_match2(ent)
