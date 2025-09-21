from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Never

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add, reject_match
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


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
                    ",": {"ENT_TYPE": {"IN": ["separator", "linker"]}},
                    "descr": {"ENT_TYPE": "description"},
                    "linker": {"ENT_TYPE": "linker"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "seta": {"ENT_TYPE": "seta"},
                    "subpart": {"ENT_TYPE": "subpart"},
                },
                patterns=[
                    " part+ ,* descr+ ",
                    " seta+ ,* descr+ ",
                    " subpart+ ,* descr+ ",
                    " part+ ,* descr+ ,* descr+ ",
                    " seta+ ,* descr+ ,* descr+ ",
                    " subpart+ ,* descr+ ,* descr+ ",
                    " descr+ part+ ",
                    " descr+ seta+ ",
                    " descr+ subpart+ ",
                    " descr+ part+ descr+ ",
                    " descr+ seta+ descr+ ",
                    " descr+ subpart+ descr+ ",
                ],
            ),
        ]

    @classmethod
    def description_linker_match(cls, span: Span) -> Never:  # noqa: C901
        descr = []
        part, subpart, seta = None, None, None

        for e in span.ents:
            if e.label_ == "description":
                descr.append(e._.trait)
            elif e.label_ in PARTS:
                part = e._.trait
            elif e.label_ == "subpart":
                subpart = e._.trait
            elif e.label_ == "seta":
                seta = e._.trait

        for d in descr:
            if part:
                part.append_link(d)
                d.append_link(part)
            if subpart:
                subpart.append_link(d)
                d.append_link(subpart)
            if seta:
                seta.append_link(d)
                d.append_link(seta)

        for d in descr:
            d.links_completed_for("subpart", "seta", *PARTS)

        raise reject_match.SkipTraitCreation


@registry.misc("description_linker_match")
def description_linker_match(ent: Span) -> DescriptionLinker:
    return DescriptionLinker.description_linker_match(ent)
