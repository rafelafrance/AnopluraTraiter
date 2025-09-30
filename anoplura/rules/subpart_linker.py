from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SubpartLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    phrase: ClassVar[list[str]] = [
        "count",
        "description",
        "separator",
        "linker",
        "subpart",
        "seta",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="subpart_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ########################################
        add.context_pipe(
            nlp,
            name="subpart_linker_patterns",
            compiler=cls.subpart_linker_patterns(),
        )
        add.cleanup_pipe(nlp, name="subpart_linker_cleanup")

    @classmethod
    def subpart_linker_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart_linker",
                on_match="subpart_linker_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "phrase": {"ENT_TYPE": {"IN": cls.phrase}},
                },
                patterns=[
                    " part+ phrase+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_linker_match(cls, ent: Span) -> Never:
        subparts = [e._.trait for e in ent.ents if e.label_ in ("subpart", "seta")]
        part = next(e._.trait for e in ent.ents if e.label_ in PARTS)

        for subpart in subparts:
            part.link(subpart)

        raise reject_match.SkipTraitCreation


@registry.misc("subpart_linker_match")
def subpart_linker_match(ent: Span) -> SubpartLinker:
    return SubpartLinker.subpart_linker_match(ent)
