import json

def load_config():
    with open("./configs/config.json", "r", encoding="utf-8") as f:
        return json.load(f)
