from dspy import InputField, OutputField, Signature
from pydantic import BaseModel


class SetaCount(BaseModel):
    seta: str
    sex: str
    body_part: str
    count: str
    rows: str
    each_side: str


class SetaCounts(Signature):
    """
    Analyze the text in the species description and extract this information.

    I need the text exactly as it appears in the text.
    Leave abbreviations exactly as they are.
    If the data field is not found in the text return the default value.

    I want plain text:
      ✅ Use UTF-8 characters only.
      ❌ DO NOT change the text in any way.
      ❌ DO NOT add or delete any punctuation and do not add or delete any spaces.
      ❌ DO NOT include HTML tags
      ❌ DO NOT include HTML entities
      ❌ DO NOT include MATHML tags,
      ❌ DO NOT include Markdown tags.
      ❌ DO NOT add or infer any new information.
      ❌ DO NOT rephrase, summarize, or infer meaning.
      ❌ DO NOT turn phrases into lists or categories.
      ✅ Use exact phrases from the label text only.

    ❌ Do not hallucinate!
    """

    text: str = InputField()

    seta_counts: list[SetaCount] = OutputField(
        default=[],
        desc="""List of seta counts as described in the document.""",
    )

    # seta: str = OutputField(
    #     default="",
    #     desc="""The seta as described in the document""",
    # )
    # count: str = OutputField(
    #     default="",
    #     desc="""How many of these setae are there?""",
    # )
    # rows: str = OutputField(
    #     default="",
    #     desc="""These setae are on which rows?""",
    # )
    # each_side: str = OutputField(
    #     default="",
    #     desc="""Are the setae on each_side?""",
    # )
