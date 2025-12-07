import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base_rule import BaseRule, ForOutput


@dataclass(eq=False)
class Seta(BaseRule):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    parts: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "part")
    # ----------------------

    seta: str = ""
    seta_part: str | None = None

    def for_output(self) -> ForOutput:
        sex = f"{self.sex.title()} " if self.sex else ""
        value = self.seta.title()
        return ForOutput(key=value, value=f"{sex}{value}")

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
                    "(": {"LOWER": {"IN": t_const.OPEN}},
                    ")": {"LOWER": {"IN": t_const.CLOSE}},
                    "abbrev": {"ENT_TYPE": "seta_abbrev"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "setae"},
                    "pos": {"ENT_TYPE": "position"},
                },
                patterns=[
                    "abbrev+",
                    "pos* chaeta+",
                    "pos* seta+",
                    "pos* chaeta+ (? abbrev+ )?",
                    "pos* seta+   (? abbrev+ )? ",
                ],
            ),
        ]

    @classmethod
    def seta_match(cls, ent: Span) -> "Seta":
        abbrev = ""
        seta = []
        for e in ent.ents:
            lower = e.text.lower()
            if e.label_ == "seta_abbrev":
                abbrev = lower
            else:
                seta.append(lower)

        text = " ".join(seta) if seta else cls.replace.get(abbrev, abbrev)
        text = re.sub(r"seta$", "setae", text)

        return cls.from_ent(ent, seta=text, seta_part=cls.parts.get(text))


@registry.misc("seta_match")
def seta_match(ent: Span) -> Seta:
    return Seta.seta_match(ent)
