from dataclasses import dataclass

from spacy import registry
from spacy.tokens import Span
from traiter.rules.lat_long import LatLong as T_LatLong

from anoplura.rules.base import Base


@dataclass(eq=False)
class LatLong(T_LatLong, Base):
    @classmethod
    def lat_long_match(cls, ent: Span) -> "LatLong":
        return super().lat_long_match(ent)

    @classmethod
    def lat_long_plus(cls, ent: Span) -> "LatLong":
        return super().lat_long_match(ent)


@registry.misc("lat_long_match")
def color_match(ent: Span) -> LatLong:
    return LatLong.lat_long_match(ent)


@registry.misc("lat_long_plus")
def lat_long_plus(ent: Span) -> LatLong:
    return LatLong.lat_long_plus(ent)
