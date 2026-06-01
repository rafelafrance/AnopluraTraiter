Find the geographic locations where the host animals (and their lice) were collected.
This is the place on Earth where the specimens were obtained, not the body part on the host
(that is handled by the host_locations prompt).

Locations are typically given as specific sites, towns, provinces, states, or countries,
often with coordinates. Examples:
  "May Downs Station, Mount Isa, Queensland, Australia (20°39'S, 139°23'E)"
  "Colloń Curań, Neuqueń Province, Argentina"
  "Arkhangai Province, Zurkh Mountain, Mongolia"

For each location found, return an object with these exact fields:
    "species": species name (string),
    "sex": sex of the specimen (string or null),
    "geographic_location": the full location as stated in the text (string or null).

Notes:
- Preserve the location exactly as written in the source text. Do not normalize, reorder, or abbreviate.
- If multiple locations are listed for a species, return one entry per location.
- Coordinates in parentheses are part of the location and should be included.
- Do not output MathML, no <math></math>, no {\circ}, nor \\text{S} nor other similar markup.
- Only output UTF-8 characters.
- Do not extract institutional names, museum codes, or collection numbers as locations.
- Do not confuse geographic locations with host body-part locations (e.g. "skin surface and fur").

Return a JSON array of objects.
