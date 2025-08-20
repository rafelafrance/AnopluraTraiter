from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Part(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    part: str = None
    which: str | list[str] | list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="part_terms", path=cls.terms)
        add.trait_pipe(nlp, name="part_patterns", compiler=cls.part_patterns())
        add.cleanup_pipe(nlp, name="part_cleanup")

    @classmethod
    def part_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="part",
                on_match="part_match",
                decoder={
                    "part": {"ENT_TYPE": "bug_part"},
                },
                patterns=[
                    " part+ ",
                ],
            ),
        ]

    @classmethod
    def part_match(cls, ent: Span) -> "Part":
        text = ent.text.lower()
        part = cls.replace.get(text, text)
        return cls.from_ent(ent, part=part)


@registry.misc("part_match")
def part_match(ent: Span) -> Part:
    return Part.part_match(ent)
