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
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "seta_terms.csv",
    ]
    words: ClassVar[list[str]] = ["seta_word", "position", "bug_part", "shape"]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    seta: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp, name="seta_patterns", compiler=cls.seta_patterns(), overwrite=["shape"]
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
                    "setae": {"ENT_TYPE": "chaeta"},
                    "filler": {"POS": {"IN": ["ADP", "ADJ", "ADV", "PRON", "NOUN"]}},
                    "word": {"ENT_TYPE": {"IN": cls.words}},
                },
                patterns=[
                    "abbrev",
                    "setae",
                    "word+ filler* setae+ word*",
                ],
            ),
        ]

    @classmethod
    def seta_match(cls, ent):
        text = ent.text.lower()
        seta = cls.replace.get(text, text)
        return cls.from_ent(ent, seta=seta)


@registry.misc("seta_match")
def seta_match(ent):
    return Seta.seta_match(ent)
