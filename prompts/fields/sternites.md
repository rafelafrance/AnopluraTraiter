Find all mentions of abdominal sternites in the text.
Sternites are ventral abdominal sclerites, typically described by their count per segment,
their individual numbering, setae counts, or their absence.

Sternites have their own global numbering that runs independently of segment numbers.
For example, "sternites 1 and 2 on segment 2" means two sternites (numbered 1 and 2)
are located on abdominal segment 2. Multiple sternites may share a single segment.

For each sternite or sternite group found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region where sternites are described, typically abdomen (string or null),
    "segment": the abdominal segment number(s) where the sternite(s) are located (string or null),
    "number": the sternite's own number or number range, e.g. "1", "3–10", "II" (string or null),
    "count": number of sternites on that segment or in total, if stated (string or null),
    "missing": true if sternites are explicitly absent or lacking in the region or segment (true or null),
    "description": morphological description including shape, sclerotization, setae, or other features (string or null).

Notes:
- Sternite numbers are not the same as segment numbers. "Sternite 11 on segment 7" means sternite number 11 is located on segment 7.
- When a range of segments is given (e.g. "sternites 3–10 on segments 3–6"), keep the range as-is.
- Distinguish sternite numbers from setae counts: "Sternite 1 with 6 StAS" means sternite number 1 has 6 setae, not 6 sternites.
- If the text states sternites are absent, lacking, or reduced, set missing to true.
- When sternites are described without a specific segment, leave segment as null and capture details in description.
- Do not confuse tergites (dorsal) with sternites (ventral).

Return a JSON array of objects.
