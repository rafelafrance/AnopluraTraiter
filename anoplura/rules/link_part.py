from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class LinkPart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    others: ClassVar[list[str]] = [
        "linker",
        "separator",
        "subpart",
        "part_shape",
        "subpart_morphology",
        "seta",
        "seta_count",
        "seta_morphology",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="link_part_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="link_part_patterns",
            compiler=cls.link_part_patterns(),
            overwrite=["seta"],
        )
        add.cleanup_pipe(nlp, name="link_part_cleanup")

    @classmethod
    def link_part_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="link_part",
                on_match="link_part_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "other": {"ENT_TYPE": {"IN": cls.others}},
                },
                patterns=[
                    " part+  other+ ",
                    " other+ part+ ",
                ],
            ),
        ]

    @classmethod
    def link_part_match(cls, ent: Span) -> Never:
        part, which = None, None
        others = []

        for e in ent.ents:
            if e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ in ("subpart", "subpart_morphology", "seta", "seta_count"):
                others.append(e._.trait)

        cls.fill_others(others, part, which)

        raise reject_match.SkipTraitCreation

    @classmethod
    def fill_others(
        cls, others: list[Base], part: str, which: str | list[str] | list[int]
    ) -> None:
        for other in others:
            if not other.part:
                other.part = part
                other.which = which


@registry.misc("link_part_match")
def link_part_match(ent: Span) -> LinkPart:
    return LinkPart.link_part_match(ent)
