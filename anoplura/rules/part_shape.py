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
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    sep: ClassVar[list[str]] = [",", "and", "is"]
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
                    ",": {"LOWER": {"IN": cls.sep}},
                    "fill": {"POS": {"IN": ["ADP", "ADV"]}},
                    "rel": {"ENT_TYPE": "relative_term"},
                    "shape": {"ENT_TYPE": "shape"},
                    "part": {"ENT_TYPE": "part"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " shape+ part+ pos* ",
                    " part+ fill* rel+ fill* rel+ ,* fill* rel* shape+ pos* ",
                ],
            ),
        ]

    @classmethod
    def part_shape_match(cls, ent):
        part, shape, pos = [], [], []

        for t in ent:
            if t._.term == "bug_part":
                text = cls.replace.get(t.lower_, t.lower_)
                part.append(text)
            elif t._.term == "position":
                pos.append(t.lower_)
            else:
                shape.append(t.lower_)

        part = " ".join(part)
        part = cls.replace.get(part, part)

        pos = " ".join(pos)

        shape = " ".join(shape)
        shape = shape.replace(" , ", ", ")

        return cls.from_ent(ent, part=part, part_shape=shape, part_shape_position=pos)


@registry.misc("part_shape_match")
def part_shape_match(ent):
    return PartShape.part_shape_match(ent)
