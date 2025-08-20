from dataclasses import dataclass, field

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaSize(Base):
    seta: str | None = None
    seta_part: str | None = None
    dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.context_pipe(
            nlp,
            name="seta_size_patterns",
            compiler=cls.seta_size_patterns(),
            overwrite=["size"],
        )

    @classmethod
    def seta_size_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="seta_size",
                on_match="seta_size_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "seta": {"ENT_TYPE": "seta"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " (? seta+ )? size+ ",
                ],
            ),
        ]

    @classmethod
    def seta_size_match(cls, ent: Span) -> "SetaSize":
        dims, seta_part, seta = None, None, None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims

            elif e.label_ == "seta":
                seta_part = e._.trait.seta_part
                seta = e._.trait.seta

        return cls.from_ent(ent, seta_part=seta_part, seta=seta, dims=dims)


@registry.misc("seta_size_match")
def seta_size_match(ent: Span) -> SetaSize:
    return SetaSize.seta_size_match(ent)
