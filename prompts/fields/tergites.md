Find all mentions of abdominal tergites in the text.
Tergites are dorsal abdominal sclerites, typically described by their count per segment,
their individual numbering, setae counts, or their absence.

Tergites have their own global numbering that runs independently of segment numbers.
For example, "tergites 1 and 2 on segment 2" means two tergites (numbered 1 and 2)
are located on abdominal segment 2. Multiple tergites may share a single segment.

For each tergite or tergite group found, return an object with these exact fields:
    "species": species name (string),
    "sex": sex of the specimen (string or null),
    "body_region": body region where tergites are described, typically abdomen (string or null),
    "segment": the abdominal segment number(s) where the tergite(s) are located (string or null),
    "number": the tergite's own number or number range, e.g. "1", "3–10", "II" (string or null),
    "count": number of tergites on that segment or in total, if stated (string or null),
    "missing": true if tergites are explicitly absent or lacking in the region or segment (true or null),
    "description": morphological description including shape, sclerotization, setae, or other features (string or null).

Notes:
- Tergite numbers are not the same as segment numbers. "Tergite 18 on segment 8" means tergite number 18 is located on segment 8.
- When a range of segments is given (e.g. "tergites 3–6 on segments 4–7"), keep the range as-is.
- Distinguish tergite numbers from setae counts: "Tergite 1 with 4 TeAS" means tergite number 1 has 4 setae, not 4 tergites.
- If the text states tergites are absent, lacking, or reduced, set missing to true.
- When tergites are described without a specific segment, leave segment as null and capture details in description.
- Do not confuse tergites (dorsal) with sternites (ventral).

Return a JSON array of objects.
