from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class SetaPosition(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None
    part: str | None = None
    position: str | None = None
    other: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_pos_description",
            compiler=cls.seta_pos_description_patterns(),
            overwrite=["position"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="seta_position_patterns",
            compiler=cls.seta_position_patterns(),
            overwrite=["seta_pos_description"],
        )
        add.cleanup_pipe(nlp, name="seta_position_cleanup")

    @classmethod
    def seta_pos_description_patterns(cls):
        return [
            Compiler(
                label="seta_pos_description",
                is_temp=True,
                on_match="seta_pos_description_match",
                decoder={
                    "verb": {"POS": "VERB"},
                    "words": {"POS": {"IN": ["ADV", "CCONJ", "ADJ", "PART", "ADP"]}},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " verb* words* pos+ words* ",
                ],
            ),
        ]

    @classmethod
    def seta_position_patterns(cls):
        return [
            Compiler(
                label="seta_position",
                on_match="seta_position_match",
                decoder={
                    "descr": {"ENT_TYPE": "seta_pos_description"},
                    "seta": {"ENT_TYPE": "seta"},
                    "subpart": {"ENT_TYPE": "subpart"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                },
                patterns=[
                    " seta+ descr+ subpart+ ",
                    " seta+ descr+ seta+ ",
                ],
            ),
        ]

    @classmethod
    def seta_pos_description_match(cls, ent):
        return cls.from_ent(ent)

    @classmethod
    def seta_position_match(cls, ent):
        seta, part = None, None
        pos, other = None, None

        for e in ent.ents:
            if e.label_ == "seta":
                if not seta:
                    seta = e._.trait.seta
                    part = e._.trait.part
                else:
                    other = e._.trait.seta
            elif e.label_ == "seta_pos_description":
                pos = e.text.lower()
            elif e.label_ == "subpart":
                other = e._.trait.subpart

        return cls.from_ent(
            ent,
            seta=seta,
            part=part,
            position=pos,
            other=other,
        )


@registry.misc("seta_pos_description_match")
def seta_pos_description_match(ent):
    return SetaPosition.seta_pos_description_match(ent)


@registry.misc("seta_position_match")
def seta_position_match(ent):
    return SetaPosition.seta_position_match(ent)
