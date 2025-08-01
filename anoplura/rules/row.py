from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Row(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    # ----------------------

    rows: list[int] | None = None
    position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="row_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="row_patterns",
            compiler=cls.row_patterns(),
            overwrite=["position", "row"],
        )
        add.cleanup_pipe(nlp, name="row_cleanup")

    @classmethod
    def row_patterns(cls):
        return [
            Compiler(
                label="row",
                on_match="row_match",
                decoder={
                    "pos": {"ENT_TYPE": "position"},
                    "row": {"ENT_TYPE": "row"},
                },
                patterns=[
                    " pos+ row+ ",
                ],
            ),
        ]

    @classmethod
    def row_match(cls, ent):
        pos = None

        for e in ent.ents:
            if e.label_ == "position":
                pos = e._.trait.position

        return cls.from_ent(ent, position=pos)


@registry.misc("row_match")
def row_match(ent):
    return Row.row_match(ent)
