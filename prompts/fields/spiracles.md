Find all mentions of spiracles (respiratory openings) in the text.
Spiracles are typically described by their location, presence/absence, size, or other morphological features.
The most commonly described spiracle is the mesothoracic spiracle on the thorax.
Abdominal spiracles are often associated with paratergal plates on specific abdominal segments.

For each spiracle or spiracle group found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region where the spiracle is located, e.g. mesothorax, abdomen, paratergal plate (string or null),
    "segment": abdominal segment number(s) where the spiracle is found, if applicable (string or null),
    "count": number of spiracles described, e.g. "6 pairs", "on segments 3–8" (string or null),
    "missing": true if spiracles are explicitly absent or lacking in the region or segment (true or null),
    "description": morphological description including size, shape, annulation, or other features (string or null).

Notes:
- Mesothoracic spiracles are on the thorax. Abdominal spiracles are on abdominal segments, often associated with paratergal plates.
- When spiracles are described as being on paratergal plates (e.g. "plates III–VII each with spiracle"), set body_region to "paratergal plate" and segment to the plate segment(s).
- If spiracle diameter measurements are given, include them in the description field. The spiracle_diameters prompt handles precise numeric extraction separately.
- "Annulated" refers to spiracles with ring-like structures around the opening.
- Do not confuse spiracle counts with spiracle diameter measurements.

Return a JSON array of objects.
