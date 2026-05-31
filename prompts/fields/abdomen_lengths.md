Find all abdomen length measurements of the louse specimens described in the text.
Abdomen length is the length of the abdominal region alone, excluding the head and
thorax. It is less commonly reported than total body length or abdomen width, but
when present it provides useful allometric data.

In Anoplura descriptions, abdomen length may be given explicitly or abbreviated as
"AL" (e.g. in figure legends or measurement tables). It may appear as a single value,
a mean with range, or a range with sample size.

Common patterns:
  "Abdomen length, 0.650 mm"
  "AL of holotype, 0.720 mm; mean, 0.710 mm; range, 0.680-0.740 mm"
  "length of abdomen, x = 0.580 (0.540 – 0.620, n = 4)"
  "AL, 0.600 mm"

For each abdomen length measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "length": single measurement value if only one value is given (number or null),
    "mean_length": mean or average abdomen length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Abdomen length", "length of abdomen", and "AL" (when used as an abbreviation for
  abdomen length) all refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "length" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate length_low and length_high
  but leave mean_length as null.
- If only a mean is given without a range, populate mean_length but leave
  length_low and length_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_length.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract total body length (TL), head length, thorax length, or abdomen
  width (AW) — only abdomen length.
- Be careful not to confuse abdomen length with abdomen width. Width measures
  the maximum breadth of the abdomen; length measures its anterior-to-posterior
  extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
