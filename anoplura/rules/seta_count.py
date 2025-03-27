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
class SetaCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = [
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_count_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_count_patterns",
            compiler=cls.seta_count_patterns(),
            overwrite=["number", "range", "seta"],
        )
        add.cleanup_pipe(nlp, name="seta_count_cleanup")

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
                    "filler": {"POS": {"IN": ["ADP", "ADJ", "NOUN"]}},
                    "group": {"ENT_TYPE": "group"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " group* 99+    cheata+ group*   ",
                    " group* 99-99+ cheata+ group*   ",
                    " group+        cheata+          ",
                    "               cheata+ group+   ",
                    " missing+      cheata+          ",
                    "               cheata+ missing+ ",
                ],
            ),
        ]

    @classmethod
    def seta_count_match(cls, ent):
        low, high, seta, group = None, None, None, None

        for e in ent.ents:
            if e.label_ == "seta":
                seta = e._.trait.seta
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

        return cls.from_ent(
            ent,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
        )


@registry.misc("seta_count_match")
def seta_count_match(ent):
    return SetaCount.seta_count_match(ent)
