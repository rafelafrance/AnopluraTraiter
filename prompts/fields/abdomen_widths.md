Find all abdomen width measurements of the louse specimens described in the text.
Abdomen width is the maximum breadth (lateral extent) of the abdomen, distinct from
abdomen length (anterior-to-posterior extent). It is commonly reported as "maximum
abdomen width" or simply "abdomen width".

In Anoplura descriptions, abdomen width may be given explicitly or abbreviated as
"AW" (e.g. in figure legends or measurement tables). It may appear as a single
value, a mean with range, or a range with sample size and standard deviation.

Common patterns:
  "Maximum abdomen width, 0.485-0.605 mm (mean, 0.540 mm)"
  "AW of allotype, 0.666 mm; mean, 0.697 mm; range, 0.666-0.725 mm"
  "AW, 0.600-0.633 (0.618 ± 0.017)"
  "Maximum width, 0.710-0.790 mm (n = 2)"

For each abdomen width measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "width": single measurement value if only one value is given (number or null),
    "mean_width": mean or average abdomen width if stated (number or null),
    "width_low": lower bound of range (number or null),
    "width_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Maximum abdomen width", "abdomen width", "maximum width" (when context refers to
  the abdomen), and "AW" (when used as an abbreviation for abdomen width) all
  refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "width" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate width_low and width_high
  but leave mean_width as null.
- If only a mean is given without a range, populate mean_width but leave
  width_low and width_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_width.
- Some papers report mean ± standard deviation (e.g. "0.618 ± 0.017"). Extract
  the first number as mean_width. Do not create a range from the standard
  deviation unless a range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract abdomen length (AL), total body length, head width, or thorax
  width — only abdomen width.
- Be careful not to confuse abdomen width with abdomen length. Width measures
  the maximum lateral breadth of the abdomen; length measures its
  anterior-to-posterior extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
