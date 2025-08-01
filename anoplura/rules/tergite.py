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
class Tergite(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    sep: ClassVar[list[str]] = [",", "and"]
    # ----------------------

    part: str = "tergite"
    which: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="tergite_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="tergite_patterns",
            compiler=cls.tergite_patterns(),
            overwrite=["number", "range"],
        )
        add.cleanup_pipe(nlp, name="tergite_cleanup")

    @classmethod
    def tergite_patterns(cls):
        return [
            Compiler(
                label="tergite",
                on_match="tergite_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"LOWER": {"IN": cls.sep}},
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "label": {"ENT_TYPE": "labels"},
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
    def tergite_match(cls, ent):
        which = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                which.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                which += list(range(low, high + 1))

        which = sorted(set(which)) if which else None

        return cls.from_ent(ent, which=which)


@registry.misc("tergite_match")
def tergite_match(ent):
    return Tergite.tergite_match(ent)
