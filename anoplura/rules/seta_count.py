from dataclasses import dataclass

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaCount(Base):
    seta: str | None = None
    low: int | None = None
    high: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_count_patterns",
            compiler=cls.seta_count_patterns(),
            overwrite=["number", "range", "seta"],
        )

    @classmethod
    def seta_count_patterns(cls):
        return [
            Compiler(
                label="seta_count",
                on_match="seta_count_match",
                keep="seta_count",
                decoder={
                    "cheata": {"ENT_TYPE": "seta"},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                },
                patterns=[
                    "99+ cheata+",
                    "99-99+ cheata+",
                ],
            ),
        ]

    @classmethod
    def seta_count_match(cls, ent):
        low, high, seta = None, None, None
        for e in ent.ents:
            if e.label_ == "seta":
                seta = e._.trait.seta
            elif e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
        return cls.from_ent(ent, seta=seta, low=low, high=high)


@registry.misc("seta_count_match")
def seta_count_match(ent):
    return SetaCount.seta_count_match(ent)
