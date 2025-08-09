from dataclasses import dataclass, field

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class PartSize(Base):
    # Class vars ----------
    # ---------------------

    part: str = None
    which: str | list[str] | list[int] | None = None
    dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_size_patterns",
            compiler=cls.part_size_patterns(),
            overwrite=["size"],
        )

    @classmethod
    def part_size_patterns(cls):
        return [
            Compiler(
                label="part_size",
                on_match="part_size_match",
                decoder={
                    "part": {"ENT_TYPE": "part"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " part+ size+ ",
                ],
            ),
        ]

    @classmethod
    def part_size_match(cls, ent):
        dims, part, which = None, None, None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims

            elif e.label_ == "part":
                part = e._.trait.part
                which = e._.trait.which

        return cls.from_ent(ent, part=part, which=which, dims=dims)


@registry.misc("part_size_match")
def part_size_match(ent):
    return PartSize.part_size_match(ent)
