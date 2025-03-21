import spacy
from traiter.pylib.pipes import extensions, tokenizer
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.number import Number

from anoplura.rules.part import Part
from anoplura.rules.part_size import PartSize
from anoplura.rules.range import Range
from anoplura.rules.sclerotized import Sclerotized
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.seta_size import SetaSize
from anoplura.rules.sex import Sex
from anoplura.rules.size import Size
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

    Part.pipe(nlp)

    LatLong.pipe(nlp)
    Elevation.pipe(nlp)

    Number.pipe(nlp)
    Range.pipe(nlp)
    Size.pipe(nlp)

    SubpartCount.pipe(nlp)
    SetaCount.pipe(nlp)
    SetaSize.pipe(nlp)

    Sclerotized.pipe(nlp)

    PartSize.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
