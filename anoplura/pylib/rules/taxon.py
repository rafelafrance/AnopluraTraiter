from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const, term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.rules.base import Base


@dataclass(eq=False)
class Taxon(Base):
    # Class vars ----------
    taxon_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "taxon_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "replace")
    ranks: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "rank")
    groups: ClassVar[dict[str, str]] = term_util.look_up_table(taxon_csv, "label")
    # ---------------------

    taxon: str = None
    rank: str = None
    group: str = None

    def formatted(self) -> dict[str, str]:
        return {"Taxon": self.taxon, "Rank": self.rank, "Group": self.group}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="taxon_terms", path=cls.taxon_csv)
        add.trait_pipe(nlp, name="taxon_patterns", compiler=cls.taxon_patterns())
        add.cleanup_pipe(nlp, name="taxon_cleanup")

    @classmethod
    def taxon_patterns(cls):
        return [
            Compiler(
                label="color",
                on_match="taxon_match",
                keep="color",
                decoder={
                    "-": {"TEXT": {"IN": const.DASH}},
                    "color": {"ENT_TYPE": "taxon_term"},
                    "taxon_words": {"ENT_TYPE": {"IN": ["taxon_term", "taxon_mod"]}},
                    "missing": {"ENT_TYPE": "taxon_missing"},
                    "to": {"POS": {"IN": ["AUX"]}},
                },
                patterns=[
                    "missing? taxon_words* -* color+ -* taxon_words*",
                    "missing? taxon_words+ to taxon_words+ color+ -* taxon_words*",
                ],
            ),
        ]

    @classmethod
    def taxon_match(cls, ent):
        taxon = ""
        rank = ""
        group = ""
        return super().from_ent(ent, taxon=taxon, rank=rank, group=group)


@registry.misc("taxon_match")
def taxon_match(ent):
    return Taxon.taxon_match(ent)
