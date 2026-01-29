import os
import json
import platform

CONFIG_FILE = "apps_config.json"

def load_apps():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "notepad": "notepad.exe" if platform.system() == "Windows" else "TextEdit",
        "calculator": "calc.exe" if platform.system() == "Windows" else "Calculator"
    }

def save_apps(apps):
    with open(CONFIG_FILE, "w") as f:
        json.dump(apps, f, indent=4)