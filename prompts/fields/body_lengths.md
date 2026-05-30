Find all total body length measurements of the louse specimens described in the text.
Body lengths are given for holotypes, allotypes, paratypes, and sometimes nymphs.
They may appear as a single value, a mean with range, or a range with sample size.

Common patterns in Anoplura descriptions:
  "Total body length of holotype, 1.021 mm"
  "Body length of allotype, 1.400 mm; mean, 1.295 mm; range, 1.233-1.400 mm (n = 3)"
  "Total body length, x = 1.014 (0.950 – 1.130, n = 5)"
  "mean, 1.507 mm; range, 1.445-1.600 mm"

For each body length measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "third instar" (string or null),
    "type": specimen type designation, e.g. "holotype", "allotype", "paratype" (string or null),
    "length": single measurement value if only one value is given (number or null),
    "mean_length": mean or average body length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Total body length" and "body length" both refer to the same measurement.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "length" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate length_low and length_high
  but leave mean_length as null.
- If only a mean is given without a range, populate mean_length but leave
  length_low and length_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_length.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract head lengths, thorax lengths, abdomen lengths, or other
  partial-body measurements — only total body length.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
