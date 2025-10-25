from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, ForOutput


@dataclass(eq=False)
class SpecimenType(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "specimen_type_terms.csv",
    ]
    # ----------------------

    specimen_type: str = ""
    specimen_type_other: str | None = None

    def for_output(self) -> ForOutput:
        text = (
            f"{self.specimen_type_other.title()} " if self.specimen_type_other else ""
        )
        text += f"{self.specimen_type.title()} {self.sex}"
        return ForOutput(key="Specimen Type", value=text)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="specimen_type_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="specimen_type_patterns",
            compiler=cls.specimen_type_patterns(),
            overwrite=["sex", "specimen_type"],
        )
        add.cleanup_pipe(nlp, name="specimen_type_cleanup")

    @classmethod
    def specimen_type_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="specimen_type",
                on_match="specimen_type_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "sex": {"ENT_TYPE": "sex"},
                    "type": {"ENT_TYPE": "specimen_type"},
                    "other": {"ENT_TYPE": "other_type"},
                },
                patterns=[
                    " type+ ",
                    " type+ (? sex+ )? ",
                    " other type+ ",
                ],
            ),
        ]

    @classmethod
    def specimen_type_match(cls, ent: Span) -> "SpecimenType":
        type_, sex, other = None, None, None
        for sub_ent in ent.ents:
            if sub_ent.label_ == "specimen_type":
                type_ = sub_ent.text.lower()
            elif sub_ent.label_ == "sex":
                sex = sub_ent._.trait.sex
            elif sub_ent.label_ == "other_type":
                other = sub_ent.text.lower()

        sex = sex if sex else ""

        return cls.from_ent(
            ent, specimen_type=type_, sex=sex, specimen_type_other=other
        )


@registry.misc("specimen_type_match")
def specimen_type_match(ent: Span) -> SpecimenType:
    return SpecimenType.specimen_type_match(ent)
