import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class Seta(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    parts: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "part")
    # ----------------------

    seta: str | None = None
    seta_part: str | None = None
    part: str = None
    which: str | list[str] | list[int] | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_patterns",
            compiler=cls.seta_patterns(),
            overwrite=["chaeta", "seta_abbrev", "setae"],
        )
        add.cleanup_pipe(nlp, name="seta_cleanup")

    @classmethod
    def seta_patterns(cls):
        return [
            Compiler(
                label="seta",
                on_match="seta_match",
                decoder={
                    "abbrev": {"ENT_TYPE": "seta_abbrev"},
                    "chaeta": {"ENT_TYPE": "chaeta"},
                    "seta": {"ENT_TYPE": "setae"},
                },
                patterns=[
                    "abbrev+",
                    "chaeta+",
                    "seta+",
                ],
            ),
        ]

    @classmethod
    def seta_match(cls, ent):
        text = ent.text.lower()
        seta = cls.replace.get(text, text)
        seta = re.sub(r"seta$", "setae", seta)
        return cls.from_ent(ent, seta=seta, seta_part=cls.parts.get(text))


@registry.misc("seta_match")
def seta_match(ent):
    return Seta.seta_match(ent)
