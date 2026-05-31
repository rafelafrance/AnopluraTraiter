Find all phrases containing "except" (or "exception") that convey morphological
trait information about the louse being described.

In taxonomic descriptions of Anoplura, "except" phrases are a common way to state
a general trait and then note the specific cases where that trait does not apply.
These phrases encode dense trait information: the baseline pattern, the exception,
and the structures or locations involved.

Common patterns include:

  - **Absence with location exception**: "no other setae present on thorax except on legs"
    (traits are absent everywhere except specific locations)
  - **Presence with location exception**: "present except on sternites 1–3"
    (traits are present everywhere except specific locations)
  - **General rule with structural exception**: "tergites subrectangular except tergite 18
    which is very broad" (a trait holds for most structures except specific ones)
  - **Sex/form comparison**: "as in male except for plate VII, which has a large curved
    extension" (one sex shares traits with the other except for noted differences)
  - **Absence with structural exception**: "lacking tergites and sternites except for
    ventral subgenital plate" (structures are absent except specific ones)

For each phrase found, return an object with these exact fields:
    "species": species name inferred from the surrounding context (string),
    "sex": sex of the specimen the phrase describes, e.g. "male", "female", "nymph" (string or null),
    "phrase": the full sentence or clause containing "except" or "exception", captured verbatim (string or null),
    "general_trait": the baseline trait or pattern stated before the exception (string or null),
    "exception": what differs from the general pattern (string or null),
    "body_region": body region the phrase refers to, e.g. "thorax", "abdomen", "head" (string or null).

Notes:
- Capture the full sentence or clause, not just a fragment. Include enough context
  so the general pattern and the exception are both clear.
- When the text says "as in male except..." or "as in female except...", set sex
  to the sex currently being described (the one doing the comparing).
- Do not extract "except" phrases from non-morphological contexts such as
  geographic distributions ("found throughout Africa except...") or host records.
- If the same sentence contains multiple distinct exceptions, return separate
  entries for each.
- Preserve the original wording verbatim in the "phrase" field. Do not rephrase
  or summarize.

Return a JSON array of objects.
