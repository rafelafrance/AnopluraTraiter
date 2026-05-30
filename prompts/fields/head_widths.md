Find all head width measurements of the louse specimens described in the text.
Head width is the maximum breadth (lateral extent) of the head, distinct from head
length (anterior-to-posterior extent). It is commonly reported as "maximum head
width" or simply "head width".

In Anoplura descriptions, head width may be given explicitly or abbreviated as
"HW" (e.g. in figure legends or measurement tables). It may appear as a single
value, a mean with range, or a range with sample size and standard deviation.

Common patterns:
  "Maximum head width of holotype, 0.190 mm"
  "Maximum head width of allotype, 0.211 mm; mean, 0.210 mm; range, 0.205-0.215 mm"
  "Maximum head width, 0.150-0.163 mm (mean, 0.17 mm, n = 4)"
  "HW, 0.159-0.183 (0.168 ± 0.013)"

For each head width measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "width": single measurement value if only one value is given (number or null),
    "mean_width": mean or average head width if stated (number or null),
    "width_low": lower bound of range (number or null),
    "width_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Maximum head width", "head width", "maximum width" (when context refers to the
  head), and "HW" (when used as an abbreviation for head width) all refer to the
  same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "width" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate width_low and width_high
  but leave mean_width as null.
- If only a mean is given without a range, populate mean_width but leave
  width_low and width_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_width.
- Some papers report mean ± standard deviation (e.g. "0.168 ± 0.013"). Extract
  the first number as mean_width. Do not create a range from the standard
  deviation unless a range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract head length (HL), total body length, thorax width, or abdomen
  width — only head width.
- Be careful not to confuse head width with head length. Width measures the
  maximum lateral breadth of the head; length measures its anterior-to-posterior
  extent.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
