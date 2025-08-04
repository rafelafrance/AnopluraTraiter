from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class PartShape(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "shape_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    part: str | None = None
    which: list[int] | None = None
    shape: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_shape_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_shape_itself_patterns",
            compiler=cls.part_shape_itself_patterns(),
            overwrite=["shape_term"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_shape_patterns",
            compiler=cls.part_shape_patterns(),
            overwrite=["part_shape_itself"],
        )
        add.cleanup_pipe(nlp, name="part_shape_cleanup")

    @classmethod
    def part_shape_itself_patterns(cls):
        return [
            Compiler(
                label="part_shape_itself",
                is_temp=True,
                on_match="part_shape_itself_match",
                decoder={
                    "shape": {"ENT_TYPE": "shape_term"},
                },
                patterns=[
                    " shape+ ",
                ],
            ),
        ]

    @classmethod
    def part_shape_patterns(cls):
        return [
            Compiler(
                label="part_shape",
                on_match="part_shape_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "shape": {"ENT_TYPE": "part_shape_itself"},
                },
                patterns=[
                    " shape+ part+ ",
                ],
            ),
        ]

    @classmethod
    def part_shape_itself_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def part_shape_match(cls, ent):
        part, which = None, None
        shape = []

        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ == "part_shape_itself":
                text = e.text.lower()
                shape.append(cls.replace.get(text, text))

        shape = " ".join(shape) if shape else None

        return cls.from_ent(ent, part=part, which=which, shape=shape)


@registry.misc("part_shape_match")
def part_shape_match(ent):
    return PartShape.part_shape_match(ent)


@registry.misc("part_shape_itself_match")
def part_shape_itself_match(ent):
    return PartShape.part_shape_itself_match(ent)
