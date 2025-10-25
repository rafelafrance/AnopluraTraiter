from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base, ForOutput


@dataclass(eq=False)
class Sex(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [Path(__file__).parent / "terms" / "sex_terms.csv"]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ---------------------

    def for_output(self) -> ForOutput:
        return ForOutput(key="Sex", value=self.sex)

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="sex_terms", path=cls.terms)
        add.trait_pipe(
            nlp,
            name="sex_patterns",
            compiler=cls.sex_patterns(),
        )
        add.cleanup_pipe(nlp, name="sex_cleanup")

    @classmethod
    def sex_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="sex",
                on_match="sex_match",
                decoder={
                    "sex": {"ENT_TYPE": "sexes"},
                },
                patterns=[
                    " sex ",
                ],
            ),
        ]

    @classmethod
    def sex_match(cls, ent: Span) -> "Sex":
        sex = ent.text.lower()
        sex = cls.replace.get(sex, sex)
        return cls.from_ent(ent, sex=sex)


@registry.misc("sex_match")
def sex_match(ent: Span) -> Sex:
    return Sex.sex_match(ent)
