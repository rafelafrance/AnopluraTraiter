from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.rule import ForOutput, Rule


@dataclass(eq=False)
class Morphology(Rule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "morphology_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    dash: ClassVar[list[str]] = ["-", "–", "—"]
    # ----------------------

    morphology: str = ""

    def for_output(self) -> ForOutput:
        return ForOutput(key="Morphology", value=f"Morphology: {self.morphology}")

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="morphology_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="morphology_patterns",
            compiler=cls.morphology_patterns(),
            overwrite=["morphology", "count"],
        )
        add.cleanup_pipe(nlp, name="morphology_cleanup")

    @classmethod
    def morphology_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="morphology",
                on_match="morphology_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "9": {"ENT_TYPE": "count"},
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "morph": {"ENT_TYPE": "morphology"},
                    "linker": {"ENT_TYPE": "linker"},
                    "sep": {"ENT_TYPE": "separator"},
                    "suffix": {"ENT_TYPE": "number_suffix"},
                },
                patterns=[
                    " 9+ -* suffix+ ",
                    # -----------------
                    " adv* morph+ ",
                    " adv* morph+ sep+ morph+ ",
                    " adv* morph+ sep+ morph+ sep+ morph+ ",
                    # -----------------
                    " morph+ linker+ morph+ ",
                    " morph+ linker+ morph+ linker+ morph+ ",
                    " morph+ sep+    morph+ linker+ morph+ ",
                ],
            ),
        ]

    @classmethod
    def morphology_match(cls, ent: Span) -> "Morphology":
        return cls.from_ent(ent, morphology=ent.text.lower())


@registry.misc("morphology_match")
def morphology_match(ent: Span) -> Morphology:
    return Morphology.morphology_match(ent)
