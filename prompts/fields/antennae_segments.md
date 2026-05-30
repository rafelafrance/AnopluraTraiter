Find all mentions of antennae segment counts and segment-level descriptions in the
text. Antennae are paired sensory appendages on the head of the louse. The number of
segments is a key diagnostic character in Anoplura taxonomy — most species have
5-segmented antennae, but variation occurs. Individual segments are often described
by their relative size, shape, or modifications.

In Anoplura descriptions, antennae are commonly described as "5-segmented",
"five-segmented", "5 segmented", or "Antennae 5segmented". Individual segments may
be described by their proportions (e.g. "first segment much larger than others",
"third segment unmodified", "fourth and fifth segments small").

For each antennae segment count or segment-level description found, return an object
with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "count": total number of antennal segments as a number, e.g. 5 (number or null),
    "segment_descriptions": descriptions of individual segments, e.g.
      "first segment broader than long", "third segment unmodified" (string or null).

Notes:
- "5-segmented", "five-segmented", "5 segmented", "5segmented", and "Antennae
  5-segmented" all indicate a segment count of 5. Convert spelled-out numbers
  (e.g. "five") to numeric form in the count field.
- When segment-level descriptions are given alongside the count, include them in
  segment_descriptions. If multiple segments are described, join them with
  semicolons (e.g. "first segment broader than long; third segment unmodified").
- "Basal segment" refers to the first (proximal) antennal segment.
- "Unmodified" means the segment lacks secondary sexual characteristics or
  structural modifications.
- Do not extract head setae names that contain "antennal" (e.g. "dorsal
  preantennal head seta", "supraantennal head seta") — these are head setae,
  not antennae segments.
- If only the total segment count is given without segment-level detail, set
  segment_descriptions to null.

Return a JSON array of objects.
