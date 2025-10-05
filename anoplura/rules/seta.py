import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Seta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    parts: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "part")
    # ----------------------

    seta: str | None = None
    seta_part: str | None = None

    def __str__(self) -> str:
        val = f"{self._trait}: {self.seta}"
        if self.seta_part:
            val += f" - {self.seta_part}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="seta_terms", path=cls.terms)
        add.trait_pipe(nlp, name="seta_patterns", compiler=cls.seta_patterns())
        add.cleanup_pipe(nlp, name="seta_cleanup")

    @classmethod
    def seta_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="seta",
                on_match="seta_match",
                decoder={
                    "abbrev": {"ENT_TYPE": "seta_abbrev"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "setae"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    "abbrev+",
                    "pos* chaeta+",
                    "pos* seta+",
                ],
            ),
        ]

    @classmethod
    def seta_match(cls, ent: Span) -> "Seta":
        text = ent.text.lower()
        seta = cls.replace.get(text, text)
        seta = re.sub(r"seta$", "setae", seta)
        return cls.from_ent(ent, seta=seta, seta_part=cls.parts.get(text))


@registry.misc("seta_match")
def seta_match(ent: Span) -> Seta:
    return Seta.seta_match(ent)
