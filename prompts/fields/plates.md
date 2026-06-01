Find all mentions of anatomical plates described in the text.
Plates commonly include paratergal plates, subgenital plates, thoracic sternal plates, and ventral genital plates.

Plates have their own global numbering that runs independently of segment numbers.
For example, "plates 1 and 2 on segment 2" means two plates (numbered 1 and 2)
are located on segment 2. Multiple plates may share a single segment.

For each distinct plate or plate group found, return an object with these exact fields:
    "species": species name (string),
    "sex": sex of the specimen (string or null),
    "plate_type": the kind of plate, e.g. paratergal plate, subgenital plate, thoracic sternal plate (string or null),
    "segment": the segment number(s) where the plate(s) are located (string or null),
    "number": the plate's own number or number range, e.g. "1", "3–10", "II" (string or null),
    "body_region": body region where the plate is located, e.g. thorax, abdomen, genitalia (string or null),
    "description": morphological description of the plate including shape, sclerotization, setae, lobes, or other features (string or null),
    "count": number of plates mentioned for this segment or group, if explicitly stated (string or null).

Notes:
- Plate numbers are not the same as segment numbers. "Plate 5 on segment 3" means plate number 5 is located on segment 3.
- If multiple segments are described together (e.g. plates I–VI), return one entry covering the group.
- Do not split paired (left/right) plates into separate entries unless the text describes them distinctly.
- Preserve the original numbering style (Roman or Arabic) as it appears in the source text.
- Distinguish plate numbers from counts: "Plate 1 with 4 setae" means plate number 1 has 4 setae, not 4 plates.
- When a plate has no explicit segment number, leave segment as null and include identifying details in description.

Return a JSON array of objects.
