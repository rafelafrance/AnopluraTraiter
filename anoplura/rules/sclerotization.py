from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, HtmlFormat


@dataclass(eq=False)
class Sclerotization(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    dash: ClassVar[list[str]] = ["-", "–", "—"]
    # ----------------------

    sclerotization: str = ""

    def for_html(self) -> HtmlFormat:
        return HtmlFormat(key="Sclerotization", value=self.sclerotization)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sclerotization_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ################################################
        add.trait_pipe(
            nlp,
            name="sclerotization_patterns",
            compiler=cls.sclerotization_patterns(),
        )
        add.cleanup_pipe(nlp, name="sclerotization_cleanup")

    @classmethod
    def sclerotization_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sclerotization",
                on_match="sclerotization_match",
                decoder={
                    "-": {"TEXT": {"IN": cls.dash}},
                    "adv": {"POS": "ADV"},
                    "sclerotized": {"ENT_TYPE": "sclerotized"},
                },
                patterns=[
                    " adv* -* sclerotized+ ",
                ],
            ),
        ]

    @classmethod
    def sclerotization_match(cls, ent: Span) -> "Sclerotization":
        sclerotization = ent.text.lower()
        return cls.from_ent(ent, sclerotization=sclerotization)


@registry.misc("sclerotization_match")
def sclerotization_match(ent: Span) -> Sclerotization:
    return Sclerotization.sclerotization_match(ent)
