from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class LinkPartToPart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    reference: ClassVar[list[str]] = [
        "segment",
    ]
    linkee: ClassVar[list[str]] = [
        "sternite",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="link_part_to_part_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ########################################
        add.context_pipe(
            nlp,
            name="link_part_to_part_patterns",
            compiler=cls.link_part_to_part_patterns(),
            overwrite=cls.linkee,
        )
        add.cleanup_pipe(nlp, name="link_part_to_part_cleanup")

    @classmethod
    def link_part_to_part_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="link_part_to_part",
                on_match="link_part_to_part_match",
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
    def link_part_to_part_match(cls, ent: Span) -> Never:
        reference_part, reference_which = None, None
        linkee = None

        for e in ent.ents:
            if e.label_ in cls.reference:
                reference_part = e._.trait.part
                reference_which = e._.trait.which
            elif e.label_ in cls.linkee:
                linkee = e._.trait

        linkee.reference_part = reference_part
        linkee.reference_which = reference_which

        raise reject_match.SkipTraitCreation


@registry.misc("link_part_to_part_match")
def link_part_to_part_match(ent: Span) -> LinkPartToPart:
    return LinkPartToPart.link_part_to_part_match(ent)
