from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SclerotizationLinker(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sclerotization_linker_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.context_pipe(
            nlp,
            name="sclerotization_linker_patterns",
            compiler=cls.sclerotization_part_patterns(),
        )
        add.cleanup_pipe(nlp, name="sclerotization_linker_cleanup")

    @classmethod
    def sclerotization_part_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sclerotization_linker",
                on_match="sclerotization_linker_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "sclerotized": {"ENT_TYPE": "sclerotization"},
                    "with": {"ENT_TYPE": "linker"},
                },
                patterns=[
                    " part+ with* ,* sclerotized+ ",
                    " part+ with* ,* sclerotized+ part+ ",
                    " part+ ,* part+ sclerotized+ ",
                    " part+ ,* part+ ,* part+ sclerotized+ ",
                ],
            ),
        ]

    @classmethod
    def sclerotization_linker_match(cls, span: Span) -> Never:
        sclerotized = next(e._.trait for e in span.ents if e.label_ == "sclerotization")
        parts = [e._.trait for e in span.ents if e.label_ in PARTS]

        for part in parts:
            part.append_link(sclerotized)
            sclerotized.append_link(part)

        sclerotized.links_completed_for("part")

        raise reject_match.SkipTraitCreation


@registry.misc("sclerotization_linker_match")
def sclerotization_linker_match(ent: Span) -> SclerotizationLinker:
    return SclerotizationLinker.sclerotization_linker_match(ent)
