from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.rules.base import Base


@dataclass(eq=False)
class Seta(Base):
    # Class vars ----------
    seta_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "seta_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(seta_csv, "replace")
    # --e-------------------

    seta: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_terms", path=cls.seta_csv)
        add.trait_pipe(nlp, name="seta_patterns", compiler=cls.seta_patterns())
        add.cleanup_pipe(nlp, name="seta_cleanup")

    @classmethod
    def seta_patterns(cls):
        return [
            Compiler(
                label="seta",
                on_match="seta_match",
                keep="seta",
                decoder={
                    "abbrev": {"ENT_TYPE": "seta_abbrev"},
                    "setae": {"ENT_TYPE": "chaeta"},
                    "word": {"ENT_TYPE": "seta_word"},
                },
                patterns=[
                    "abbrev",
                    "word+ setae word*",
                    "word* setae word+",
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
