from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SpecimenType(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "specimen_type_terms.csv",
    ]
    # ----------------------

    specimen_type: str | None = None
    specimen_sex: str | None = None
    specimen_type_other: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="specimen_type_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="specimen_type_patterns",
            compiler=cls.specimen_type_patterns(),
            overwrite=["sex", "specimen_type"],
        )
        add.cleanup_pipe(nlp, name="specimen_type_cleanup")

    @classmethod
    def specimen_type_patterns(cls):
        return [
            Compiler(
                label="specimen_type",
                on_match="specimen_type_match",
                keep="specimen_type",
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
    def specimen_type_match(cls, ent):
        type_, sex, other = None, None, None
        for sub_ent in ent.ents:
            if sub_ent.label_ == "specimen_type":
                type_ = sub_ent.text.lower()
            elif sub_ent.label_ == "sex":
                sex = sub_ent._.trait.sex
            elif sub_ent.label_ == "other_type":
                other = sub_ent.text.lower()

        return cls.from_ent(
            ent, specimen_type=type_, specimen_sex=sex, specimen_type_other=other
        )


@registry.misc("specimen_type_match")
def specimen_type_match(ent):
    return SpecimenType.specimen_type_match(ent)
