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
class Taxon(Base):
    # Class vars ----------
    taxon_csv: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "taxon_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "replace")
    ranks: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "rank")
    groups: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "label")
    # ---------------------

    taxon: str | None = None
    rank: str | None = None

    def __str__(self) -> str:
        val = f"{self._trait}: {self.taxon}"
        if self.rank:
            val += f" {self.rank}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="taxon_terms", path=cls.taxon_csv)
        add.trait_pipe(nlp, name="taxon_patterns", compiler=cls.taxon_patterns())
        add.cleanup_pipe(nlp, name="taxon_cleanup")

    @classmethod
    def taxon_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="taxon",
                on_match="taxon_match",
                decoder={
                    "anoplura": {"ENT_TYPE": "anoplura"},
                },
                patterns=[
                    "anoplura+",
                ],
            ),
        ]

    @classmethod
    def taxon_match(cls, ent: Span) -> "Taxon":
        text = ent.text.lower()
        taxon = cls.replace.get(text, text)
        rank = cls.ranks.get(text, "species")
        return cls.from_ent(ent, taxon=taxon, rank=rank)


@registry.misc("taxon_match")
def taxon_match(ent: Span) -> Taxon:
    return Taxon.taxon_match(ent)
