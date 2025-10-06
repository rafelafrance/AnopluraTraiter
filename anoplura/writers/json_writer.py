import json
from dataclasses import asdict
from pathlib import Path

from spacy.tokens import Doc


def writer(doc: Doc, json_file: Path) -> None:
    json_doc = {"path": "", "text": doc.text, "traits": []}
    traits = [e._.trait for e in doc.ents]

    for trait in traits:
        obj = {
            k.removeprefix("_"): v for k, v in asdict(trait).items() if v is not None
        }
        if "dims" in obj:
            obj["dims"] = [
                {k: v for k, v in d.items() if v is not None} for d in obj["dims"]
            ]

        json_doc["traits"].append(obj)

    with json_file.open("w") as f:
        json.dump(json_doc, f, indent=4)
