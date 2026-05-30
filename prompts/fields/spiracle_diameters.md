Find all mesothoracic spiracle diameter measurements.
For each measurement found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "diameter": single measurement value if given (number or null),
    "mean_diameter": mean diameter if stated (number or null),
    "diameter_low": lower bound of range (number or null),
    "diameter_high": upper bound of range (number or null),
    "n": sample size (number or null),
    "units": unit of measurement (string or null).
Return a JSON array of objects.
