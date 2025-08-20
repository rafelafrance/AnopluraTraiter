from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


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
    which: list[int] | None = None
    position: str | None = None

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
        plates = []
        pos = []

        for e in ent.ents:
            if e.label_ in ("number", "roman"):
                plates.append(int(e._.trait.number))

            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
                plates += list(range(low, high + 1))

            elif e.label_ == "position":
                pos.append(e.text.lower())

        plates = sorted(set(plates)) if plates else None
        pos = " ".join(pos) if pos else None

        return cls.from_ent(ent, which=plates, position=pos)


@registry.misc("plate_match")
def plate_match(ent: Span) -> Plate:
    return Plate.plate_match(ent)
