from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Plate(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    sep: ClassVar[list[str]] = [",", "and"]
    # ----------------------

    part: str = "plate"
    which: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="plate_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="plate_patterns",
            compiler=cls.plate_patterns(),
            overwrite=["number", "range", "roman"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.cleanup_pipe(nlp, name="plate_cleanup")

    @classmethod
    def plate_patterns(cls):
        return [
            Compiler(
                label="plate",
                on_match="plate_match",
                decoder={
                    ",": {"LOWER": {"IN": cls.sep}},
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "iv": {"ENT_TYPE": "roman"},
                    "plate": {"ENT_TYPE": "plates"},
                },
                patterns=[
                    " plate 9* ",
                    " plate 9+ ,* 9+ ",
                    " plate 9+ ,* 9+ ,* 9+ ",
                    " plate 9-9+ ",
                    " plate 9-9+ ,* 9+ ",
                    " plate iv ",
                    " plate iv , iv ",
                ],
            ),
        ]

    @classmethod
    def plate_match(cls, ent):
        plates = []

        for sub_ent in ent.ents:
            if sub_ent.label_ in ("number", "roman"):
                plates.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                plates += list(range(low, high + 1))

        plates = sorted(set(plates)) if plates else None

        return cls.from_ent(ent, which=plates)


@registry.misc("plate_match")
def plate_match(ent):
    return Plate.plate_match(ent)
