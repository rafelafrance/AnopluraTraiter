from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import BaseRule, ForOutput


@dataclass(eq=False)
class Position(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    position: str = ""

    def for_output(self) -> ForOutput:
        return ForOutput(key="Position", value=f"Position: {self.position}")

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="position_patterns",
            compiler=cls.position_patterns(),
            overwrite=["position"],
        )
        add.cleanup_pipe(nlp, name="position_cleanup")

    @classmethod
    def position_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="position",
                on_match="position_match",
                decoder={
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "conj": {"POS": {"IN": ["CCONJ"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "linker": {"ENT_TYPE": "linker"},
                    "sep": {"ENT_TYPE": "separator"},
                    "verb": {"POS": {"IN": ["VERB"]}},
                },
                patterns=[
                    " adv* pos+ ",
                    " adv* pos+ sep+ pos+ ",
                    " adv* pos+ sep+ pos+ sep+ pos+ ",
                    # -----------------
                    " pos+ linker+ pos+ ",
                    " pos+ linker+ pos+ linker+ pos+ ",
                    " pos+ sep+    pos+ linker+ pos+ ",
                    # -----------------
                    " verb* adv* conj* adv* pos+ ",
                ],
            ),
        ]

    @classmethod
    def position_match(cls, ent: Span) -> "Position":
        return cls.from_ent(ent, position=ent.text.lower())


@registry.misc("position_match")
def position_match(ent: Span) -> Position:
    return Position.position_match(ent)
