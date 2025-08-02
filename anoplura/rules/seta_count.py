from dataclasses import dataclass

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib.pattern_compiler import Compiler

from anoplura.rules.base import Base


@dataclass(eq=False)
class SetaCount(Base):
    # Class vars ----------
    # ----------------------

    seta: str | None = None
    part: str | None = None
    count_low: int | None = None
    count_high: int | None = None
    count_group: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="seta_count_patterns",
            compiler=cls.seta_count_patterns(),
            overwrite=["count", "group"],
        )
        add.cleanup_pipe(nlp, name="seta_count_cleanup")

    @classmethod
    def seta_count_patterns(cls):
        return [
            Compiler(
                label="seta_count",
                on_match="seta_count_match",
                decoder={
                    "99": {"ENT_TYPE": "count"},
                    "group": {"ENT_TYPE": "group"},
                    "seta": {"ENT_TYPE": "seta"},
                },
                patterns=[
                    " 99+   group* seta+ ",
                    " seta+ 99+    group* ",
                ],
            ),
        ]

    @classmethod
    def seta_count_match(cls, ent):
        seta, low, high, group, part = None, None, None, None, None

        for e in ent.ents:
            if e.label_ == "count":
                low = e._.trait.count_low
                high = e._.trait.count_high
                group = e._.trait.count_group
            elif e.label_ == "seta":
                seta = e._.trait.seta
                part = e._.trait.part
            elif e.label_ == "group":
                group = e._.trait.group

        return cls.from_ent(
            ent, count_low=low, count_high=high, count_group=group, seta=seta, part=part
        )


@registry.misc("seta_count_match")
def seta_count_match(ent):
    return SetaCount.seta_count_match(ent)
