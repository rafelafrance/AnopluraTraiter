from dataclasses import dataclass

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SterniteCount(Base):
    # Class vars ----------
    # ----------------------

    low: int | None = None
    high: int | None = None
    number: list[int] | None = None
    segment: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sternite_count_patterns",
            compiler=cls.sternite_count_patterns(),
            overwrite=["number", "range", "sternite"],
        )
        add.cleanup_pipe(nlp, name="sternite_count_cleanup")

    @classmethod
    def sternite_count_patterns(cls):
        return [
            Compiler(
                label="sternite_count",
                on_match="sternite_count_match",
                keep="sternite_count",
                decoder={
                    "sternite": {"ENT_TYPE": "sternite"},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "adj": {"POS": {"IN": ["ADP", "ADJ"]}},
                },
                patterns=[
                    " 99+ adj* sternite ",
                ],
            ),
        ]

    @classmethod
    def sternite_count_match(cls, ent):
        low, high, sternite, group = None, None, None, None

        for e in ent.ents:
            if e.label_ == "sternite":
                sternite = e._.trait.sternite
            elif e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
            elif e.label_ == "missing":
                low = 0
            elif e.label_ == "group":
                group = e.text.lower()
                low = int(cls.replace.get(group, group)) if low is None else low

        return cls.from_ent(ent, sternite=sternite, low=low, high=high, group=group)


@registry.misc("sternite_count_match")
def sternite_count_match(ent):
    return SterniteCount.sternite_count_match(ent)
