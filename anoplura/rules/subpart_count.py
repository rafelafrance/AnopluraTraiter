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
class SubpartCount(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "part_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    dash: ClassVar[list[str]] = ["-", "–"]
    # ----------------------

    body_part: str | None = None
    subpart: str | None = None
    subpart_count: int | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="subpart_count_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="subpart_count_patterns",
            compiler=cls.subpart_count_patterns(),
            overwrite=["body_part", "number"],
        )
        add.cleanup_pipe(nlp, name="subpart_count_cleanup")

    @classmethod
    def subpart_count_patterns(cls):
        return [
            Compiler(
                label="subpart_count",
                on_match="subpart_count_match",
                keep="subpart_count",
                decoder={
                    "part": {"ENT_TYPE": "body_part"},
                    "number": {"ENT_TYPE": "number"},
                    "-": {"TEXT": {"IN": cls.dash}, "OP": "+"},
                    "subpart": {"ENT_TYPE": "subpart_suffix"},
                },
                patterns=[
                    "part+ number+ - subpart+",
                ],
            ),
        ]

    @classmethod
    def subpart_count_match(cls, ent):
        part, subpart, count = "", "", 0
        for sub_ent in ent.ents:
            if sub_ent.label_ == "body_part":
                part = sub_ent._.trait.body_part
            elif sub_ent.label_ == "subpart_suffix":
                text = sub_ent.text.lower()
                subpart = cls.replace.get(text, text)
            elif sub_ent.label_ == "number":
                count = int(sub_ent._.trait.number)

        return cls.from_ent(ent, body_part=part, subpart=subpart, subpart_count=count)


@registry.misc("subpart_count_match")
def subpart_count_match(ent):
    return SubpartCount.subpart_count_match(ent)
