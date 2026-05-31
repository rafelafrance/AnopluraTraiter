Find all counts of named setae (bristles/hairs) described on any body part.
Setae have standardized names that are typically spelled out on first mention
with a parenthetical abbreviation, then abbreviated thereafter.
Common abbreviations include:
  Head: DPHS, DAcHS, DMHS, SuHS, ApHS, VPHS, VPaHS, SpAtHS, DPaHS, DPoCHS, AnMHS
  Thorax: DPTS
  Abdomen: DCAS, DMAS, VCAS, VMAS, DLAS, VLAS, StAS, TeAS, PrS
  Plates: PrS (paratergal setae)

For each seta count found, return an object with these exact fields:
    "species": species name (string),
    "sex": sex of the specimen (string or null),
    "body_region": body region where the seta is located, e.g. head, thorax, abdomen, paratergal plate, subgenital plate (string or null),
    "segment": segment number or description where the seta is found (string or null),
    "seta_name": the seta's name or abbreviation as given in the text, e.g. "dorsal principal head seta (DPHS)", "DCAS", "StAS" (string or null),
    "count": number of setae or range, e.g. "1", "4–6", "2–3" (string or null),
    "side": which side of the body, e.g. "each side", "left", "right", "both sides" (string or null),
    "rows": row position or row count of the seta, if described in terms of rows (string or null),
    "description": additional morphological description including length, shape, thickness, or other features (string or null).

Notes:
- Seta names appear as full names on first mention (e.g. "dorsal principal head seta (DPHS)") and as abbreviations thereafter (e.g. "DPHS"). Extract whichever form the text uses.
- "On each side" means the count applies per side, not total. Capture "each side" in the side field.
- When setae are described in rows (e.g. "8 rows of 5–8 DCAS"), capture row information in the rows field and per-row counts in count.
- Do not confuse seta counts with sternite or tergite numbers.
- If setae are explicitly absent or missing on a body part, still record the entry with count as "0" or missing as noted in description.
- If the seta name is missing you may use terms like paratergal plates, subgenital plates, or gonopods to identify the seta types.

Return a JSON array of objects.
