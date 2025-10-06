from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Tergite(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "label_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    part: str = "tergite"
    number: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="tergite_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="tergite_patterns",
            compiler=cls.tergite_patterns(),
            overwrite=["number", "range"],
        )
        add.cleanup_pipe(nlp, name="tergite_cleanup")

    @classmethod
    def tergite_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="tergite",
                on_match="tergite_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"ENT_TYPE": "separator"},
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "label": {"ENT_TYPE": "no_labels"},
                    "tergite": {"ENT_TYPE": "tergites"},
                },
                patterns=[
                    " tergite ",
                    " tergite (* label* 9      )* ",
                    " tergite (* label* 9 ,* 9 )* ",
                    " tergite 9* ",
                    " tergite 9+ ,* 9+ ",
                    " tergite 9+ ,* 9+ ,* 9+ ",
                    " tergite 9-9+ ",
                    " tergite 9-9+ ,* 9+ ",
                ],
            ),
        ]

    @classmethod
    def tergite_match(cls, ent: Span) -> "Tergite":
        number = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                number.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                number += list(range(low, high + 1))

        number = sorted(set(number)) if number else None

        return cls.from_ent(ent, number=number)


@registry.misc("tergite_match")
def tergite_match(ent: Span) -> Tergite:
    return Tergite.tergite_match(ent)
