from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class PlateSeta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "missing_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    # ----------------------

    plates: list[int] | None = None
    plate_position: str | None = None
    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="plate_seta_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="plate_seta_patterns",
            compiler=cls.plate_seta_patterns(),
            overwrite=["plate", "seta", "seta_count"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.cleanup_pipe(nlp, name="plate_seta_cleanup")

    @classmethod
    def plate_seta_patterns(cls):
        return [
            Compiler(
                label="plate_seta",
                on_match="plate_seta_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "count": {"ENT_TYPE": "seta_count"},
                    "filler": {"POS": {"IN": ["ADP", "PRON", "NOUN", "PART"]}},
                    "plate": {"ENT_TYPE": "plate"},
                    "group": {"ENT_TYPE": "group"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "seta"},
                    "missing": {"ENT_TYPE": "missing"},
                },
                patterns=[
                    " plate+ filler*  count+ ",
                    " plate+ filler*  count+ ",
                    " plate+ missing+ chaeta+  ",
                    " (? seta+ )? filler* plate+ group* ",
                ],
            ),
        ]

    @classmethod
    def plate_seta_match(cls, ent):
        plates, pos, seta, low, high, group = None, None, None, None, None, None

        for sub_ent in ent.ents:
            if sub_ent.label_ == "plate":
                plates = sub_ent._.trait.plates
                pos = sub_ent._.trait.plate_position

            elif sub_ent.label_ == "seta_count":
                seta = sub_ent._.trait.seta
                low = sub_ent._.trait.seta_count_low
                high = sub_ent._.trait.seta_count_high
                group = sub_ent._.trait.seta_count_group

            elif sub_ent.label_ == "missing":
                seta = "missing"
                low = 0

            elif sub_ent.label_ == "seta":
                seta = sub_ent._.trait.seta

            elif sub_ent.label_ == "group":
                group = sub_ent.text.lower()

        return cls.from_ent(
            ent,
            plates=plates,
            plate_position=pos,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
        )


@registry.misc("plate_seta_match")
def plate_seta_match(ent):
    return PlateSeta.plate_seta_match(ent)
