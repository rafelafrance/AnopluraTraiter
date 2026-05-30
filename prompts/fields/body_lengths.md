Find all body length measurements.
For each body length found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "type": whether holotype or allotype (string or null),
    "length": single measurement value if given (number or null),
    "mean_length": mean body length if stated (number or null),
    "length_low": lower bound of range (number or null),
    "length_high": upper bound of range (number or null),
    "n": sample size (number or null),
    "units": unit of measurement (string or null).
Return a JSON array of objects.
