from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaRow(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [Path(__file__).parent / "terms" / "group_terms.csv"]
    sep: ClassVar[list[str]] = [",", "and", "to"]
    # ----------------------

    seta_rows: list[int] | None = None
    seta: str | None = None
    seta_count_low: int | None = None
    seta_count_high: int | None = None
    seta_count_group: str | None = None
    seta_count_position: str | None = None
    seta_count_group_count: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="seta_row_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="seta_row_patterns",
            compiler=cls.seta_row_patterns(),
            overwrite=["number", "range", "seta_count", "row"],
        )
        add.cleanup_pipe(nlp, name="seta_row_cleanup")

    @classmethod
    def seta_row_patterns(cls):
        return [
            Compiler(
                label="seta_row",
                on_match="seta_row_match",
                keep="seta_row",
                decoder={
                    ",": {"LOWER": {"IN": cls.sep}},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "row": {"ENT_TYPE": "row"},
                    "count": {"ENT_TYPE": "seta_count"},
                    "with": {"POS": {"IN": ["ADP"]}},
                },
                patterns=[
                    " row+ 99+        with? count+ ",
                    " row+ 99+ ,* 99+ with? count+ ",
                    " row+ 99-99+     with? count+ ",
                ],
            ),
        ]

    @classmethod
    def seta_row_match(cls, ent):
        low, high, seta, group, g_count, pos = None, None, None, None, None, None
        seta = None
        rows = []

        for e in ent.ents:
            if e.label_ == "seta_count":
                seta = e._.trait.seta
                low = e._.trait.seta_count_low
                high = e._.trait.seta_count_high
                group = e._.trait.seta_count_group
                pos = e._.trait.seta_count_position
                g_count = e._.trait.seta_count_group_count
            elif e.label_ == "number":
                rows.append(int(e._.trait.number))
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
                rows += list(range(low, high + 1))

        rows = sorted(set(rows)) if rows else None

        return cls.from_ent(
            ent,
            seta_rows=rows,
            seta=seta,
            seta_count_low=low,
            seta_count_high=high,
            seta_count_group=group,
            seta_count_position=pos,
            seta_count_group_count=g_count,
        )


@registry.misc("seta_row_match")
def seta_row_match(ent):
    return SetaRow.seta_row_match(ent)
