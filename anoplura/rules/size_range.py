from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dim import Dim
from anoplura.rules.base_rule import BaseRule


@dataclass(eq=False)
class SizeRange(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "dimension_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ---------------------

    dims: list[Dim] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="size_range_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="size_range_patterns",
            compiler=cls.part_sample_patterns(),
            overwrite=["size"],
        )
        add.cleanup_pipe(nlp, name="size_range_cleanup")

    @classmethod
    def part_sample_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="size_range",
                on_match="size_range_match",
                decoder={
                    "9": {"ENT_TYPE": "size"},
                    "=": {"ENT_TYPE": "separator"},
                    "label": {"ENT_TYPE": "range_term"},
                },
                patterns=[
                    " label+ =* 9+ ",
                ],
            ),
        ]

    @classmethod
    def size_range_match(cls, ent: Span) -> "SizeRange":
        dims = None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims

        return cls.from_ent(ent, dims=dims)


@registry.misc("size_range_match")
def size_range_match(ent: Span) -> SizeRange:
    return SizeRange.size_range_match(ent)
