Find all head width measurements.
For each head width found, return an object with these exact fields:
    "species": species name (string or null),
    "sex": sex of the specimen (string or null),
    "width": single measurement value if given (number or null),
    "mean_width": mean head width if stated (number or null),
    "width_low": lower bound of range (number or null),
    "width_high": upper bound of range (number or null),
    "n": sample size (number or null),
    "units": unit of measurement (string or null).
Return a JSON array of objects.
