from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Shape(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    # ----------------------

    shape: str | None = None

    def format(self) -> str:
        return f"{self._trait}: {self.shape}"

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="shape_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="shape_patterns",
            compiler=cls.shape_patterns(),
        )
        add.cleanup_pipe(nlp, name="shape_cleanup")

    @classmethod
    def shape_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="shape",
                on_match="shape_match",
                decoder={
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "linker": {"ENT_TYPE": "linker"},
                    "rel": {"ENT_TYPE": {"IN": ["shape_term", "rel_pos", "rel_size"]}},
                    "sep": {"ENT_TYPE": "separator"},
                    "shape": {"ENT_TYPE": "shape_term"},
                },
                patterns=[
                    " adv* shape+ ",
                    " adv* rel+ sep* shape+ ",
                    " adv* rel+ linker* shape+ ",
                    " adv* rel+ sep* rel+ sep* shape+ ",
                ],
            ),
        ]

    @classmethod
    def shape_match(cls, ent: Span) -> "Shape":
        return cls.from_ent(ent, shape=ent.text.lower())


@registry.misc("shape_match")
def shape_match(ent: Span) -> Shape:
    return Shape.shape_match(ent)
