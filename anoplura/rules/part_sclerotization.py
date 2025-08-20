from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules import base
from anoplura.rules.base import Base


@dataclass(eq=False)
class PartSclerotization(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "separator_terms.csv",
    ]
    # ----------------------

    part: str | list[str] = None
    which: str | list[str] | list[int] | None = None
    description: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sclerotized_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="sclerotized_description_patterns",
            compiler=cls.sclerotized_description_patterns(),
            overwrite=["sclerotization"],
        )
        add.context_pipe(
            nlp,
            name="sclerotized_patterns",
            compiler=cls.sclerotized_patterns(),
            overwrite=["sclerotized_description"],
        )
        add.cleanup_pipe(nlp, name="sclerotized_cleanup")

    @classmethod
    def sclerotized_description_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sclerotized_description",
                is_temp=True,
                on_match="sclerotized_description_match",
                decoder={
                    "adv": {"POS": "ADV"},
                    "sclerotized": {"ENT_TYPE": "sclerotization"},
                },
                patterns=[
                    " adv sclerotized ",
                ],
            ),
        ]

    @classmethod
    def sclerotized_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sclerotized",
                on_match="sclerotized_match",
                decoder={
                    ",": {"ENT_TYPE": "separator"},
                    "part": {"ENT_TYPE": "part"},
                    "sclerotized": {"ENT_TYPE": "sclerotized_description"},
                },
                patterns=[
                    "part+                   sclerotized+",
                    "part+ ,* part+          sclerotized+",
                    "part+ ,* part+ ,* part+ sclerotized+",
                ],
            ),
        ]

    @classmethod
    def sclerotized_description_match(cls, ent: Span) -> "PartSclerotization":
        return cls.from_ent(ent)

    @classmethod
    def sclerotized_match(cls, ent: Span) -> "PartSclerotization":
        part = [e for e in ent.ents if e.label_ == "part"]
        descr = next(
            (e.text.lower() for e in ent.ents if e.label_ == "sclerotized_description"),
            None,
        )

        part, which = base.get_all_body_parts(part)

        return cls.from_ent(ent, part=part, which=which, description=descr)


@registry.misc("sclerotized_description_match")
def sclerotized_description_match(ent: Span) -> PartSclerotization:
    return PartSclerotization.sclerotized_description_match(ent)


@registry.misc("sclerotized_match")
def sclerotized_match(ent: Span) -> PartSclerotization:
    return PartSclerotization.sclerotized_match(ent)
