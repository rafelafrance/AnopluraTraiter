from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class Subpart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    subpart: str | None = None

    def __str__(self) -> str:
        return f"{self._trait}: {self.subpart}"

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="subpart_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ################################################
        add.context_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=[
                "part",
                "bug_subpart",
                "position",
            ],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                decoder={
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "pos": {"ENT_TYPE": "position"},
                    "subpart": {"ENT_TYPE": "bug_subpart"},
                },
                patterns=[
                    " subpart+ ",
                    " part+  subpart+ ",
                    " pos+   subpart+ ",
                    " pos+ part+ subpart+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_match(cls, ent: Span) -> "Subpart":
        sub = []

        for e in ent.ents:
            if e.label_ == "bug_subpart":
                text = e.text.lower()
                sub.append(cls.replace.get(text, text))
            elif e.label_ in PARTS:
                if hasattr(e._.trait, "number"):
                    sub.append(e._.trait.number)
                sub.append(e._.trait.part)
            elif e.label_ in ("position", "shape_term"):
                sub.append(e.text.lower())

        sub = " ".join(sub)

        return cls.from_ent(ent, subpart=sub)


@registry.misc("subpart_match")
def subpart_match(ent: Span) -> Subpart:
    return Subpart.subpart_match(ent)
