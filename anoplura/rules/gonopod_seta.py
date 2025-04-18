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
class GonopodSeta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    # ----------------------

    gonopods: list[int] | None = None
    gonopod_position: str | None = None
    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None
    seta_count_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="gonopod_seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="gonopod_seta_patterns",
            compiler=cls.gonopod_seta_patterns(),
            overwrite=["gonopod", "seta", "seta_count"],
        )
        add.cleanup_pipe(nlp, name="gonopod_seta_cleanup")

    @classmethod
    def gonopod_seta_patterns(cls):
        return [
            Compiler(
                label="gonopod_seta",
                on_match="gonopod_seta_match",
                keep="gonopod_seta",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "count": {"ENT_TYPE": "seta_count"},
                    "fill": {"POS": {"IN": ["ADP", "NOUN", "PART", "PRON", "VERB"]}},
                    "gonopod": {"ENT_TYPE": "gonopod"},
                    "group": {"ENT_TYPE": "group"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "seta"},
                    "missing": {"ENT_TYPE": "missing"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " gonopod+ fill*  count+ ",
                    " gonopod+ missing+ chaeta+  ",
                    " (? seta+ )? fill* gonopod+ group* ",
                    " count+ fill* pos* fill* gonopod+ group* pos* ",
                ],
            ),
        ]

    @classmethod
    def gonopod_seta_match(cls, ent):
        gonopods, pos, seta, low, high, group = None, None, None, None, None, None
        seta_pos = None

        for sub_ent in ent.ents:
            if sub_ent.label_ == "gonopod":
                gonopods = sub_ent._.trait.gonopods

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
            gonopods=gonopods,
            gonopod_position=pos,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
            seta_count_position=seta_pos,
        )


@registry.misc("gonopod_seta_match")
def gonopod_seta_match(ent):
    return GonopodSeta.gonopod_seta_match(ent)
