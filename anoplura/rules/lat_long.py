from dataclasses import dataclass

from spacy.language import Language
from traiter.rules.lat_long import LatLong as T_LatLong

from anoplura.rules.base import Base


@dataclass(eq=False)
class LatLong(Base, T_LatLong):
    sex: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        T_LatLong.pipe(nlp)
