import spacy
from traiter.pipes import delete, extensions, tokenizer
from traiter.rules.number import Number

from anoplura.rules import sex_assignment
from anoplura.rules.count import Count
from anoplura.rules.elevation import Elevation
from anoplura.rules.gonopod import Gonopod
from anoplura.rules.lat_long import LatLong
from anoplura.rules.part import Part
from anoplura.rules.part_count import PartCount
from anoplura.rules.part_mean import PartMean
from anoplura.rules.part_sample import PartSample
from anoplura.rules.part_sclerotization import PartSclerotization
from anoplura.rules.part_stats import PartStats
from anoplura.rules.plate import Plate
from anoplura.rules.range import Range
from anoplura.rules.roman import Roman
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.sex import Sex
from anoplura.rules.sex_count import SexCount
from anoplura.rules.sexual_dimorphism import SexualDimorphism
from anoplura.rules.size import Size
from anoplura.rules.specimen_type import SpecimenType
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from anoplura.rules.taxon import Taxon
from anoplura.rules.tergite import Tergite

# from traiter.pipes.debug import ents


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

    Roman.pipe(nlp)
    Number.pipe(nlp)
    Range.pipe(nlp)

    Segment.pipe(nlp)
    Plate.pipe(nlp)
    Gonopod.pipe(nlp)
    Sternite.pipe(nlp)
    Tergite.pipe(nlp)

    Subpart.pipe(nlp)

    delete.pipe(nlp, delete=["roman"])

    SpecimenType.pipe(nlp)

    Size.pipe(nlp)
    PartMean.pipe(nlp)
    PartSample.pipe(nlp)
    PartStats.pipe(nlp)

    PartSclerotization.pipe(nlp)

    Count.pipe(nlp)

    SexCount.pipe(nlp)
    PartCount.pipe(nlp)
    SetaCount.pipe(nlp)

    SexualDimorphism.pipe(nlp)

    delete.pipe(nlp, delete=["number", "range", "roman", "count"])

    sex_assignment.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
