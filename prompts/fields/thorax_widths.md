Find all thorax width measurements of the louse specimens described in the text.
Thorax width is the maximum breadth (lateral extent) of the thorax, distinct from
thorax length (anterior-to-posterior extent). It is commonly reported as "maximum
thorax width" or simply "thorax width".

In Anoplura descriptions, thorax width may be given explicitly or abbreviated as
"THW" (e.g. in figure legends or measurement tables). It may appear as a single
value, a mean with range, or a range with sample size and standard deviation.

Common patterns:
  "Maximum thorax width of allotype, 0.295 mm; mean, 0.308 mm; range, 0.295-0.325 mm"
  "Maximum thorax width, 0.280-0.305 mm (mean, 0.290 mm, n = 3)"
  "Maximum width, 0.285-0.295 mm (n = 2)"
  "THW, 0.250-0.267 (0.259 ± 0.008)"

For each thorax width measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "width": single measurement value if only one value is given (number or null),
    "mean_width": mean or average thorax width if stated (number or null),
    "width_low": lower bound of range (number or null),
    "width_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Maximum thorax width", "thorax width", "maximum width" (when context refers to
  the thorax), and "THW" (when used as an abbreviation for thorax width) all
  refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "width" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate width_low and width_high
  but leave mean_width as null.
- If only a mean is given without a range, populate mean_width but leave
  width_low and width_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_width.
- Some papers report mean ± standard deviation (e.g. "0.259 ± 0.008"). Extract
  the first number as mean_width. Do not create a range from the standard
  deviation unless a range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract thorax length (THL), total body length, head width, or abdomen
  width — only thorax width.
- Be careful not to confuse thorax width with thorax length. Width measures the
  maximum lateral breadth of the thorax; length measures its anterior-to-posterior
  extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
