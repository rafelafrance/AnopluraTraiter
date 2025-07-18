from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
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
    # ---------------------

    group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="group_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="group_patterns",
            compiler=cls.group_patterns(),
            overwrite=["group"],
        )
        add.cleanup_pipe(nlp, name="group_cleanup")

    @classmethod
    def group_patterns(cls):
        return [
            Compiler(
                label="group",
                on_match="group_match",
                decoder={
                    "group": {"ENT_TYPE": "group"},
                },
                patterns=[
                    " group+ ",
                ],
            ),
        ]

    @classmethod
    def group_match(cls, ent):
        return cls.from_ent(ent, group=ent.text.lower())


@registry.misc("group_match")
def group_match(ent):
    return Group.group_match(ent)
