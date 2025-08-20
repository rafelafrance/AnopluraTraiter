from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SexCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    sex: str | None = None
    count_low: int | None = None
    count_high: int | None = None
    count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.trait_pipe(
            nlp,
            name="sex_count_patterns",
            compiler=cls.sex_count_patterns(),
            overwrite=["count", "sex"],
        )
        add.cleanup_pipe(nlp, name="sex_count_cleanup")

    @classmethod
    def sex_count_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sex_count",
                on_match="sex_count_match",
                decoder={
                    "sex": {"ENT_TYPE": "sex"},
                    "99": {"ENT_TYPE": "count"},
                },
                patterns=[
                    " 99+ sex+ ",
                ],
            ),
        ]

    @classmethod
    def sex_count_match(cls, ent: Span) -> "SexCount":
        sex, low, high, group = None, None, None, None

        for e in ent.ents:
            if e.label_ == "sex":
                sex = e._.trait.sex
            elif e.label_ == "count":
                low = e._.trait.count_low
                high = e._.trait.count_high
                group = e._.trait.count_group

        return cls.from_ent(
            ent, sex=sex, count_low=low, count_high=high, count_group=group
        )


@registry.misc("sex_count_match")
def sex_count_match(ent: Span) -> SexCount:
    return SexCount.sex_count_match(ent)
