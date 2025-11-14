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
class PartRange(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    # ---------------------

    part_range: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_range_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="part_range_patterns",
            compiler=cls.part_range_patterns(),
            overwrite=["size"],
        )
        add.cleanup_pipe(nlp, name="part_range_cleanup")

    @classmethod
    def part_range_patterns(cls) -> None:
        return [
            Compiler(
                label="part_range",
                on_match="part_range_match",
                keep="part_range",
                decoder={
                    "label": {"ENT_TYPE": "range_term"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " label size+ ",
                ],
            ),
        ]

    @classmethod
    def part_range_match(cls, ent: Span) -> "PartRange":
        range_ = None

        for e in ent.ents:
            if e.label_ == "size":
                range_ = e._.trait.dims

        return cls.from_ent(ent, part_range=range_)


@registry.misc("part_range_match")
def part_range_match(ent: Span) -> PartRange:
    return PartRange.part_range_match(ent)
