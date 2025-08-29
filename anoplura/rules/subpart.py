from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from spacy.tokens import Span
from traiter.pipes import add
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import PARTS, Base


@dataclass(eq=False)
class Subpart(Base):
    # Class vars ----------
    terms: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "group_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "position_terms.csv",
        Path(__file__).parent / "terms" / "size_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(terms, "replace")
    # ----------------------

    subpart: str | None = None
    part: str | list[str] | None = None
    which: str | list[str] | list[int] | None = None
    position: str | None = None
    group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="subpart_terms", path=cls.terms)
        # add.debug_tokens(nlp)  # ################################################
        add.context_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=[
                "part",
                "bug_subpart",
                "position",
                "group",
                # "subpart_suffix",
                "size_term",
            ],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_patterns(cls) -> list[Compiler]:
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                decoder={
                    "group": {"ENT_TYPE": "group"},
                    "part": {"ENT_TYPE": {"IN": PARTS}},
                    "pos": {"ENT_TYPE": {"IN": ["position", "size_term"]}},
                    "subpart": {"ENT_TYPE": "bug_subpart"},
                },
                patterns=[
                    " pos* subpart+ group* ",
                    " pos+ part+ subpart+ group* ",
                    " part+ subpart+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_match(cls, ent: Span) -> "Subpart":
        sub, part, which, group = None, None, None, None
        pos = []

        for e in ent.ents:
            if e.label_ == "bug_subpart":
                text = e.text.lower()
                sub = cls.replace.get(text, text)
            elif e.label_ in PARTS:
                part = e._.trait.part
                which = e._.trait.which
            elif e.label_ in ("position", "size_term"):
                pos.append(e.text.lower())
            elif e.label_ == "group":
                group = e.text.lower()
            # elif e.label_ == "subpart_suffix":
            #     sub = e.text.lower()

        pos = " ".join(pos) if pos else None

        return cls.from_ent(
            ent, subpart=sub, part=part, which=which, position=pos, group=group
        )


@registry.misc("subpart_match")
def subpart_match(ent: Span) -> Subpart:
    return Subpart.subpart_match(ent)
