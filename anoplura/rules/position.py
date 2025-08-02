from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Position(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    position: str | None = None
    position_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="position_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="position_patterns",
            compiler=cls.position_patterns(),
            overwrite=["position", "group"],
        )
        add.cleanup_pipe(nlp, name="position_cleanup")

    @classmethod
    def position_patterns(cls):
        return [
            Compiler(
                label="position",
                on_match="position_match",
                decoder={
                    "group": {"ENT_TYPE": "group"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " pos+ group* ",
                    " group* pos+ ",
                ],
            ),
        ]

    @classmethod
    def position_match(cls, ent):
        pos = []
        group = None

        for e in ent.ents:
            if e.label_ == "position":
                text = e.text.lower()
                pos.append(cls.replace.get(text, text))
            elif e.label_ == "group":
                group = e._.trait.group

        pos = " ".join(pos)
        return cls.from_ent(ent, position=pos, position_group=group)


@registry.misc("position_match")
def position_match(ent):
    return Position.position_match(ent)
