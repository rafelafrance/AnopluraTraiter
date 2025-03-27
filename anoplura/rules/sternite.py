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
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "body_part_terms.csv",
    ]
    # ----------------------

    sternites: list[int] | None = None
    sternite_position: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sternite_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sternite_patterns",
            compiler=cls.sternite_patterns(),
            overwrite=["number", "range"],
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
                    "adj": {"POS": {"IN": ["ADP", "ADJ"]}},
                    "pos": {"ENT_TYPE": "position"},
                    "sternite": {"ENT_TYPE": "sternites"},
                },
                patterns=[
                    " sternite 9+ ",
                    " sternite 9-9+ ",
                    " pos+ sternite 9* ",
                    " pos+ sternite 9-9* ",
                ],
            ),
        ]

    @classmethod
    def sternite_match(cls, ent):
        sternites = []
        pos = []

        for sub_ent in ent.ents:
            if sub_ent.label_ == "number":
                sternites.append(int(sub_ent._.trait.number))

            elif sub_ent.label_ == "position":
                pos.append(sub_ent.text.lower())

            elif sub_ent.label_ == "range":
                low = int(sub_ent._.trait.low)
                high = int(sub_ent._.trait.high)
                sternites += list(range(low, high + 1))

        sternites = sorted(set(sternites)) if sternites else None
        pos = " ".join(pos) if pos else None

        return cls.from_ent(ent, sternites=sternites, sternite_position=pos)


@registry.misc("sternite_match")
def sternite_match(ent):
    return Sternite.sternite_match(ent)
