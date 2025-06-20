import spacy
from traiter.pipes import delete, extensions, tokenizer
from traiter.rules.number import Number

from anoplura.rules import sex_assignment
from anoplura.rules.elevation import Elevation
from anoplura.rules.gonopod import Gonopod
from anoplura.rules.gonopod_seta import GonopodSeta
from anoplura.rules.lat_long import LatLong
from anoplura.rules.part import Part
from anoplura.rules.part_mean import PartMean
from anoplura.rules.part_range import PartRange
from anoplura.rules.part_sample import PartSample
from anoplura.rules.part_sclerotization import PartSclerotization
from anoplura.rules.part_shape import PartShape
from anoplura.rules.part_size import PartSize
from anoplura.rules.part_stats import PartStats
from anoplura.rules.plate import Plate
from anoplura.rules.plate_seta import PlateSeta
from anoplura.rules.range import Range
from anoplura.rules.roman import Roman
from anoplura.rules.segment import Segment
from anoplura.rules.segment_comparison import SegmentComparison
from anoplura.rules.segment_sternite_count import SegmentSterniteCount
from anoplura.rules.segment_tergite_count import SegmentTergiteCount
from anoplura.rules.seta import Seta
from anoplura.rules.seta_count import SetaCount
from anoplura.rules.seta_position import SetaPosition
from anoplura.rules.seta_row import SetaRow
from anoplura.rules.seta_size import SetaSize
from anoplura.rules.sex import Sex
from anoplura.rules.sex_count import SexCount
from anoplura.rules.sexual_dimorphism import SexualDimorphism
from anoplura.rules.shape import Shape
from anoplura.rules.size import Size
from anoplura.rules.specimen_type import SpecimenType
from anoplura.rules.sternite import Sternite
from anoplura.rules.sternite_count import SterniteCount
from anoplura.rules.sternite_seta import SterniteSeta
from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_count import SubpartCount
from anoplura.rules.taxon import Taxon
from anoplura.rules.tergite import Tergite
from anoplura.rules.tergite_count import TergiteCount
from anoplura.rules.tergite_seta import TergiteSeta

# from traiter.pipes.debug import tokens


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    Taxon.pipe(nlp)
    Sex.pipe(nlp)
    Shape.pipe(nlp)
    Seta.pipe(nlp)
    Part.pipe(nlp)
    Subpart.pipe(nlp)

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
    SetaRow.pipe(nlp)
    SterniteCount.pipe(nlp)
    TergiteCount.pipe(nlp)

    SterniteSeta.pipe(nlp)
    TergiteSeta.pipe(nlp)
    PlateSeta.pipe(nlp)
    GonopodSeta.pipe(nlp)

    SegmentSterniteCount.pipe(nlp)
    SegmentTergiteCount.pipe(nlp)
    SegmentComparison.pipe(nlp)

    PartSclerotization.pipe(nlp)

    PartShape.pipe(nlp)

    delete.pipe(nlp, traits=["roman"])

    SpecimenType.pipe(nlp)
    SexualDimorphism.pipe(nlp)
    SexCount.pipe(nlp)

    Size.pipe(nlp)
    SetaSize.pipe(nlp)
    PartSize.pipe(nlp)
    PartMean.pipe(nlp)
    PartRange.pipe(nlp)
    PartSample.pipe(nlp)
    PartStats.pipe(nlp)

    SetaPosition.pipe(nlp)  # Do this last or near last

    delete.pipe(nlp, traits=["number", "range", "shape"])

    sex_assignment.pipe(nlp)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
