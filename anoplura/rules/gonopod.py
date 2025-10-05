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
class Gonopod(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    part: str = "gonopod"
    number: list[int] | None = None

    def __str__(self) -> str:
        val = f"{self._trait}: {self.part}"
        if self.number:
            val += f" - {self.number}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="gonopod_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="gonopod_patterns",
            compiler=cls.gonopod_patterns(),
            overwrite=["number", "roman"],
        )
        add.cleanup_pipe(nlp, name="gonopod_cleanup")

    @classmethod
    def gonopod_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="gonopod",
                on_match="gonopod_match",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "iv": {"ENT_TYPE": "roman"},
                    "pod": {"ENT_TYPE": "gonopods"},
                },
                patterns=[
                    " pod 9 ",
                    " pod iv ",
                    " pod 9* ",
                ],
            ),
        ]

    @classmethod
    def gonopod_match(cls, ent: Span) -> "Gonopod":
        number = [
            int(e._.trait.number) for e in ent.ents if e.label_ in ("number", "roman")
        ]
        number = sorted(set(number)) if number else None

        return cls.from_ent(ent, number=number)


@registry.misc("gonopod_match")
def gonopod_match(ent: Span) -> Gonopod:
    return Gonopod.gonopod_match(ent)
