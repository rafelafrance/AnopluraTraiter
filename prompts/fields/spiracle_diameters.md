Find all spiracle diameter measurements of the louse specimens described in the text.
Spiracles are respiratory openings on the body surface. The most commonly measured
spiracle is the mesothoracic spiracle on the thorax, but abdominal spiracles
(especially on specific segments like the 5th abdominal segment) are also reported.
Spiracle diameter is a key diagnostic character in Anoplura taxonomy.

In Anoplura descriptions, spiracle diameter may be given as a single value, a mean
with range, or a range with sample size and standard deviation. It is commonly
described as "mesothoracic spiracle diameter" or "spiracle diameter on [segment]".

Common patterns:
  "Mesothoracic spiracle diameter, 0.018 mm"
  "Mesothoracic spiracle diameter x = 0.0165 (0.0125 – 0.0175, n = 5)"
  "Mesothoracic spiracle maximum diameter 0.028-0.033 mm, mean 0.031 mm"
  "spiracle diameter on 5th abdominal segment, x = 0.0176 (range = 0.0150 – 0.0200)"

For each spiracle diameter measurement found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string),
    "sex": sex or life stage of the specimen, e.g. "male", "female", "nymph", "first instar" (string or null),
    "location": location of the spiracle measured, e.g. "mesothorax",
      "5th abdominal segment", "abdominal segment 5" (string or null),
    "diameter": single measurement value if only one value is given (number or null),
    "mean_diameter": mean or average spiracle diameter if stated (number or null),
    "diameter_low": lower bound of range (number or null),
    "diameter_high": upper bound of range (number or null),
    "n": sample size if stated (number or null),
    "units": unit of measurement, typically "mm" (string or null).

Notes:
- "Mesothoracic spiracle diameter", "spiracle diameter", and "spiracle maximum
  diameter" all refer to the same measurement when the location is the mesothorax.
- When the text specifies an abdominal spiracle (e.g. "spiracle diameter on 5th
  abdominal segment"), set location to that segment.
- When a holotype or allotype value is given alongside a mean and range, return one
  entry with the holotype/allotype value in "diameter" and the statistics in their
  respective fields. Do not split them into separate entries.
- If only a range is given without a mean, populate diameter_low and diameter_high
  but leave mean_diameter as null.
- If only a mean is given without a range, populate mean_diameter but leave
  diameter_low and diameter_high as null.
- The "x =" notation means mean. Extract the value after "x =" as mean_diameter.
- Some papers report mean ± standard deviation. Extract the first number as
  mean_diameter. Do not create a range from the standard deviation unless a
  range is also explicitly given.
- When ranges use "–" (en-dash) or "-" (hyphen) as separator, treat both the same.
- Do not extract qualitative descriptions of spiracle size alone (e.g. "large
  spiracles", "small spiracles") — only numeric diameter measurements.
  Qualitative descriptions are handled by the spiracles prompt.
- If units are not explicitly stated but the context makes it clear (e.g. all other
  measurements in the section are in mm), set units to "mm".
- When the text says "n = 5" or "(n = 5)", extract 5 as the sample size.

Return a JSON array of objects.
