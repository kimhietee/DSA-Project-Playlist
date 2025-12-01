import json
import os

def load_data(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            if "playlist" in file.lower() or "queue" in file.lower():
                f.write("{}")
            else:
                f.write("[]")

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "playlist" in file.lower() and isinstance(data, list):
            return {}
        return data

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

