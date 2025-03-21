from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class Sternite(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "part_terms.csv"
    # ----------------------

    sternites: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sternite_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sternite_patterns",
            compiler=cls.sternite_patterns(),
            overwrite=["sternite", "number", "range"],
        )
        add.cleanup_pipe(nlp, name="sternite_cleanup")

    @classmethod
    def sternite_patterns(cls):
        return [
            Compiler(
                label="sternite",
                on_match="sternite_match",
                keep="sternite",
                decoder={
                    "9": {"ENT_TYPE": "number"},
                    "9-9": {"ENT_TYPE": "range"},
                    "sternite": {"ENT_TYPE": "sternite"},
                },
                patterns=[
                    " sternite 9 ",
                    " sternite 9-9+ ",
                ],
            ),
        ]

    @classmethod
    def sternite_match(cls, ent):
        sternites = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                sternites.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                sternites += list(range(low, high + 1))

        return cls.from_ent(ent, sternites=sternites)


@registry.misc("sternite_match")
def sternite_match(ent):
    return Sternite.sternite_match(ent)
