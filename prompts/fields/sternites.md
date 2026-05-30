Find all sternites.
Also note if sternites are missing.
Report the sternite even if a segment is not mentioned.
DO NOT confuse setae counts for a sternite number.
For each sternite count found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region of the sternite (string or null),
    "missing": are sternites missing from the body region (true or null),
    "segment": segment number or name (string or null),
    "number": sternite's number (string or null),
    "name": sternite's name (string or null),
    "description": a description of the sternite (string or null),
    "count": how many sternites are on the segment (string or null).
Return a JSON array of objects.
