import os, json, sys

def get_app_dir():
    if getattr(sys, "frozen", False):
        # running as .exe
        app_dir = os.path.dirname(sys.executable)
    else:
        # running from source
        app_dir = os.path.dirname(os.path.abspath(__file__))
    return app_dir

def load_config():
    app_dir = get_app_dir()
    config_path = os.path.join(app_dir, "config", "config.json")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("⚠️ Config file not found, using defaults.")
        return {"API_BASE_URL": "https://api.petmateanimalclinic.com"}

# Load once and export the variable
CONFIG = load_config()
API_BASE_URL = CONFIG["API_BASE_URL"]
