Find all mentions of anatomical plates described in the text.
Plates commonly include paratergal plates, subgenital plates, thoracic sternal plates, and ventral genital plates.

For each distinct plate or plate group found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "plate_type": the kind of plate, e.g. paratergal plate, subgenital plate, thoracic sternal plate (string or null),
    "segment_number": segment identifier as given in the text, preserving Roman or Arabic numerals (string or null),
    "body_region": body region where the plate is located, e.g. thorax, abdomen, genitalia (string or null),
    "description": morphological description of the plate including shape, sclerotization, setae, lobes, or other features (string or null),
    "count": number of plates mentioned for this segment or group, if explicitly stated (string or null).

Notes:
- If multiple segments are described together (e.g. plates I–VI), return one entry covering the group.
- Do not split paired (left/right) plates into separate entries unless the text describes them distinctly.
- Preserve the original numbering style (Roman or Arabic) as it appears in the source text.
- When a plate has no explicit segment number, leave segment_number as null and include identifying details in description.

Return a JSON array of objects.
