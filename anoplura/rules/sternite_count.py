from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SterniteCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    sternites: list[int] | None = None
    sternite_count_low: int | None = None
    sternite_count_high: int | None = None
    sternite_position: int | None = None

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
                    "adj": {"POS": {"IN": ["ADP", "ADJ", "PUNCT", "NOUN"]}},
                },
                patterns=[
                    " 99+ adj* sternite+ ",
                ],
            ),
        ]

    @classmethod
    def sternite_count_match(cls, ent):
        low, high, sternites, position = None, None, None, None

        for e in ent.ents:
            if e.label_ == "sternite":
                sternites = e._.trait.sternites
                position = e._.trait.sternite_position
            elif e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)

        return cls.from_ent(
            ent,
            sternites=sternites,
            sternite_count_low=low,
            sternite_count_high=high,
            sternite_position=position,
        )


@registry.misc("sternite_count_match")
def sternite_count_match(ent):
    return SterniteCount.sternite_count_match(ent)
