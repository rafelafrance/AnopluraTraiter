from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartSample(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "dimension_terms.csv"
    eq: ClassVar[list[str]] = ["=", "⫽"]
    # ---------------------

    sample_size: int | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_sample_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="part_sample_patterns",
            compiler=cls.part_sample_patterns(),
            overwrite=["number"],
        )
        add.cleanup_pipe(nlp, name="part_sample_cleanup")

    @classmethod
    def part_sample_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_sample",
                on_match="part_sample_match",
                decoder={
                    "=": {"LOWER": {"IN": cls.eq}},
                    "label": {"ENT_TYPE": "sample_term"},
                    "99": {"ENT_TYPE": "number"},
                },
                patterns=[
                    " label+ =* 99 ",
                ],
            ),
        ]

    @classmethod
    def part_sample_match(cls, ent: Span) -> "PartSample":
        sample = None

        for e in ent.ents:
            if e.label_ == "number":
                sample = int(e._.trait.number)

        return cls.from_ent(ent, sample_size=sample)


@registry.misc("part_sample_match")
def part_sample_match(ent: Span) -> PartSample:
    return PartSample.part_sample_match(ent)
