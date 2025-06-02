from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class TergiteCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    tergites: list[int] | None = None
    tergite_count_low: int | None = None
    tergite_count_high: int | None = None
    tergite_position: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="tergite_count_patterns",
            compiler=cls.tergite_count_patterns(),
            overwrite=["number", "range", "tergite"],
        )
        add.cleanup_pipe(nlp, name="tergite_count_cleanup")

    @classmethod
    def tergite_count_patterns(cls):
        return [
            Compiler(
                label="tergite_count",
                on_match="tergite_count_match",
                decoder={
                    "tergite": {"ENT_TYPE": "tergite"},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "filler": {"POS": {"IN": ["ADP", "ADJ", "ADV", "PUNCT"]}},
                },
                patterns=[
                    " 99+    filler* tergite+ ",
                    " 99-99+ filler* tergite+ ",
                ],
            ),
        ]

    @classmethod
    def tergite_count_match(cls, ent):
        low, high, tergites, position = None, None, None, None

        for e in ent.ents:
            if e.label_ == "tergite":
                tergites = e._.trait.tergites
                position = e._.trait.tergite_position
            elif e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)

        return cls.from_ent(
            ent,
            tergites=tergites,
            tergite_count_low=low,
            tergite_count_high=high,
            tergite_position=position,
        )


@registry.misc("tergite_count_match")
def tergite_count_match(ent):
    return TergiteCount.tergite_count_match(ent)
