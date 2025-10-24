from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, HtmlFormat


@dataclass(eq=False)
class SexualDimorphism(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ---------------------

    reference_sex: str | None = None
    description: str | None = None

    def for_html(self) -> HtmlFormat:
        value = f"{self.description} {self.reference_sex}"
        return HtmlFormat(key="Sexual Dimorphism", value=value)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="dimorphism_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="sexual_dimorphism_patterns",
            compiler=cls.sexual_dimorphism_patterns(),
            overwrite=["sex"],
        )
        add.cleanup_pipe(nlp, name="sexual_dimorphism_cleanup")

    @classmethod
    def sexual_dimorphism_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sexual_dimorphism",
                on_match="sexual_dimorphism_match",
                decoder={
                    "morph": {"POS": {"IN": ["ADJ", "ADV", "ADP", "PRON"]}},
                    "sex": {"ENT_TYPE": "sex"},
                },
                patterns=[
                    " morph+ sex+ ",
                ],
            ),
        ]

    @classmethod
    def sexual_dimorphism_match(cls, ent: Span) -> "SexualDimorphism":
        sex = None
        morph = []
        for t in ent:
            if t.ent_type_ == "sex":
                sex = t.lower_
            else:
                morph.append(t.lower_)

        morph = " ".join(morph)
        return cls.from_ent(ent, reference_sex=sex, description=morph)


@registry.misc("sexual_dimorphism_match")
def sexual_dimorphism_match(ent: Span) -> SexualDimorphism:
    return SexualDimorphism.sexual_dimorphism_match(ent)
