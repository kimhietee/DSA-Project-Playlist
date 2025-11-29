import json
import os
from pprint import pprint



def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("[]")
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


filepath = 'library.json'
x = load_data(filepath)

pprint(x)


