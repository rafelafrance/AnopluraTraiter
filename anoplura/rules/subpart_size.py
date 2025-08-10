from dataclasses import dataclass, field

from spacy.language import Language
from spacy.util import registry
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler

from anoplura.pylib.dimension import Dimension
from anoplura.rules.base import Base


@dataclass(eq=False)
class SubpartSize(Base):
    # Class vars ----------
    # ---------------------

    subpart: str | None = None
    part: str | list[str] = None
    which: str | list[str] | list[int] | None = None
    position: str | None = None
    group: str | None = None
    morphology: str | None = None
    dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        # add.debug_tokens(nlp)  # ##########################################
        add.context_pipe(
            nlp,
            name="subpart_size_patterns",
            compiler=cls.subpart_size_patterns(),
            overwrite=["size"],
        )

    @classmethod
    def subpart_size_patterns(cls):
        return [
            Compiler(
                label="subpart_size",
                on_match="subpart_size_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "subpart": {"ENT_TYPE": "subpart"},
                    "size": {"ENT_TYPE": "size"},
                },
                patterns=[
                    " (? subpart+ )? size+ ",
                ],
            ),
        ]

    @classmethod
    def subpart_size_match(cls, ent):
        sub, part, which, group, dims, pos = None, None, None, None, None, None

        for e in ent.ents:
            if e.label_ == "size":
                dims = e._.trait.dims

            elif e.label_ == "subpart":
                sub = e._.trait.subpart
                part = e._.trait.part
                which = e._.trait.which
                pos = e._.trait.position
                group = e._.trait.group

        return cls.from_ent(
            ent,
            subpart=sub,
            part=part,
            which=which,
            position=pos,
            group=group,
            dims=dims,
        )


@registry.misc("subpart_size_match")
def subpart_size_match(ent):
    return SubpartSize.subpart_size_match(ent)
