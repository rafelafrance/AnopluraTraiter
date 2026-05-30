Find all thorax length measurements of the louse specimens described in the text.
Thorax length is the anterior-to-posterior extent of the thorax alone, excluding the
head and abdomen. It is less commonly reported than thorax width and is distinct from
thorax width (maximum breadth of the thorax).

In Anoplura descriptions, thorax length may be given explicitly or abbreviated as
"THL" (e.g. in figure legends or measurement tables). It may appear as a single
value, a mean with range, or a range with sample size and standard deviation.

Common patterns:
  "Thorax length of holotype, 0.085 mm"
  "THL of allotype, 0.105 mm; mean, 0.110 mm; range, 0.100-0.120 mm"
  "THL, 0.080-0.095 (0.087 ± 0.005)"
  "THL = 0.087 ± 0.005"

For each thorax length measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "length": single measurement value if only one value is given (number or null),
    "mean_length": mean or average thorax length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Thorax length", "length of thorax", and "THL" (when used as an abbreviation for
  thorax length) all refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "length" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate length_low and length_high
  but leave mean_length as null.
- If only a mean is given without a range, populate mean_length but leave
  length_low and length_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_length.
- Some papers report mean ± standard deviation (e.g. "0.087 ± 0.005"). Extract
  the first number as mean_length. Do not create a range from the standard
  deviation unless a range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract thorax width (THW), total body length, head length, or abdomen
  length — only thorax length.
- Be careful not to confuse thorax length with thorax width. Width measures the
  maximum breadth of the thorax; length measures its anterior-to-posterior extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
