from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class Mean(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
        Path(__file__).parent / "terms" / "dimension_terms.csv",
    ]
    # ---------------------

    mean: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="mean_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="mean_patterns",
            compiler=cls.mean_patterns(),
            overwrite=["size"],
        )
        add.cleanup_pipe(nlp, name="mean_cleanup")

    @classmethod
    def mean_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="mean",
                on_match="mean_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "label": {"ENT_TYPE": "mean_term"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " label+ ,? size+ ",
                ],
            ),
        ]

    @classmethod
    def mean_match(cls, ent: Span) -> "Mean":
        mean = None

        for e in ent.ents:
            if e.label_ == "size":
                mean = e._.trait.dims

        return cls.from_ent(ent, mean=mean)


@registry.misc("mean_match")
def mean_match(ent: Span) -> Mean:
    return Mean.mean_match(ent)
