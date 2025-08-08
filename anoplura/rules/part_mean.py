from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartMean(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ---------------------

    mean: float | None = None
    units: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
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
    def part_mean_patterns(cls):
        return [
            Compiler(
                label="part_mean",
                on_match="part_mean_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "label": {"ENT_TYPE": "mean_term"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " label+ ,* size+ ",
                ],
            ),
        ]

    @classmethod
    def part_mean_match(cls, ent):
        size = next(e for e in ent.ents if e.label_ == "size")
        dim = size._.trait.dims[0]
        return cls.from_ent(ent, mean=dim.low, units=dim.units)


@registry.misc("part_mean_match")
def part_mean_match(ent):
    return PartMean.part_mean_match(ent)
