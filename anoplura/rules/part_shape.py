from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartShape(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    part: str | None = None
    part_shape: str | None = None
    part_shape_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_shape_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_shape_patterns",
            compiler=cls.part_shape_patterns(),
            overwrite=["part", "shape"],
        )
        add.cleanup_pipe(nlp, name="part_shape_cleanup")

    @classmethod
    def part_shape_patterns(cls):
        return [
            Compiler(
                label="part_shape",
                on_match="part_shape_match",
                keep="part_shape",
                decoder={
                    "shape": {"ENT_TYPE": "shape"},
                    "part": {"ENT_TYPE": "part"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " shape+ part+ pos* ",
                ],
            ),
        ]

    @classmethod
    def part_shape_match(cls, ent):
        part, shape, pos = None, None, None

        for e in ent.ents:
            if e.label_ == "shape":
                text = e.text.lower()
                shape = cls.replace.get(text, text)
            elif e.label_ == "position":
                text = e.text.lower()
                pos = cls.replace.get(text, text)
            elif e.label_ == "part":
                part = e._.trait.part

        return cls.from_ent(ent, part=part, part_shape=shape, part_shape_position=pos)


@registry.misc("part_shape_match")
def part_shape_match(ent):
    return PartShape.part_shape_match(ent)
