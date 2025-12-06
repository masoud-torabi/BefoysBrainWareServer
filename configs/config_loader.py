import os
import json

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")

    with open("./configs/config.json", "r", encoding="utf-8") as f:
        return json.load(f)
