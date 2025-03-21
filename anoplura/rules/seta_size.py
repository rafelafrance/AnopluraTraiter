from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaSize(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    seta: str | None = None
    dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_size_patterns",
            compiler=cls.seta_size_patterns(),
            overwrite=["size", "seta"],
        )

    @classmethod
    def seta_size_patterns(cls):
        return [
            Compiler(
                label="seta_size",
                on_match="seta_size_match",
                keep="seta_size",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "seta": {"ENT_TYPE": "seta"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " (? seta )? size+ ",
                ],
            ),
        ]

    @classmethod
    def seta_size_match(cls, ent):
        seta, dims = None, None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims
            elif e.label_ == "seta":
                seta = e._.trait.seta

        return cls.from_ent(ent, dims=dims, seta=seta)


@registry.misc("seta_size_match")
def seta_size_match(ent):
    return SetaSize.seta_size_match(ent)
