Find the locations on the host animal's body where the louse species lives, feeds, or
deposits its eggs (nit sites). This is the body part or region of the host mammal, not
the geographic location (handled by the geographic_locations prompt) and not the
louse's own anatomy.

Host locations describe infestation sites, oviposition sites, or general body regions.
In lice taxonomy these are often stated in the introduction, host-parasite relationship
sections, or remarks, and may be phrased as:
  "found on the head and neck region"
  "collected from the pelage"
  "infesting the dorsal body surface"
  "attached to hair near the ears"
  "eggs glued to fur along the ventral midline"

For each location found, return an object with these exact fields:
    "species": louse species name inferred from the surrounding context (string or null),
    "host_species": the host animal species name, if mentioned (string or null),
    "host_location": where on the host's body the lice or eggs are found, captured verbatim (string or null),
    "context": brief description of how the location is described, e.g. "infestation site",
      "oviposition site", "general distribution on host" (string or null).

Notes:
- Preserve the location description exactly as written in the source text.
- If multiple distinct body regions are listed in one phrase, return one entry per
  region. For example, "head and neck" yields two entries: "head" and "neck".
- Oviposition sites (where eggs/nits are glued or deposited) are a type of host
  location. Extract them the same way, setting context to "oviposition site".
- Do not confuse host body locations with geographic locations (e.g. "Queensland,
  Australia", "Mongolia").
- Do not extract louse anatomy descriptions (e.g. "dorsal view of abdomen",
  "ventral surface of sternite 3") as host locations.
- Do not extract general statements like "permanent parasite of mammals" or
  "obligate ectoparasite" — these describe the relationship, not a body location.
- When the text says "collected from the pelage" or "found in the fur", extract
  "pelage" or "fur" as the host location.

Return a JSON array of objects.
