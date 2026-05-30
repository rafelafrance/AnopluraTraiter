Find all tergites.
Also note if tergites are missing.
Report the tergite even if its segment is not mentioned.
DO NOT confuse setae counts for a tergite number.
For each tergite count found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region of the tergite (string or null),
    "missing": are tergites missing from the body region (true or null),
    "segment": the tergite is on this segment (string or null),
    "number": the tergite's number (string or null),
    "name": the tergite's name (string or null),
    "description": a description of the tergite (string or null),
    "count": how many tergites are on the segment (string or null),
Return a JSON array of objects.
