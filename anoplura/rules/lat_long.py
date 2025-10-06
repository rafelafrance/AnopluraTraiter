from dataclasses import dataclass

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry
from traiter.rules.lat_long import LatLong as T_LatLong

from anoplura.rules.base import Base


@dataclass(eq=False)
class LatLong(Base, T_LatLong):
    def format(self) -> str:
        val = f"{self._trait}: {self.lat_long}"
        if self.uncertainty:
            val += f" ± {self.uncertainty:f}"
        if self.units:
            val += f" {self.units}"
        if self.datum:
            val += f" {self.datum}"
        return val

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_LatLong.pipe(nlp)

    @classmethod
    def lat_long_match(cls, ent: Span) -> "LatLong":
        return super().lat_long_match(ent)

    @classmethod
    def lat_long_plus(cls, ent: Span) -> "LatLong":
        return super().lat_long_plus(ent)


@registry.misc("lat_long_match")
def lat_long_match(ent: Span) -> LatLong:
    return LatLong.lat_long_match(ent)


@registry.misc("lat_long_plus")
def lat_long_plus(ent: Span) -> LatLong:
    return LatLong.lat_long_plus(ent)
