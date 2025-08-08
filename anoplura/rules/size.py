from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy import registry
from spacy.language import Language
from traiter.pipes import add
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.rules import terms as t_terms
from traiter.rules.base import Base

from anoplura.pylib.dimension import Dimension

ALL_CSVS = [
    Path(__file__).parent / "terms" / "dimension_terms.csv",
    Path(__file__).parent / "terms" / "separator_terms.csv",
    Path(t_terms.__file__).parent / "unit_length_terms.csv",
]


@dataclass(eq=False)
class Size(Base):
    # Class vars ----------
    cross: ClassVar[list[str]] = t_const.CROSS + t_const.COMMA
    factors_cm: ClassVar[dict[str, float]] = term_util.look_up_table(
        ALL_CSVS, "factor_cm", float
    )
    factors_cm["in"] = 2.54
    units: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(ALL_CSVS, "replace")
    # ---------------------

    dims: list[Dimension] = field(default_factory=list)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="size_terms", path=ALL_CSVS)
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name="size_patterns",
            compiler=cls.size_patterns(),
            overwrite=["range", "number", "dim", "metric_length", "imperial_length"],
        )

        add.cleanup_pipe(nlp, name="size_cleanup")

    @property
    def dimensions(self):
        return tuple(d.dim for d in self.dims)

    @classmethod
    def size_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "99": {"ENT_TYPE": "number"},
            "99-99": {"ENT_TYPE": "range"},
            "cm": {"ENT_TYPE": {"IN": cls.units}},
            "dim": {"ENT_TYPE": "dimension"},
            "sep": {"ENT_TYPE": "separator"},
            "x": {"ENT_TYPE": "cross"},
        }
        return [
            Compiler(
                label="size",
                on_match="size_match",
                decoder=decoder,
                patterns=[
                    "99+    cm+ dim*",
                    "99-99+ cm+ dim*",
                    "99-99+ cm* dim* x 99-99+ cm+ dim*",
                    " dim+ sep* 99+    cm+ ",
                    " dim+ sep* 99-99+ cm+ ",
                ],
            ),
        ]

    @classmethod
    def update_indices(cls, sub_ent, dims):
        if dims[-1].start is None:
            dims[-1].start = sub_ent[0].idx

        last = sub_ent[-1]
        dims[-1].end = last.idx + len(last)

    @classmethod
    def scan_parts(cls, ent):
        dims = [Dimension()]

        for sub_ent in ent.ents:
            if sub_ent.label_ == "range":
                dims[-1].low = sub_ent._.trait.low
                dims[-1].high = sub_ent._.trait.high
                cls.update_indices(sub_ent, dims)

            elif sub_ent.label_ == "number":
                dims[-1].low = sub_ent._.trait.number
                cls.update_indices(sub_ent, dims)

            elif sub_ent.label_ == "dimension":
                text = sub_ent.text.lower()
                dims[-1].dim = cls.replace.get(text, text)
                cls.update_indices(sub_ent, dims)

            elif sub_ent.label_ in cls.units:
                text = sub_ent.text.lower()
                dims[-1].units = cls.replace.get(text, text)
                cls.update_indices(sub_ent, dims)

            elif sub_ent.label_ == "cross":
                dims.append(Dimension())

        return dims

    @staticmethod
    def fill_units(dims):
        default_units = next((d.units for d in dims if d.units), "cm")

        for dim in dims:
            dim.units = dim.units if dim.units else default_units

    @staticmethod
    def fill_dimensions(dims):
        used = [d.dim for d in dims if d.dim]

        defaults = ["length", "width", "thickness"]
        defaults = [d for d in defaults if d not in used]

        for dim in dims:
            dim.dim = dim.dim if dim.dim else defaults.pop(0)

    @classmethod
    def fill_trait_data(cls, dims, ent):
        # Build the key and value for the range's: low, high
        for dim in dims:
            for key in ("low", "high"):
                value = getattr(dim, key)
                if value is None:
                    continue

                setattr(dim, key, float(value))

        trait = cls.from_ent(ent, dims=dims)
        return trait

    @classmethod
    def size_match(cls, ent):
        dims = cls.scan_parts(ent)
        cls.fill_units(dims)
        cls.fill_dimensions(dims)
        trait = cls.fill_trait_data(dims, ent)
        return trait

    @classmethod
    def convert_units_to_cm(cls, size_trait):
        for dim in size_trait.dims:
            for key in ("low", "high"):
                value = getattr(dim, key)
                if value is None:
                    continue

                factor = cls.factors_cm.get(dim.units)

                value = round(value * factor, 3)
                setattr(dim, key, value)

        return size_trait


@registry.misc("size_match")
def size_match(ent):
    return Size.size_match(ent)
