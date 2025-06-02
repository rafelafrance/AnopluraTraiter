from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Range(Base):
    # Class vars ----------
    dash: ClassVar[list[str]] = ["-", "–", "—", ",", "or", "to"]
    numbers: ClassVar[list[str]] = ["number", "roman"]
    # ---------------------

    low: float | None = None
    high: float | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.trait_pipe(
            nlp,
            name="range_patterns",
            overwrite=["number", "roman"],
            compiler=cls.range_patterns(),
        )

    @classmethod
    def range_patterns(cls):
        return [
            Compiler(
                label="range",
                on_match="range_match",
                decoder={
                    "[+]": {"TEXT": {"IN": t_const.PLUS}},
                    "-": {"TEXT": {"IN": cls.dash}},
                    "99": {"ENT_TYPE": "number"},
                    "iv": {"ENT_TYPE": "roman"},
                },
                patterns=[
                    " 99 -+ 99 [+]? ",
                    " iv -+ iv ",
                ],
            ),
        ]

    @classmethod
    def range_match(cls, ent):
        nums = sorted([e._.trait.number for e in ent.ents if e.label_ in cls.numbers])
        return cls.from_ent(ent, low=nums[0], high=nums[-1])


@registry.misc("range_match")
def range_match(ent):
    return Range.range_match(ent)
