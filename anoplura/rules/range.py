from dataclasses import dataclass
from typing import ClassVar

from spacy import registry
from spacy.language import Language
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class Range(Base):
    # Class vars ----------
    dash: ClassVar[list[str]] = " - , or to ".split()
    # ---------------------

    low: float = None
    high: float = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.term_pipe(nlp, name="range_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="range_patterns",
            overwrite=["number"],
            compiler=cls.range_patterns(),
        )

    @classmethod
    def range_patterns(cls):
        return [
            Compiler(
                label="range",
                keep="range",
                on_match="range_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}, "OP": "+"},
                    "99": {"ENT_TYPE": "number"},
                },
                patterns=[
                    " 99 - 99 ",
                ],
            ),
        ]

    @classmethod
    def range_match(cls, ent):
        numbers = [t._.trait.number for t in ent if t.ent_type_ == "number"]
        return cls.from_ent(ent, low=numbers[0], high=numbers[-1])


@registry.misc("range_match")
def range_match(ent):
    return Range.range_match(ent)
