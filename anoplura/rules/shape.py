from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Shape(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "shape_terms.csv"
    # ---------------------

    shape: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="shape_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="shape_patterns",
            compiler=cls.shape_patterns(),
        )
        add.cleanup_pipe(nlp, name="shape_cleanup")

    @classmethod
    def shape_patterns(cls):
        return [
            Compiler(
                label="shape",
                on_match="shape_match",
                decoder={
                    "shape": {"ENT_TYPE": "shape_term"},
                },
                patterns=[
                    " shape+ ",
                ],
            ),
        ]

    @classmethod
    def shape_match(cls, ent):
        shape = ent.text.lower()
        return cls.from_ent(ent, shape=shape)


@registry.misc("shape_match")
def shape_match(ent):
    return Shape.shape_match(ent)
