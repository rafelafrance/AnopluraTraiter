from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PartLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    reference: ClassVar[list[str]] = [
        "segment",
    ]
    linkee: ClassVar[list[str]] = [
        "sternite",
        "tergite",
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
            overwrite=cls.linkee,
        )
        add.cleanup_pipe(nlp, name="part_linker_cleanup")

    @classmethod
    def part_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part_linker",
                on_match="part_linker_match",
                decoder={
                    "reference": {"ENT_TYPE": {"IN": cls.reference}},
                    "linkee": {"ENT_TYPE": {"IN": cls.linkee}},
                    "with": {"ENT_TYPE": "linker"},
                },
                patterns=[
                    " reference+ with+ linkee+ ",
                    " linkee+ with+ reference+ ",
                ],
            ),
        ]

    @classmethod
    def part_linker_match(cls, ent: Span) -> Never:
        linkees = [e._.trait for e in ent.ents if e.label_ in cls.linkee]
        reference = next(e._.trait for e in ent.ents if e.label_ in cls.reference)

        for linkee in linkees:
            reference.append_link(linkee)
            linkee.append_link(reference)

        raise reject_match.SkipTraitCreation


@registry.misc("part_linker_match")
def part_linker_match(ent: Span) -> PartLinker:
    return PartLinker.part_linker_match(ent)
