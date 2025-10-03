from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SexualDimorphismLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sexual_dimorphism_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="sexual_dimorphism_linker_patterns",
            compiler=cls.sexual_dimorphism_part_patterns(),
        )
        add.cleanup_pipe(nlp, name="sexual_dimorphism_linker_cleanup")

    @classmethod
    def sexual_dimorphism_part_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sexual_dimorphism_linker",
                on_match="sexual_dimorphism_linker_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "morph": {"ENT_TYPE": "sexual_dimorphism"},
                    "linker": {"ENT_TYPE": "linker"},
                },
                patterns=[
                    " part+ linker* ,* morph+ ",
                    " part+ linker* ,* morph+ part+ ",
                    " part+ ,* part+ morph+ ",
                    " part+ ,* part+ ,* part+ morph+ ",
                ],
            ),
        ]

    @classmethod
    def sexual_dimorphism_linker_match(cls, span: Span) -> Never:
        morph = next(e._.trait for e in span.ents if e.label_ == "sexual_dimorphism")
        parts = [e._.trait for e in span.ents if e.label_ in PARTS]

        for part in parts:
            part.link(morph)

        raise reject_match.SkipTraitCreation


@registry.misc("sexual_dimorphism_linker_match")
def sexual_dimorphism_linker_match(ent: Span) -> SexualDimorphismLinker:
    return SexualDimorphismLinker.sexual_dimorphism_linker_match(ent)
