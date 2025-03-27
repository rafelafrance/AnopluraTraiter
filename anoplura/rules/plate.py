from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class Plate(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    plates: list[int] | None = None
    plate_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="plate_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="plate_patterns",
            compiler=cls.plate_patterns(),
            overwrite=["number", "range", "roman"],
        )
        add.cleanup_pipe(nlp, name="plate_cleanup")

    @classmethod
    def plate_patterns(cls):
        return [
            Compiler(
                label="plate",
                on_match="plate_match",
                keep="plate",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "iv": {"ENT_TYPE": "roman"},
                    "plate": {"ENT_TYPE": "plates"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    " plate 9 ",
                    " plate iv ",
                    " plate 9-9+ ",
                    " pos+ plate 9* ",
                    " pos+ plate 9-9* ",
                ],
            ),
        ]

    @classmethod
    def plate_match(cls, ent):
        plates = []
        pos = []

        for sub_ent in ent.ents:
            if sub_ent.label_ in ("number", "roman"):
                plates.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "position":
                pos.append(sub_ent.text.lower())

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                plates += list(range(low, high + 1))

        plates = sorted(set(plates)) if plates else None
        pos = " ".join(pos) if pos else None

        return cls.from_ent(ent, plates=plates, plate_position=pos)


@registry.misc("plate_match")
def plate_match(ent):
    return Plate.plate_match(ent)
