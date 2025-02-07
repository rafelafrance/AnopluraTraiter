# import re
#
# import spacy
# from traiter.const import COMMA
# from traiter.patterns.matcher_patterns import MatcherPatterns
#
# from anoplura.pylib.const import COMMON_PATTERNS, CONJ, MISSING, REPLACE
#
# JOINER = CONJ + COMMA
# JOINER_RE = "|".join([*JOINER, r"\s"])
# JOINER_RE = re.compile(rf"\b({JOINER_RE})\b", flags=re.IGNORECASE)
#
# MISSING_RE = "|".join([rf"\b{m}\b" for m in MISSING])
# MISSING_RE = re.compile(MISSING_RE, flags=re.IGNORECASE)
#
# BODY_PART = MatcherPatterns(
#     "body_part",
#     on_match="anoplura.body_part.v1",
#     decoder=COMMON_PATTERNS
#     | {
#         "seg": {"ENT_TYPE": "segmented"},
#         "ord": {"ENT_TYPE": {"IN": ["ordinal", "number_word"]}},
#     },
#     patterns=[
#         "missing part+",
#         "missing? any_part* part",
#         "part+ &/,/or* part* &/,/or* part+",
#         "part+ ord -? ord",
#         "part+ 99? -? 99",
#         "part+ ord?",
#         "part+ 99?",
#         "part+ ord -? seg",
#         "part+ 99 -? seg",
#         "ord? -? seg? part+",
#         "99 - seg part+",
#     ],
# )
#
#
# @spacy.registry.misc(BODY_PART.on_match)
# def body_part(ent):
#     data = {}
#
#     parts = JOINER_RE.split(ent.text.lower())
#     parts = [REPLACE.get(p, p) for p in parts]
#     text = " ".join(parts)
#     text = re.sub(r"\s*-\s*", "-", text)
#     text = REPLACE.get(text, text)
#
#     if MISSING_RE.search(ent.text.lower()) is not None:
#         data["missing"] = True
#
#     data["body_part"] = text
#
#     ent._.data = data
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from anoplura.pylib.rules.base import Base


@dataclass(eq=False)
class BodyPart(Base):
    # Class vars ----------
    body_part_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "body_part_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(
        body_part_csv, "replace"
    )
    # ---------------------

    body_part: str = None

    def formatted(self) -> dict[str, str]:
        return {"Body Part": self.body_part}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="body_part_terms", path=cls.body_part_csv)
        # add.debug_tokens(nlp)
        add.trait_pipe(
            nlp, name="body_part_patterns", compiler=cls.body_part_patterns()
        )
        add.cleanup_pipe(nlp, name="body_part_cleanup")

    @classmethod
    def body_part_patterns(cls):
        return [
            Compiler(
                label="color",
                on_match="body_part_match",
                keep="color",
                decoder={
                    "anoplura": {"ENT_TYPE": "anoplura"},
                },
                patterns=[
                    "anoplura+",
                ],
            ),
        ]

    @classmethod
    def body_part_match(cls, ent):
        text = ent.text.lower()
        body_part = cls.replace.get(text, text)
        rank = cls.ranks.get(text, "species")
        group = cls.groups.get(text, "mammal")
        return super().from_ent(ent, body_part=body_part, rank=rank, group=group)


@registry.misc("body_part_match")
def body_part_match(ent):
    return BodyPart.body_part_match(ent)
