Find all specimen type designations in the text.
Specimen types are formal designations of type specimens used in taxonomic descriptions.
The three types to extract are:

  - **holotype**: the single specimen designated as the name-bearing type
  - **allotype**: a specimen of the opposite sex to the holotype
  - **paratypes**: all other specimens designated as types besides the holotype and allotype

For each specimen type found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen, e.g. "male", "female", "nymph" (string or null),
    "type": one of "holotype", "allotype", or "paratypes" (string or null),
    "count": total number of paratypes as a single number (number or null),
    "male_count": number of paratype males as a single number (number or null),
    "female_count": number of paratype females as a single number (number or null).

Notes:
- Holotype and allotype are each single specimens. Return one entry per type with count, male_count, and female_count as null.
- For paratypes, return one entry with the total count and breakdown by sex. If nymphs are included among paratypes, count them separately only if the text explicitly distinguishes them.
- When the text lists paratypes as "1 male, 9 females", set count to 10, male_count to 1, female_count to 9.
- When the text says "same data as holotype" for paratypes, still extract the counts.
- Do not confuse specimen type designations with non-type specimens mentioned in material examined sections.

Return a JSON array of objects.
