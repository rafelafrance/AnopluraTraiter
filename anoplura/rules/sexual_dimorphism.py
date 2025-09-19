from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SexualDimorphism(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ---------------------

    reference_sex: str | None = None
    parts: list[str] | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="dimorphism_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="dimorphism_patterns",
            compiler=cls.dimorphism_patterns(),
            overwrite=["shape"],
        )
        add.context_pipe(
            nlp,
            name="sexual_dimorphism_patterns",
            compiler=cls.sexual_dimorphism_patterns(),
            overwrite=["sex", "dimorphism"],
        )
        add.cleanup_pipe(nlp, name="sexual_dimorphism_cleanup")

    @classmethod
    def dimorphism_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="dimorphism",
                is_temp=True,
                on_match="dimorphism_match",
                decoder={
                    "morph": {"POS": {"IN": ["ADJ", "ADV", "ADP", "PART", "PRON"]}},
                },
                patterns=[
                    "morph+",
                ],
            ),
        ]

    @classmethod
    def sexual_dimorphism_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sexual_dimorphism",
                on_match="sexual_dimorphism_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "morph": {"ENT_TYPE": "dimorphism"},
                    "part": {"ENT_TYPE": "part"},
                    "sex": {"ENT_TYPE": "sex"},
                },
                patterns=[
                    "                         morph+ sex+ ",
                    " part+ ,*                morph* sex+ ",
                    " part+ ,* part+ ,*       morph* sex+ ",
                    " part+ ,* part+ ,* part+ morph* sex+ ",
                ],
            ),
        ]

    @classmethod
    def dimorphism_match(cls, ent: Span) -> "SexualDimorphism":
        return cls.from_ent(ent)

    @classmethod
    def sexual_dimorphism_match(cls, ent: Span) -> "SexualDimorphism":
        sex, morph = None, None
        parts = []
        for e in ent.ents:
            if e.label_ == "sex":
                sex = e._.trait.sex
            elif e.label_ == "part":
                parts.append(e._.trait.part)
            elif e.label_ == "dimorphism":
                morph = e.text.lower()

        return cls.from_ent(ent, reference_sex=sex, parts=parts, description=morph)


@registry.misc("dimorphism_match")
def dimorphism_match(ent: Span) -> SexualDimorphism:
    return SexualDimorphism.dimorphism_match(ent)


@registry.misc("sexual_dimorphism_match")
def sexual_dimorphism_match(ent: Span) -> SexualDimorphism:
    return SexualDimorphism.sexual_dimorphism_match(ent)
