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
class Setae(Base):  # Class vars ----------
    setae_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "setae_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(setae_csv, "replace")
    # ---------------------

    setae: str = None

    def formatted(self) -> dict[str, str]:
        return {"Body Part": self.setae}

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="setae_terms", path=cls.setae_csv)
        add.trait_pipe(nlp, name="setae_patterns", compiler=cls.setae_patterns())
        add.cleanup_pipe(nlp, name="setae_cleanup")

    @classmethod
    def setae_patterns(cls):
        return [
            Compiler(
                label="setae",
                on_match="setae_match",
                keep="setae",
                decoder={
                    "abbrev": {"ENT_TYPE": "seta_abbrev"},
                    "seta": {"ENT_TYPE": "chaeta"},
                    "word": {"ENT_TYPE": "seta_word"},
                },
                patterns=[
                    "abbrev",
                    "word+ seta word*",
                    "word* seta word+",
                ],
            ),
        ]

    @classmethod
    def setae_match(cls, ent):
        text = ent.text.lower()
        setae = cls.replace.get(text, text)
        return cls.from_ent(ent, setae=setae)


@registry.misc("setae_match")
def setae_match(ent):
    return Setae.setae_match(ent)
