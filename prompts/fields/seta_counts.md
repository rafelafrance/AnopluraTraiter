Find all setae counts on all body parts.
Also note if setae are missing.
For each seta count type found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "body_region": body region where the seta is located (string or null),
    "segment": segment number or description (string or null),
    "seta_name": name of the seta type (string or null),
    "description": a description of the seta (string or null),
    "count": how many setae are there number or range (string or null),
    "side": which side of the body (string or null),
    "rows": row position of the seta (string or null).
Return a JSON array of objects.
