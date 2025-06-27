from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Position(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    # ----------------------

    position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="position_patterns",
            compiler=cls.position_patterns(),
            overwrite=["seta"],
        )
        add.cleanup_pipe(nlp, name="position_cleanup")

    @classmethod
    def position_patterns(cls):
        return [
            Compiler(
                label="position",
                on_match="position_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " (? seta+ )? pos+ group* ",
                    " (? seta+ )? pos* group+ ",
                ],
            ),
        ]

    @classmethod
    def position_match(cls, ent):
        pos = None

        for e in ent.ents:
            if e.label_ == "position":
                pos = e.text.lower()

        return cls.from_ent(ent, position=pos)


@registry.misc("position_match")
def position_match(ent):
    return Position.position_match(ent)
