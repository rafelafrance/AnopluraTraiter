from dataclasses import dataclass

from spacy import registry
from spacy.tokens import Span
from traiter.rules.elevation import Elevation as T_Elevation

from anoplura.rules.base import Base


@dataclass(eq=False)
class Elevation(T_Elevation, Base):
    @classmethod
    def elevation_match(cls, ent: Span) -> "Elevation":
        return super().elevation_match(ent)


@registry.misc("elevation_match")
def elevation_match(ent: Span) -> Elevation:
    return Elevation.elevation_match(ent)
