from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Group(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    # ----------------------

    group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="group_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="group_patterns",
            compiler=cls.group_patterns(),
            overwrite=["group", "count"],
        )
        add.cleanup_pipe(nlp, name="group_cleanup")

    @classmethod
    def group_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="group",
                on_match="group_match",
                decoder={
                    "group": {"ENT_TYPE": "group"},
                    "on": {"LOWER": "on"},
                    "1": {"TEXT": "1"},
                    "side": {"LOWER": "side"},
                },
                patterns=[
                    " group+ ",
                    " on 1 side ",
                ],
            ),
        ]

    @classmethod
    def group_match(cls, ent: Span) -> "Group":
        return cls.from_ent(ent, group=ent.text.lower())


@registry.misc("group_match")
def group_match(ent: Span) -> Group:
    return Group.group_match(ent)
