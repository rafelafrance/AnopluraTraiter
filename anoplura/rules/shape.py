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
    def named_pipe(cls, nlp: Language, suffix: str):
        add.term_pipe(nlp, name=f"shape_terms_{suffix}", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name=f"shape_patterns_{suffix}",
            compiler=cls.shape_patterns(),
        )
        add.cleanup_pipe(nlp, name=f"shape_cleanup_{suffix}")

    @classmethod
    def shape_patterns(cls):
        return [
            Compiler(
                label="shape",
                on_match="shape_match",
                decoder={
                    "shape": {"ENT_TYPE": {"IN": ["shape_term", "relative_term"]}},
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
