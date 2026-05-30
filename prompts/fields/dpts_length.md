Find all DPTS (dorsal principal thoracic seta) length measurements of the louse
specimens described in the text.

DPTS is a distinctive seta on the dorsal surface of the thorax. Its length is a
key diagnostic character in Anoplura taxonomy — papers routinely report whether
it is short, moderate, or long, and give precise measurements. The DPTS may be
borne on a small protuberance or directly on the thoracic surface. It is absent
in some species.

In Anoplura descriptions, DPTS length may be given explicitly or abbreviated as
"DPTS". It may appear as a single value, a mean with range, or a qualitative
description with or without a numeric value.

Common patterns:
  "Dorsal principal thoracic seta (DPTS) length, 0.105 mm"
  "DPTS length of allotype, 0.145 mm; mean, 0.141 mm; range, 0.138-0.145 mm"
  "DPTS length x = 0.0340 (0.0275 – 0.0375, n = 5)"
  "DPTS length 0.117-0.130 mm, mean 0.121 mm (n = 7)"
  "Dorsal principal thoracic setae (DPTS) moderate in length (0.14 mm)"

For each DPTS length measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "length": single measurement value if only one value is given (number or null),
    "mean_length": mean or average DPTS length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null),
    "description": qualitative description of DPTS length, e.g. "short", "moderate",
      "long" (string or null).

Notes:
- "Dorsal principal thoracic seta", "dorsal principal thoracic setae", and "DPTS"
  all refer to the same structure.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "length" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate length_low and length_high
  but leave mean_length as null.
- If only a mean is given without a range, populate mean_length but leave
  length_low and length_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_length.
- Some papers give only a qualitative description (e.g. "short DPTS", "long DPTS",
  "moderate in length"). In these cases, set description to the qualitative term
  and leave all numeric fields as null.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract measurements of other thoracic setae (e.g. mesothoracic setae,
  DMsS) — only DPTS.
- If the text states DPTS is absent or "no evidence of DPTS", do not create an
  entry for it.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
