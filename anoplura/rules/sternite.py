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
class Sternite(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    sep: ClassVar[list[str]] = [",", "and"]
    # ----------------------

    part: str = "sternite"
    which: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sternite_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sternite_patterns",
            compiler=cls.sternite_patterns(),
            overwrite=["number", "range"],
        )
        add.cleanup_pipe(nlp, name="sternite_cleanup")

    @classmethod
    def sternite_patterns(cls):
        return [
            Compiler(
                label="sternite",
                on_match="sternite_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    ",": {"LOWER": {"IN": cls.sep}},
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "label": {"ENT_TYPE": "labels"},
                    "sternite": {"ENT_TYPE": "sternites"},
                },
                patterns=[
                    " sternite ",
                    " sternite (* label* 9      )* ",
                    " sternite (* label* 9 ,* 9 )* ",
                    " sternite 9* ",
                    " sternite 9+ ,* 9+ ",
                    " sternite 9+ ,* 9+ ,* 9+ ",
                    " sternite 9-9+ ",
                    " sternite 9-9+ ,* 9+ ",
                ],
            ),
        ]

    @classmethod
    def sternite_match(cls, ent):
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


@registry.misc("sternite_match")
def sternite_match(ent):
    return Sternite.sternite_match(ent)
