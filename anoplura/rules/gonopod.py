from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Gonopod(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    # ----------------------

    gonopods: list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="gonopod_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="gonopod_patterns",
            compiler=cls.gonopod_patterns(),
            overwrite=["number", "roman"],
        )
        # add.debug_tokens(nlp)  # ##########################################
        add.cleanup_pipe(nlp, name="gonopod_cleanup")

    @classmethod
    def gonopod_patterns(cls):
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
    def gonopod_match(cls, ent):
        gonopods = [
            int(e._.trait.number) for e in ent.ents if e.label_ in ("number", "roman")
        ]
        gonopods = sorted(set(gonopods)) if gonopods else None

        return cls.from_ent(ent, gonopods=gonopods)


@registry.misc("gonopod_match")
def gonopod_match(ent):
    return Gonopod.gonopod_match(ent)
