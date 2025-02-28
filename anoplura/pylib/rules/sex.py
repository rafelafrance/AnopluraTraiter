from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.rules.base import Base


@dataclass(eq=False)
class Sex(Base):
    # Class vars ----------
    sex_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "sex_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(sex_csv, "replace")
    # ---------------------

    sex: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sex_terms", path=cls.sex_csv)
        add.trait_pipe(
            nlp,
            name="sex_patterns",
            compiler=cls.sex_patterns(),
        )
        add.cleanup_pipe(nlp, name="sex_cleanup")

    @classmethod
    def sex_patterns(cls):
        return [
            Compiler(
                label="sex",
                on_match="sex_match",
                keep="sex",
                decoder={
                    "sex": {"ENT_TYPE": "sex_"},
                },
                patterns=[
                    " sex ",
                ],
            ),
        ]

    @classmethod
    def sex_match(cls, ent):
        sex = ent.text.lower()
        sex = cls.replace.get(sex, sex)
        return cls.from_ent(ent, sex=sex)


@registry.misc("sex_match")
def sex_match(ent):
    return Sex.sex_match(ent)
