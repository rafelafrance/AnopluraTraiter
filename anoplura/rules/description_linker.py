from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import ANY_PART, Base, link_traits


@dataclass(eq=False)
class DescriptionLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="description_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="description_linker_patterns",
            compiler=cls.description_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="description_linker_cleanup")

    @classmethod
    def description_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="description_linker",
                on_match="description_linker_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "any_part": {"ENT_TYPE": {"IN": ANY_PART}},
                    "sep": {"ENT_TYPE": "separator"},
                    "descr": {"ENT_TYPE": "description"},
                    "linker": {"ENT_TYPE": "linker"},
                },
                patterns=[
                    " any_part+ sep* (? descr+ )? ",
                    # " any_part+ sep* (? descr+ )? sep* (? descr+ )? ",
                    " (? descr+ )? linker* any_part+ ",
                    " (? descr+ )? any_part+ ",
                    " (? descr+ )? any_part+ (? descr+ )? ",
                ],
            ),
        ]

    @classmethod
    def description_linker_match(cls, span: Span) -> Never:
        descr = [e._.trait for e in span.ents if e.label_ == "description"]
        parts = [e._.trait for e in span.ents if e.label_ in ANY_PART]

        for d in descr:
            for p in parts:
                link_traits(d, p)

        raise reject_match.SkipTraitCreation


@registry.misc("description_linker_match")
def description_linker_match(ent: Span) -> DescriptionLinker:
    return DescriptionLinker.description_linker_match(ent)
