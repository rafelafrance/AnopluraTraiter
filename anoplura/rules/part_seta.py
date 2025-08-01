from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base, get_body_part


@dataclass(eq=False)
class PartSeta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    # ----------------------

    part: str | None = None
    which: str | list[str] | list[int] | None = None
    seta: str | None = None
    count_low: int | None = None
    count_high: int | None = None
    count_group: str | None = None
    position: str | None = None
    group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="part_seta_patterns",
            compiler=cls.part_seta_patterns(),
            overwrite=["seta", "seta_count"],
        )
        add.cleanup_pipe(nlp, name="part_seta_cleanup")

    @classmethod
    def part_seta_patterns(cls):
        return [
            Compiler(
                label="part_seta",
                on_match="part_seta_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "count": {"ENT_TYPE": "seta_count"},
                    "fill": {"POS": {"IN": ["ADP", "NOUN", "PART", "PRON", "VERB"]}},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "group": {"ENT_TYPE": "group"},
                    "seta": {"ENT_TYPE": "seta"},
                    "missing": {"ENT_TYPE": "missing"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " part+ fill*  count+ ",
                    " (? seta+ )? fill* part+ group* ",
                    " count+ fill* pos* fill* part+ group* pos* ",
                ],
            ),
        ]

    @classmethod
    def part_seta_match(cls, ent):
        part, pos, seta, low, high, c_group = None, None, None, None, None, None
        group = None

        for e in ent.ents:
            if e.label_ in PARTS:
                part = get_body_part(e)

            elif e.label_ == "seta_count":
                seta = e._.trait.seta
                low = e._.trait.count_low
                high = e._.trait.count_high
                c_group = e._.trait.count_group

            elif e.label_ == "missing":
                seta = "missing"
                low = 0

            elif e.label_ == "seta":
                seta = e._.trait.seta

            elif e.label_ == "group":
                group = e.text.lower()

            elif e.label_ == "position":
                pos = e._.trait.position

            elif e.label_ == "group":
                group = e._.trait.group

        return cls.from_ent(
            ent,
            part=part.part,
            which=part.which,
            position=pos,
            seta=seta,
            count_low=low,
            count_high=high,
            count_group=c_group,
            group=group,
        )


@registry.misc("part_seta_match")
def part_seta_match(ent):
    return PartSeta.part_seta_match(ent)
