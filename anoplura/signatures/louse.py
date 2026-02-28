from typing import Literal

from dspy import InputField, OutputField, Signature


class BaseAnnotation(Signature):
    """For each annotation return the actual text of the annotation."""

    relevant_text: str = OutputField(
        description="Include the text used to extract the information",
    )


class SetaCount(BaseAnnotation):
    """Given the following text, find the setae count on all body parts."""

    seta_name: str = OutputField(description="The seta name which may be abbreviated")
    part: str = OutputField(
        description="What body part is the seta on? This typically in the seta name",
    )
    rows: list[str] = OutputField(description="Are the seta grouped into rows?")
    count: list[int] = OutputField(
        description="How many setae are there? This may be a number or a range",
    )
    side: str = OutputField(description="Are the seta counts reported as per side")
    sex: Literal["female", "male", "both"] = OutputField(
        description="What sex is the seta on?",
    )
    size: str = OutputField(description="What size are the seta? Large small short...")
    position: str = OutputField(description="Where are setae located on the part?")
    relative_position: str = OutputField(
        description="Are the setae near another part?",
    )


class SetaeCounts(Signature):
    """
    Given the following text, find the setae count on all body parts.

    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    """

    text: str = InputField()

    species: str = OutputField(description="Species name")
    setae_counts: list[SetaCount] = OutputField(
        default=[],
        description="Seta count annotations.",
    )


class Elevation(BaseAnnotation):
    """The specimens were collected at what altitude."""

    elevation: float = OutputField(
        description="Either the only value or the low value of a range",
    )
    elevation_high: float | None = OutputField(description="The high value of a range")
    units: str = OutputField(description="Feet meters whatever")
    about: bool = OutputField(description="Is this an estimated value?")


class SpecimenType(BaseAnnotation):
    """Specimen types, like holotype, allotype, etc. often have length annotations."""

    type: str = OutputField(description="Specimen type")
    length: float = OutputField(description="Length of the specimen type")
    length_range: list[float] = OutputField(description="Length of the specimen type")
    sample_size: int = OutputField(
        description="How many samples were taken to get the range.",
    )
    mean_length: float = OutputField(
        description="What is the mean length of all of the specimens sampled?",
    )
    length_units: str = OutputField(
        description="The length is expressed in what units?",
    )


class Gonopod(BaseAnnotation):
    """Gonopods."""

    gonopod_numbers: list[int] = OutputField(
        description="Gonopods are numbered with Roman numerals",
    )
    shape: str = OutputField(description="Gonopods shape")
    setae: list[SetaCount] = OutputField(
        description="Seta (setae) associated with the gonopods?",
    )


class Louse(Signature):
    """
    Parse these annotations in louse species description.

    Only get annotations from the document itself.
    If you cannot find the data do not include it.
    """

    text: str = InputField()

    species: str = OutputField(description="Species name")
    elevation: Elevation | None = OutputField(
        description="Elevation which may be a range",
    )
    setae_counts: list[SetaCount] = OutputField(
        default=[],
        description="Seta count annotations.",
    )
    gonopods: list[Gonopod] = OutputField(
        default=[],
        description="Gonopod annotations.",
    )
    specimen_type: list[SpecimenType] = OutputField(
        default=[],
        description="Specimen type.",
    )
