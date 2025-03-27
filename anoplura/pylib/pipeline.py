import spacy
from traiter.pylib.pipes import extensions, tokenizer
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.number import Number

from anoplura.rules import clean
from anoplura.rules.body_part import BodyPart
from anoplura.rules.body_part_size import PartSize
from anoplura.rules.plate import Plate
from anoplura.rules.range import Range
from anoplura.rules.roman import Roman
from anoplura.rules.sclerotized import Sclerotized
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.seta_size import SetaSize
from anoplura.rules.sex import Sex
from anoplura.rules.size import Size
from anoplura.rules.sternite import Sternite
from anoplura.rules.sternite_count import SterniteCount
from anoplura.rules.sternite_seta import SterniteSeta
from anoplura.rules.subpart_count import SubpartCount
from anoplura.rules.taxon import Taxon

# from traiter.pylib.pipes.debug import tokens


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    Taxon.pipe(nlp)
    Sex.pipe(nlp)
    Seta.pipe(nlp)
    BodyPart.pipe(nlp)

    LatLong.pipe(nlp)
    Elevation.pipe(nlp)

    Roman.pipe(nlp)
    Number.pipe(nlp)
    Range.pipe(nlp)

    Segment.pipe(nlp)
    Plate.pipe(nlp)
    Sternite.pipe(nlp)

    SubpartCount.pipe(nlp)
    SetaCount.pipe(nlp)
    SterniteCount.pipe(nlp)

    SterniteSeta.pipe(nlp)

    Sclerotized.pipe(nlp)

    clean.pipe(nlp, ["roman"])
    Size.pipe(nlp)
    SetaSize.pipe(nlp)
    PartSize.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
