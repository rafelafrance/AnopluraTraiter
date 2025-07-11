from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base, get_body_part


@dataclass(eq=False)
class Position(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="position_patterns",
            compiler=cls.position_patterns(),
            overwrite=["position"],
        )
        add.cleanup_pipe(nlp, name="position_cleanup")

    @classmethod
    def position_patterns(cls):
        return [
            Compiler(
                label="position",
                on_match="position_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "subpart": {"ENT_TYPE": "subpart"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " part+    pos+ ",
                    " pos+     part+ ",
                    " subpart+ pos+ ",
                    " pos+     subpart+ ",
                ],
            ),
        ]

    @classmethod
    def position_match(cls, ent):
        body_part, sub_ent = None, None
        pos = []

        for e in ent.ents:
            if e.label_ in PARTS:
                body_part = get_body_part(e)
            elif e.label_ == "subpart":
                body_part = get_body_part(e)
            elif e.label_ == "position":
                sub_ent = e
                text = e.text.lower()
                text = cls.replace.get(text, text)
                pos.append(text)

        new_ent = cls.from_ent(
            sub_ent,
            position=" ".join(pos),
            body_part=body_part.body_part if body_part else "",
            which=body_part.which if body_part else "",
        )

        return new_ent


@registry.misc("position_match")
def position_match(ent):
    return Position.position_match(ent)
