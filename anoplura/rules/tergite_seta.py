from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class TergiteSeta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    # ----------------------

    tergites: list[int] | None = None
    tergite_position: str | None = None
    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None
    seta_count_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="tergite_seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="tergite_seta_patterns",
            compiler=cls.tergite_seta_patterns(),
            overwrite=["tergite", "seta", "seta_count"],
        )
        add.cleanup_pipe(nlp, name="tergite_seta_cleanup")

    @classmethod
    def tergite_seta_patterns(cls):
        return [
            Compiler(
                label="tergite_seta",
                on_match="tergite_seta_match",
                keep="tergite_seta",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "count": {"ENT_TYPE": "seta_count"},
                    "filler": {"POS": {"IN": ["ADP", "PRON", "NOUN", "PART"]}},
                    "tergite": {"ENT_TYPE": "tergite"},
                    "group": {"ENT_TYPE": "group"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "seta"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " tergite+ filler*  count+ ",
                    " tergite+ missing+ chaeta+  ",
                    " (? seta+ )? filler* tergite+ group* ",
                ],
            ),
        ]

    @classmethod
    def tergite_seta_match(cls, ent):
        tergites, pos, seta, low, high, group = None, None, None, None, None, None
        seta_pos = None

        for sub_ent in ent.ents:
            if sub_ent.label_ == "tergite":
                tergites = sub_ent._.trait.tergites
                pos = sub_ent._.trait.tergite_position

            elif sub_ent.label_ == "seta_count":
                seta = sub_ent._.trait.seta
                low = sub_ent._.trait.seta_count_low
                high = sub_ent._.trait.seta_count_high
                group = sub_ent._.trait.seta_count_group
                seta_pos = sub_ent._.trait.seta_count_position

            elif sub_ent.label_ == "missing":
                seta = "missing"
                low = 0

            elif sub_ent.label_ == "seta":
                seta = sub_ent._.trait.seta

            elif sub_ent.label_ == "group":
                group = sub_ent.text.lower()

        return cls.from_ent(
            ent,
            tergites=tergites,
            tergite_position=pos,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
            seta_count_position=seta_pos,
        )


@registry.misc("tergite_seta_match")
def tergite_seta_match(ent):
    return TergiteSeta.tergite_seta_match(ent)
