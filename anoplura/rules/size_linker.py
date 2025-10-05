from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SizeLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    all_parts: ClassVar[list[str]] = [*PARTS, "seta", "sex", "subpart"]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="size_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="size_linker_patterns",
            compiler=cls.size_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="size_linker_cleanup")

    @classmethod
    def size_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="size_linker",
                on_match="size_linker_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "9": {"ENT_TYPE": "size"},
                    "desc": {"ENT_TYPE": "description"},
                    "part": {"ENT_TYPE": {"IN": cls.all_parts}},
                },
                patterns=[
                    " (? 9+ )? (? desc* )? part+ ",
                    " (? 9+ part+ )? ",
                    " (? part+ 9+ )? ",
                    " (? part+ )? (? 9+ )? ",
                    " (? part+ )? (? 9+ )? ",
                    " (? part+ )? (? 9+ ,* 9+ )? ",
                ],
            ),
        ]

    @classmethod
    def size_linker_match(cls, span: Span) -> Never:
        sizes = [e._.trait for e in span.ents if e.label_ == "size"]
        parent = next(e._.trait for e in span.ents if e.label_ in cls.all_parts)

        for size in sizes:
            parent.link(size)

        raise reject_match.SkipTraitCreation


@registry.misc("size_linker_match")
def size_linker_match(ent: Span) -> SizeLinker:
    return SizeLinker.size_linker_match(ent)
