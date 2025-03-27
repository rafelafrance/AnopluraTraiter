from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.rules.base import Base


@dataclass(eq=False)
class BodyPart(Base):
    # Class vars ----------
    terms: ClassVar[Path] = Path(__file__).parent / "terms" / "body_part_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    body_part: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="body_part_terms", path=cls.terms)
        add.trait_pipe(
            nlp, name="body_part_patterns", compiler=cls.body_part_patterns()
        )
        add.cleanup_pipe(nlp, name="body_part_cleanup")

    @classmethod
    def body_part_patterns(cls):
        return [
            Compiler(
                label="body_part",
                on_match="body_part_match",
                keep="body_part",
                decoder={
                    "body_part": {"ENT_TYPE": "bug_part"},
                },
                patterns=[
                    " body_part ",
                ],
            ),
        ]

    @classmethod
    def body_part_match(cls, ent):
        text = ent.text.lower()
        body_part = cls.replace.get(text, text)
        return cls.from_ent(ent, body_part=body_part)


@registry.misc("body_part_match")
def body_part_match(ent):
    return BodyPart.body_part_match(ent)
