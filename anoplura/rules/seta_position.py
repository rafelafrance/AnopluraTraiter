from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SetaPosition(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    seta_part: str | None = None
    position: str | None = None
    subpart: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="seta_position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##############################################
        add.trait_pipe(
            nlp,
            name="seta_pos",
            compiler=cls.seta_pos_patterns(),
            overwrite=["position", "group"],
        )
        # add.debug_tokens(nlp)  # ##############################################
        add.context_pipe(
            nlp,
            name="seta_position_patterns",
            compiler=cls.seta_position_patterns(),
            overwrite=["seta_pos"],
        )
        add.cleanup_pipe(nlp, name="seta_position_cleanup")

    @classmethod
    def seta_pos_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="seta_pos",
                is_temp=True,
                on_match="seta_pos_match",
                decoder={
                    "pos": {"ENT_TYPE": {"IN": ["position", "shape_term"]}},
                    "group": {"ENT_TYPE": "group"},
                    "verb": {"POS": "VERB"},
                    "words": {"POS": {"IN": ["ADV", "CCONJ", "ADJ", "PART", "ADP"]}},
                },
                patterns=[
                    "              pos+ words* group* ",
                    " verb+ words* pos+ words* group* ",
                ],
            ),
        ]

    @classmethod
    def seta_position_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="seta_position",
                on_match="seta_position_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "pos": {"ENT_TYPE": "seta_pos"},
                    "seta": {"ENT_TYPE": "seta"},
                    "subpart": {"ENT_TYPE": "subpart"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                },
                patterns=[
                    " (? seta+ )? pos+ subpart+ ",
                    " (? seta+ )? pos+ ",
                    " (? seta* )? pos+ seta+ ",
                ],
            ),
        ]

    @classmethod
    def seta_pos_match(cls, ent: Span) -> "SetaPosition":
        return cls.from_ent(ent)

    @classmethod
    def seta_position_match(cls, ent: Span) -> "SetaPosition":
        seta, seta_part = None, None
        pos, subpart = None, None

        for e in ent.ents:
            if e.label_ == "seta":
                if not seta:
                    seta = e._.trait.seta
                    seta_part = e._.trait.seta_part
                else:
                    subpart = e._.trait.seta
            elif e.label_ == "seta_pos":
                pos = e.text.lower()
            elif e.label_ == "subpart":
                subpart = e._.trait.subpart

        return cls.from_ent(
            ent,
            seta=seta,
            seta_part=seta_part,
            position=pos,
            subpart=subpart,
        )


@registry.misc("seta_pos_match")
def seta_pos_match(ent: Span) -> SetaPosition:
    return SetaPosition.seta_pos_match(ent)


@registry.misc("seta_position_match")
def seta_position_match(ent: Span) -> SetaPosition:
    return SetaPosition.seta_position_match(ent)
