from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import ANY_PART, Base, ForOutput


@dataclass(eq=False)
class SizeDescription(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "separator_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    # ----------------------

    size_description: str = ""

    def for_output(self) -> ForOutput:
        return ForOutput(key="Size", value=self.size_description)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="size_description_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # #########################################
        add.trait_pipe(
            nlp,
            name="size_description_patterns",
            compiler=cls.size_description_patterns(),
            overwrite=["count", "number_suffix", "subpart", "seta", *ANY_PART],
        )
        add.cleanup_pipe(nlp, name="size_description_cleanup")

    @classmethod
    def size_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="size_description",
                on_match="size_description_match",
                decoder={
                    "adv": {"POS": {"IN": ["ADV"]}},
                    "rel": {"ENT_TYPE": {"IN": ["size_term", "rel_pos", "rel_size"]}},
                    "sep": {"ENT_TYPE": "separator"},
                    "size": {"ENT_TYPE": "size_term"},
                },
                patterns=[
                    " adv* size+ ",
                    " adv* rel+ sep* adv* size+ ",
                    " adv* rel+ sep* adv* rel+ sep* size+ ",
                ],
            ),
        ]

    @classmethod
    def size_description_match(cls, ent: Span) -> "SizeDescription":
        return cls.from_ent(ent, size_description=ent.text.lower())


@registry.misc("size_description_match")
def size_description_match(ent: Span) -> SizeDescription:
    return SizeDescription.size_description_match(ent)
