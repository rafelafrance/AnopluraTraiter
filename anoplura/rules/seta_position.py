from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaPosition(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    seta_position: str | None = None
    seta_position_group: str | None = None
    seta_position_group_count: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_position_patterns",
            compiler=cls.seta_position_patterns(),
            overwrite=["seta"],
        )
        add.cleanup_pipe(nlp, name="seta_position_cleanup")

    @classmethod
    def seta_position_patterns(cls):
        return [
            Compiler(
                label="seta_position",
                on_match="seta_position_match",
                decoder={
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "seta": {"ENT_TYPE": "seta"},
                    "filler": {"POS": {"IN": ["ADP", "ADJ", "ADV", "PRON"]}},
                    "group": {"ENT_TYPE": "group"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " (? seta+ )? pos+ group* ",
                    " (? seta+ )? pos* group+ ",
                ],
            ),
        ]

    @classmethod
    def seta_position_match(cls, ent):
        seta, group, g_count, pos = None, None, None, None

        for e in ent.ents:
            if e.label_ == "seta":
                seta = e._.trait.seta
            elif e.label_ == "position":
                pos = e.text.lower()
            elif e.label_ == "group":
                group = e.text.lower()
                g_count = cls.replace.get(group)
                g_count = int(g_count) if g_count else None

        return cls.from_ent(
            ent,
            seta=seta,
            seta_position=pos,
            seta_position_group=group,
            seta_position_group_count=g_count,
        )


@registry.misc("seta_position_match")
def seta_position_match(ent):
    return SetaPosition.seta_position_match(ent)
