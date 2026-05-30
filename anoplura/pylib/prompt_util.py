"""Handle prompt Markdown files."""

import re
from pathlib import Path

PROMPT_DIR = Path("prompts")
FIELD_PROMPT_DIR = PROMPT_DIR / "fields"

# ---------------------------------------------------------------------
# The system prompt section
SYS_PROMPT = re.compile(r"^System\s+Prompt", flags=re.IGNORECASE)

# The output fields section
OUT_FIELDS = re.compile(r"^Output\s+Fields", flags=re.IGNORECASE)


def read_lm_prompt(path: Path) -> tuple[str, list[str]]:
    """Read a Markdown prompt file & return the system prompt and field name list."""
    sys_prompt: str = ""
    field_names: list[str] = []

    with path.open() as f:
        raw = f.read()

    # Split Markdown file into sections using headers
    sections = re.split(r"^(?<!#)#\s", raw, flags=re.MULTILINE)

    for section in sections:
        sect = section.strip()

        # Get system prompt section
        if SYS_PROMPT.match(section):
            sys_prompt = SYS_PROMPT.sub("", section).strip()

        # Get output fields list section
        elif OUT_FIELDS.match(section):
            sect = OUT_FIELDS.sub("", section).strip()
            links = re.findall(r"\([\w/]+\.md\)", sect)
            field_names = [lk.removeprefix("(").removesuffix(".md)") for lk in links]

    return sys_prompt, field_names


# ---------------------------------------------------------------------
def get_field_prompts(field_names: list[str]) -> dict[str, str]:
    """Get prompts of all fields given in the field list."""
    prompts = {}
    for field_name in field_names:
        prompt_path = Path(PROMPT_DIR) / f"{field_name}.md"
        with prompt_path.open() as f:
            prompt = f.read()
        prompts[field_name] = prompt
    return prompts
