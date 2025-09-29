from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import ANY_PART, PARTS, Base, link_traits


@dataclass
class PartLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ########################################
        add.context_pipe(
            nlp,
            name="part_linker_patterns",
            compiler=cls.part_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="part_linker_cleanup")

    @classmethod
    def part_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_linker",
                on_match="part_linker_match",
                decoder={
                    "any_part": {"ENT_TYPE": {"IN": ANY_PART}},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "desc": {"ENT_TYPE": "description"},
                    "linker": {"ENT_TYPE": {"IN": ["separator", "linker"]}},
                },
                patterns=[
                    " any_part+ linker* any_part+ ",
                    " any_part+ desc* linker* any_part+ ",
                    " any_part+ desc* linker* any_part+ linker* desc* part+ ",
                ],
            ),
        ]

    @classmethod
    def part_linker_match(cls, ent: Span) -> Never:
        parts = [e._.trait for e in ent.ents if e.label_ in ANY_PART]

        for part1 in parts:
            for part2 in parts:
                link_traits(part1, part2)

        raise reject_match.SkipTraitCreation


@registry.misc("part_linker_match")
def part_linker_match(ent: Span) -> PartLinker:
    return PartLinker.part_linker_match(ent)
