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
class Count(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    count_low: int | None = None
    count_high: int | None = None
    count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="count_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="count_patterns",
            compiler=cls.count_patterns(),
            overwrite=["number", "range", "group"],
        )
        add.cleanup_pipe(nlp, name="count_cleanup")

    @classmethod
    def count_patterns(cls):
        return [
            Compiler(
                label="count",
                on_match="count_match",
                decoder={
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "group": {"ENT_TYPE": "group"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " group* 99+ ",
                    " group* 99-99+ ",
                    " missing+ ",
                    " 99+    group* ",
                    " 99-99+ group* ",
                ],
            ),
        ]

    @classmethod
    def count_match(cls, ent):
        low, high, group = None, None, None

        for e in ent.ents:
            if e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
            elif e.label_ == "missing":
                low = 0
            elif e.label_ == "group":
                group = e.text.lower()

        return cls.from_ent(ent, count_low=low, count_high=high, count_group=group)


@registry.misc("count_match")
def count_match(ent):
    return Count.count_match(ent)
