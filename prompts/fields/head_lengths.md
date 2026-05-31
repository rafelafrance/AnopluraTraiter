Find all head length measurements of the louse specimens described in the text.
Head length is the anterior-to-posterior extent of the head alone, excluding the
thorax and abdomen. It is distinct from head width (maximum breadth of the head).

In Anoplura descriptions, head length may be given explicitly or abbreviated as
"HL" (e.g. in figure legends or measurement tables). It may appear as a single
value, a mean with range, or a range with sample size and standard deviation.

Common patterns:
  "Head length of holotype, 0.187 mm"
  "HL of allotype, 0.200 mm; mean, 0.232 mm; range, 0.200-0.251 mm"
  "HL, 0.181-0.190 (0.187 ± 0.005)"
  "HL = 0.187 ± 0.005"

For each head length measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "length": single measurement value if only one value is given (number or null),
    "mean_length": mean or average head length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Head length", "length of head", and "HL" (when used as an abbreviation for
  head length) all refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "length" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate length_low and length_high
  but leave mean_length as null.
- If only a mean is given without a range, populate mean_length but leave
  length_low and length_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_length.
- Some papers report mean ± standard deviation (e.g. "0.187 ± 0.005"). Extract
  the first number as mean_length. Do not create a range from the standard
  deviation unless a range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract head width (HW), total body length, thorax length, or abdomen
  length — only head length.
- Be careful not to confuse head length with head width. Width measures the
  maximum breadth of the head; length measures its anterior-to-posterior extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
