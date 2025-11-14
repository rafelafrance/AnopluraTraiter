from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class PartMean(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    # ---------------------

    part_mean: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_mean_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_mean_patterns",
            compiler=cls.part_mean_patterns(),
            overwrite=["size"],
        )
        add.cleanup_pipe(nlp, name="part_mean_cleanup")

    @classmethod
    def part_mean_patterns(cls) -> None:
        return [
            Compiler(
                label="part_mean",
                on_match="part_mean_match",
                keep="part_mean",
                decoder={
                    "label": {"ENT_TYPE": "mean_term"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " label+ size+ ",
                ],
            ),
        ]

    @classmethod
    def part_mean_match(cls, ent: Span) -> "PartMean":
        mean = None

        for e in ent.ents:
            if e.label_ == "size":
                mean = e._.trait.dims

        return cls.from_ent(ent, part_mean=mean)


@registry.misc("part_mean_match")
def part_mean_match(ent: Span) -> PartMean:
    return PartMean.part_mean_match(ent)
