from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, ForOutput


@dataclass(eq=False)
class Plate(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    part: str = "plate"
    number: list[int] | None = None

    def for_output(self) -> ForOutput:
        suffix, number = "", ""
        if self.number:
            number = ", ".join([str(n) for n in self.number])
            suffix = "s" if len(number) > 1 else ""
        return ForOutput(key=self.part.title() + suffix, value=number)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="plate_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="plate_patterns",
            compiler=cls.plate_patterns(),
            overwrite=["number", "range", "roman"],
        )
        add.cleanup_pipe(nlp, name="plate_cleanup")

    @classmethod
    def plate_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="plate",
                on_match="plate_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "iv": {"ENT_TYPE": "roman"},
                    "plate": {"ENT_TYPE": "plates"},
                    "pos": {"ENT_TYPE": {"IN": ["position"]}},
                },
                patterns=[
                    " pos* plate 9* ",
                    " pos* plate 9+ ,* 9+ ",
                    " pos* plate 9+ ,* 9+ ,* 9+ ",
                    " pos* plate 9-9+ ",
                    " pos* plate 9-9+ ,* 9+ ",
                    " pos* plate iv ",
                    " pos* plate iv , iv ",
                ],
            ),
        ]

    @classmethod
    def plate_match(cls, ent: Span) -> "Plate":
        number = []
        part = []

        for e in ent.ents:
            if e.label_ in ("number", "roman"):
                number.append(int(e._.trait.number))

            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
                number += list(range(low, high + 1))

            elif e.label_ == "position":
                part.append(e.text.lower())

        number = sorted(set(number)) if number else None

        part.append("plate")
        part = " ".join(part)

        return cls.from_ent(ent, part=part, number=number)


@registry.misc("plate_match")
def plate_match(ent: Span) -> Plate:
    return Plate.plate_match(ent)
