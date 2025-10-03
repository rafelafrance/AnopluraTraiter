from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import ANY_PART, Base


@dataclass(eq=False)
class CountLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    descr: ClassVar[list[str]] = [
        "group",
        "morphology",
        "position",
        "relative_position",
        "relative_size",
        "shape",
        "size_description",
    ]
    all_parts: ClassVar[list[str]] = [*ANY_PART, "sex"]
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
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "9": {"ENT_TYPE": "count"},
                    "desc": {"ENT_TYPE": {"IN": cls.descr}},
                    "part": {"ENT_TYPE": {"IN": cls.all_parts}},
                    "sep": {"ENT_TYPE": {"IN": ["separator", "linker"]}},
                },
                patterns=[
                    " (? 9+ )? (? desc* )? part+ ",
                    " (? 9+ part+ )? ",
                    " (? part+ 9+ )? ",
                    " part+ (? 9+ )? ",
                    " part+ (? 9+ )? ",
                    " part+ (? 9+ ,* 9+ )? ",
                ],
            ),
        ]

    @classmethod
    def count_linker_match(cls, span: Span) -> Never:
        counts = [e._.trait for e in span.ents if e.label_ == "count"]
        parent = next(e._.trait for e in span.ents if e.label_ in cls.all_parts)

        for count in counts:
            parent.link(count)

        raise reject_match.SkipTraitCreation


@registry.misc("count_linker_match")
def count_linker_match(ent: Span) -> CountLinker:
    return CountLinker.count_linker_match(ent)
