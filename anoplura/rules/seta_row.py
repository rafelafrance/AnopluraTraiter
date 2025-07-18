from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaRow(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        # Path(__file__).parent / "terms" / "group_terms.csv",
    ]
    sep: ClassVar[list[str]] = [",", "and"]
    # ----------------------

    rows: list[int] | None = None
    seta: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="row_patterns",
            compiler=cls.row_patterns(),
            overwrite=["number", "range"],
        )
        add.cleanup_pipe(nlp, name="row_cleanup")

    @classmethod
    def row_patterns(cls):
        return [
            Compiler(
                label="row",
                on_match="row_match",
                decoder={
                    ",": {"LOWER": {"IN": cls.sep}},
                    "99": {"ENT_TYPE": "number"},
                    "99-99": {"ENT_TYPE": "range"},
                    "row": {"ENT_TYPE": "row"},
                },
                patterns=[
                    " row+ 99+        ",
                    " row+ 99+ ,* 99+ ",
                    " row+ 99-99+     ",
                ],
            ),
        ]

    @classmethod
    def row_match(cls, ent):
        rows = []

        for e in ent.ents:
            if e.label_ == "number":
                rows.append(int(e._.trait.number))
            elif e.label_ == "range":
                low = int(e._.trait.low)
                high = int(e._.trait.high)
                rows += list(range(low, high + 1))

        rows = sorted(set(rows)) if rows else None

        return cls.from_ent(ent, rows=rows)


@registry.misc("row_match")
def row_match(ent):
    return SetaRow.row_match(ent)
