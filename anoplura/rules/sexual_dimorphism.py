from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SexualDimorphism(Base):
    # Class vars ----------
    sep: ClassVar[list[str]] = [",", "and"]
    # ---------------------

    reference_sex: str | None = None
    parts: list[str] | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="dimorphism_patterns",
            compiler=cls.dimorphism_patterns(),
        )
        add.context_pipe(
            nlp,
            name="sexual_dimorphism_patterns",
            compiler=cls.sexual_dimorphism_patterns(),
            overwrite=["sex", "dimorphism"],
        )
        add.cleanup_pipe(nlp, name="sexual_dimorphism_cleanup")

    @classmethod
    def dimorphism_patterns(cls):
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
    def sexual_dimorphism_patterns(cls):
        return [
            Compiler(
                label="sexual_dimorphism",
                on_match="sexual_dimorphism_match",
                decoder={
                    ",": {"LOWER": {"IN": cls.sep}},
                    "morph": {"ENT_TYPE": "dimorphism"},
                    "part": {"ENT_TYPE": "part"},
                    "sex": {"ENT_TYPE": "sex"},
                },
                patterns=[
                    "       morph+ sex+ ",
                    " part+ morph+ sex+ ",
                    " part+ ,* sex+ ",
                    " part+ ,* part+ ,* sex+ ",
                    " part+ ,* part+ ,* part+ ,* morph* sex+ ",
                ],
            ),
        ]

    @classmethod
    def dimorphism_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def sexual_dimorphism_match(cls, ent):
        sex, morph = None, None
        parts = []
        for sub_ent in ent.ents:
            if sub_ent.label_ == "sex":
                sex = sub_ent._.trait.sex
            elif sub_ent.label_ == "part":
                parts.append(sub_ent._.trait.part)
            elif sub_ent.label_ == "dimorphism":
                morph = sub_ent.text.lower()

        return cls.from_ent(ent, reference_sex=sex, parts=parts, description=morph)


@registry.misc("dimorphism_match")
def dimorphism_match(ent):
    return SexualDimorphism.dimorphism_match(ent)


@registry.misc("sexual_dimorphism_match")
def sexual_dimorphism_match(ent):
    return SexualDimorphism.sexual_dimorphism_match(ent)
