from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class PartSize(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    sep: ClassVar[list[str]] = [",", "=", "is"]
    # ---------------------

    part: str | None = None
    part_dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_size_patterns",
            compiler=cls.part_size_patterns(),
            overwrite=["size", "part"],
        )

    @classmethod
    def part_size_patterns(cls):
        return [
            Compiler(
                label="part_size",
                on_match="part_size_match",
                keep="part_size",
                decoder={
                    "part": {"ENT_TYPE": "part"},
                    "size": {"ENT_TYPE": "size"},
                    ",": {"LOWER": {"IN": cls.sep}},
                },
                patterns=[
                    " part+ ,* size+ ",
                ],
            ),
        ]

    @classmethod
    def part_size_match(cls, ent):
        part, dims = None, None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims
            elif e.label_ == "part":
                part = e._.trait.part

        return cls.from_ent(ent, part_dims=dims, part=part)


@registry.misc("part_size_match")
def part_size_match(ent):
    return PartSize.part_size_match(ent)
