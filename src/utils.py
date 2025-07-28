# /Users/shabdpatel/Documents/adobe/Challenge_1b/src/utils.py
import json
import os
from datetime import datetime
from config import Config

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, filename="output.json"):
    output_path = os.path.join(Config.OUTPUT_PATH, filename)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def get_timestamp():
    return datetime.now().isoformat()

def get_doc_outline_path(doc_name):
    return os.path.join(Config.INPUT_PATH, f"{doc_name}.json")