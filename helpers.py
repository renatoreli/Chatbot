import json
from typing import List

class Intent:
    tag: str
    patterns: List[str]
    responses: List[str]
    context: List[str]

def load_intents() -> List[Intent]:
    with open("data/intents.json", "r", encoding="utf-8") as f:
        intents_json = json.load(f)

    intents: List[Intent] = []

    for intent_dict in intents_json["intents"]:
        intent = Intent()
        intent.tag = intent_dict["tag"]
        intent.patterns = intent_dict["patterns"]
        intent.responses = intent_dict["responses"]
        intent.context = intent_dict["context"]

        intents.append(intent)

    return intents