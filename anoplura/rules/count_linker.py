from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class CountLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="count_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="count_linker_patterns",
            compiler=cls.count_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="count_linker_cleanup")

    @classmethod
    def count_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="count_linker",
                on_match="count_linker_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "sclerotized": {"ENT_TYPE": "sclerotization"},
                },
                patterns=[
                    " part+ sclerotized+ ",
                    " part+ ,* part+ sclerotized+ ",
                    " part+ ,* part+ ,* part+ sclerotized+ ",
                ],
            ),
        ]

    @classmethod
    def count_linker_match(cls, span: Span) -> Never:
        sclerotized = next(e._.trait for e in span.ents if e.label_ == "sclerotization")
        parts = [e._.trait for e in span.ents if e.label_ in PARTS]

        for part in parts:
            part.append_link(sclerotized)
            sclerotized.append_link(part)

        raise reject_match.SkipTraitCreation


@registry.misc("count_linker_match")
def count_linker_match(ent: Span) -> CountLinker:
    return CountLinker.count_linker_match(ent)
