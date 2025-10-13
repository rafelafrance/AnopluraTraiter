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
class GroupPrefix(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    # ----------------------

    group: str = ""

    def for_html(self) -> str:
        return f"Group: {self.group}"

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="group_prefix_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="group_prefix_patterns",
            compiler=cls.group_prefix_patterns(),
            overwrite=["group_prefix"],
        )
        add.cleanup_pipe(nlp, name="group_prefix_cleanup")

    @classmethod
    def group_prefix_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="group_prefix",
                on_match="group_prefix_match",
                decoder={
                    "group_prefix": {"ENT_TYPE": "group_prefix"},
                },
                patterns=[
                    " group_prefix+ ",
                ],
            ),
        ]

    @classmethod
    def group_prefix_match(cls, ent: Span) -> "GroupPrefix":
        return cls.from_ent(ent, group=ent.text.lower())


@registry.misc("group_prefix_match")
def group_match(ent: Span) -> GroupPrefix:
    return GroupPrefix.group_prefix_match(ent)
