from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.rule import Rule


@dataclass(eq=False)
class SampleSize(Rule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ---------------------

    sample_size: int | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sample_size_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sample_size_patterns",
            compiler=cls.part_sample_patterns(),
            overwrite=["count"],
        )
        add.cleanup_pipe(nlp, name="sample_size_cleanup")

    @classmethod
    def part_sample_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sample_size",
                on_match="sample_size_match",
                decoder={
                    "9": {"ENT_TYPE": "count"},
                    "=": {"ENT_TYPE": "separator"},
                    "label": {"ENT_TYPE": "sample_term"},
                },
                patterns=[
                    " label+ =* 9 ",
                ],
            ),
        ]

    @classmethod
    def sample_size_match(cls, ent: Span) -> "SampleSize":
        sample = None

        for e in ent.ents:
            if e.label_ == "count":
                sample = int(e._.trait.count_low)

        return cls.from_ent(ent, sample_size=sample)


@registry.misc("sample_size_match")
def sample_size_match(ent: Span) -> SampleSize:
    return SampleSize.sample_size_match(ent)
