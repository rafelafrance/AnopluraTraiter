from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.lat_long import LatLong as T_LatLong

from anoplura.rules.base import Base


@dataclass(eq=False)
class LatLong(Base, T_LatLong):
    _paragraph: str | None = None
    sex: str | None = None

    @classmethod
    def pipe(cls, nlp: Language):
        T_LatLong.pipe(nlp)
