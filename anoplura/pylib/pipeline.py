import spacy
from traiter.pylib.pipes import extensions, tokenizer
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.number import Number

from anoplura.rules import clean_traits
from anoplura.rules.body_part import BodyPart
from anoplura.rules.body_part_size import PartSize
from anoplura.rules.gonopod import Gonopod
from anoplura.rules.gonopod_seta import GonopodSeta
from anoplura.rules.plate import Plate
from anoplura.rules.plate_seta import PlateSeta
from anoplura.rules.range import Range
from anoplura.rules.roman import Roman
from anoplura.rules.sclerotized import Sclerotized
from anoplura.rules.segment import Segment
from anoplura.rules.segment_sternite_count import SegmentSterniteCount
from anoplura.rules.segment_tergite_count import SegmentTergiteCount
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
from anoplura.rules.tergite import Tergite
from anoplura.rules.tergite_count import TergiteCount
from anoplura.rules.tergite_seta import TergiteSeta

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
    Gonopod.pipe(nlp)
    Sternite.pipe(nlp)
    Tergite.pipe(nlp)

    SubpartCount.pipe(nlp)
    SetaCount.pipe(nlp)
    SterniteCount.pipe(nlp)
    TergiteCount.pipe(nlp)

    SterniteSeta.pipe(nlp)
    TergiteSeta.pipe(nlp)
    PlateSeta.pipe(nlp)
    GonopodSeta.pipe(nlp)

    SegmentSterniteCount.pipe(nlp)
    SegmentTergiteCount.pipe(nlp)

    Sclerotized.pipe(nlp)

    clean_traits.pipe(nlp, traits=["roman"])

    Size.pipe(nlp)
    SetaSize.pipe(nlp)
    PartSize.pipe(nlp)

    clean_traits.pipe(nlp, traits=["number", "range"])

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
