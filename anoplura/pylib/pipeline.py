import spacy
from spacy.language import Language
from spacy.tokens import Doc
from traiter.pipes import delete, extensions, tokenizer
from traiter.rules.number import Number

from anoplura.rules import delete_unlinked, sex_linker
from anoplura.rules.count import Count
from anoplura.rules.count_linker import CountLinker
from anoplura.rules.date_ import Date
from anoplura.rules.description_linker import DescriptionLinker
from anoplura.rules.elevation import Elevation
from anoplura.rules.gonopod import Gonopod
from anoplura.rules.group import Group
from anoplura.rules.lat_long import LatLong
from anoplura.rules.morphology import Morphology
from anoplura.rules.part import Part
from anoplura.rules.part_linker import PartLinker
from anoplura.rules.plate import Plate
from anoplura.rules.position import Position
from anoplura.rules.range import Range
from anoplura.rules.relative_position import RelativePosition
from anoplura.rules.relative_size import RelativeSize
from anoplura.rules.roman import Roman
from anoplura.rules.sclerotization import Sclerotization
from anoplura.rules.sclerotization_linker import SclerotizationLinker
from anoplura.rules.segment import Segment
from anoplura.rules.seta import Seta
from anoplura.rules.sex import Sex
from anoplura.rules.sexual_dimorphism import SexualDimorphism
from anoplura.rules.sexual_dimorphism_linker import SexualDimorphismLinker
from anoplura.rules.shape import Shape
from anoplura.rules.size import Size
from anoplura.rules.size_description import SizeDescription
from anoplura.rules.size_linker import SizeLinker
from anoplura.rules.specimen_type import SpecimenType
from anoplura.rules.sternite import Sternite
from anoplura.rules.subpart import Subpart
from anoplura.rules.subpart_linker import SubpartLinker
from anoplura.rules.taxon import Taxon
from anoplura.rules.tergite import Tergite

# from traiter.pipes.debug import ents


def build() -> Language:
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    if not Doc.has_extension("unlinked"):
        Doc.set_extension("unlinked", default=[])

    tokenizer.setup_tokenizer(nlp)

    Taxon.pipe(nlp)
    Sex.pipe(nlp)

    Seta.pipe(nlp)
    Part.pipe(nlp)

    LatLong.pipe(nlp)
    Elevation.pipe(nlp)
    Date.pipe(nlp)

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
    Count.pipe(nlp)

    SexualDimorphism.pipe(nlp)
    Sclerotization.pipe(nlp)

    Group.pipe(nlp)
    Morphology.pipe(nlp)
    Position.pipe(nlp)
    RelativePosition.pipe(nlp)
    RelativeSize.pipe(nlp)
    Shape.pipe(nlp)
    SizeDescription.pipe(nlp)

    SclerotizationLinker.pipe(nlp)
    DescriptionLinker.pipe(nlp)
    CountLinker.pipe(nlp)
    SizeLinker.pipe(nlp)
    SubpartLinker.pipe(nlp)
    SexualDimorphismLinker.pipe(nlp)

    PartLinker.pipe(nlp)

    sex_linker.pipe(nlp)

    delete.pipe(nlp, delete=["number", "range", "roman"])
    delete_unlinked.pipe(nlp, ["count", "size", "description"])

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
