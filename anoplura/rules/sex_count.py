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
class SexCount(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "group_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    sex: str | None = None
    sex_count: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="sex_count_patterns",
            compiler=cls.sex_count_patterns(),
            overwrite=["number", "sex"],
        )
        add.cleanup_pipe(nlp, name="sex_count_cleanup")

    @classmethod
    def sex_count_patterns(cls):
        return [
            Compiler(
                label="sex_count",
                on_match="sex_count_match",
                decoder={
                    "sex": {"ENT_TYPE": "sex"},
                    "99": {"ENT_TYPE": "number"},
                },
                patterns=[
                    " 99+ sex+ ",
                ],
            ),
        ]

    @classmethod
    def sex_count_match(cls, ent):
        sex, count = None, None

        for e in ent.ents:
            if e.label_ == "sex":
                sex = e._.trait.sex
            elif e.label_ == "number":
                count = int(e._.trait.number)

        return cls.from_ent(ent, sex=sex, sex_count=count)


@registry.misc("sex_count_match")
def sex_count_match(ent):
    return SexCount.sex_count_match(ent)
