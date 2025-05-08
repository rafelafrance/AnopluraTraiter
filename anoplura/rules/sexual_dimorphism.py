from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SexualDimorphism(Base):
    # Class vars ----------
    sep: ClassVar[list[str]] = [",", "and"]
    # ---------------------

    reference_sex: str | None = None
    body_parts: list[str] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sexual_dimorphism_patterns",
            compiler=cls.sexual_dimorphism_patterns(),
            overwrite=["sex", "body_part"],
        )
        add.cleanup_pipe(nlp, name="sexual_dimorphism_cleanup")

    @classmethod
    def sexual_dimorphism_patterns(cls):
        return [
            Compiler(
                label="sexual_dimorphism",
                on_match="sexual_dimorphism_match",
                keep="sexual_dimorphism",
                decoder={
                    ",": {"LOWER": {"IN": cls.sep}},
                    "fill": {"POS": {"IN": ["ADP", "PART", "PRON"]}},
                    "part": {"ENT_TYPE": "body_part"},
                    "sex": {"ENT_TYPE": "sex"},
                },
                patterns=[
                    " part+ ,* sex+ ",
                    " part+ ,* part+ ,* sex+ ",
                    " part+ ,* part+ ,* part+ ,* fill* sex+ ",
                ],
            ),
        ]

    @classmethod
    def sexual_dimorphism_match(cls, ent):
        sex = None
        parts = []
        for sub_ent in ent.ents:
            if sub_ent.label_ == "sex":
                sex = sub_ent._.trait.sex
            elif sub_ent.label_ == "body_part":
                parts.append(sub_ent._.trait.body_part)

        return cls.from_ent(ent, reference_sex=sex, body_parts=parts)


@registry.misc("sexual_dimorphism_match")
def sexual_dimorphism_match(ent):
    return SexualDimorphism.sexual_dimorphism_match(ent)
