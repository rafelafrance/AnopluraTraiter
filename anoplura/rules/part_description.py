from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
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
    descr: ClassVar[list[str]] = [
        "shape_term",
        "size_term",
        "linker",
        "separator",
        "subpart",
        "position",
        *other_parts,
    ]
    dash: ClassVar[list[str]] = ["-", "–", "—"]
    # ----------------------

    part: str | None = None
    which: str | list[str] | list[int] | None = None
    shape: str | None = None
    position: str | None = None
    morphology: str | None = None
    reference_part: str | None = None
    reference_which: str | list[str] | list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_description_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="part_description_patterns",
            compiler=cls.part_description_patterns(),
            overwrite=["count", "number_suffix", *cls.descr],
        )
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="part_description_patterns2",
            compiler=cls.part_description_patterns2(),
            overwrite=cls.descr,
        )
        add.cleanup_pipe(nlp, name="part_description_cleanup")

    @classmethod
    def part_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_description",
                on_match="part_description_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "9": {"ENT_TYPE": "count"},
                    "descr": {"ENT_TYPE": {"IN": cls.descr}},
                    "suffix": {"ENT_TYPE": "number_suffix"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                },
                patterns=[
                    " part+ descr+ ",
                    " descr+ part+ ",
                    " part+ descr+ part+ ",
                    " part+ 9+ -* suffix+ ",
                ],
            ),
        ]

    @classmethod
    def part_description_patterns2(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_description",
                on_match="part_description_match",
                decoder={
                    "descr": {"ENT_TYPE": {"IN": cls.descr}},
                    "prev_shape": {"ENT_TYPE": "part_description"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                },
                patterns=[
                    " prev_shape+ part+ descr+ ",
                ],
            ),
        ]

    @classmethod
    def part_description_match(cls, ent: Span) -> "PartDescription":
        part, which, ref_part, ref_which = None, None, None, None
        shape, morph = [], []
        reject = True

        for e in ent.ents:
            if e.label_ in PARTS:
                if not part:
                    part = e._.trait.part
                    which = e._.trait.which
                else:
                    ref_part = e._.trait.part
                    ref_which = e._.trait.which

            elif e.label_ in ("count", "number_suffix"):
                morph.append(e.text.lower())
                reject = False

            elif e.label_ in cls.descr:
                shape.append(e.text.lower())
                if e.label_ not in ("separator", "linker"):
                    reject = False

        if reject:
            raise reject_match.RejectMatch

        morph = "-".join(morph)
        morph = morph if morph else None

        shape = " ".join(shape)
        shape = shape.replace(" ,", ",").removesuffix(",")
        shape = shape if shape else None

        return cls.from_ent(
            ent,
            part=part,
            which=which,
            shape=shape,
            morphology=morph,
            reference_part=ref_part,
            reference_which=ref_which,
        )


@registry.misc("part_description_match")
def part_description_match(ent: Span) -> PartDescription:
    return PartDescription.part_description_match(ent)
