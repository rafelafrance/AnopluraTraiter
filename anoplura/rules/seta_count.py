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
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None
    seta_count_position: str | None = None
    seta_count_group_count: int | None = None

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
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "seta"},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "filler": {"POS": {"IN": ["ADP", "ADJ", "ADV", "PRON"]}},
                    "group": {"ENT_TYPE": "group"},
                    "missing": {"ENT_TYPE": "missing"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " group* 99+    filler* seta+ group* pos* ",
                    " group* 99-99+ filler* seta+ group* pos* ",
                    " group+        filler* seta+ ",
                    "                       seta+ group+ pos* ",
                    " missing+      filler* seta+ ",
                    "                       seta+ missing+ ",
                    " 99+ group* seta+ ",
                    " 99+ group* chaeta+ ",
                ],
            ),
        ]

    @classmethod
    def seta_count_match(cls, ent):
        low, high, seta, group, g_count, pos = None, None, None, None, None, None

        for e in ent.ents:
            if e.label_ == "seta":
                seta = e._.trait.seta
            elif e.label_ == "chaeta":
                seta = e.text.lower()
            elif e.label_ == "number":
                low = int(e._.trait.number)
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
            elif e.label_ == "missing":
                low = 0
            elif e.label_ == "position":
                pos = e.text.lower()
            elif e.label_ == "group":
                group = e.text.lower()
                g_count = cls.replace.get(group)
                g_count = int(g_count) if g_count else None

        return cls.from_ent(
            ent,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
            seta_count_position=pos,
            seta_count_group_count=g_count,
        )


@registry.misc("seta_count_match")
def seta_count_match(ent):
    return SetaCount.seta_count_match(ent)
