import json
import os

DB_FILE = "stages.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return [] # Begin met een lege lijst als er nog geen bestand is
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)
