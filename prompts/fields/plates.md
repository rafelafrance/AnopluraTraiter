Find all plates.
When the ID is missing use the description instead of the ID.
For each plate count found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region of the plate (string or null),
    "number": the plate's number is a Roman numeral (string or null),
    "name": plate's name (string or null),
    "description": a description of the plate (string or null),
    "count": how many plates are on the segment (string or null),
Return a JSON array of objects.
