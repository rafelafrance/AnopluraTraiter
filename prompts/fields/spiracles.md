Find all spiracle counts on all body parts.
For each spiracle found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region of the spiracle (string or null),
    "number": spiracle number or identifier (string or null),
    "description": a description of the spiracles (string or null),
    "name": spiricle's name (string or null),
    "missing": are spiracles missing from the body region (true or null),
    "count": how many spiracles are on the body region (string or null),
Return a JSON array of objects.
