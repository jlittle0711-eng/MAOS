import yaml
import os

CONFIG_FILE = "config.yaml"

def load_config():
    with open(CONFIG_FILE,"r") as f:
        return yaml.safe_load(f)

def ensure_dirs(config):
    os.makedirs(config["documents_folder"],exist_ok=True)
    os.makedirs(config["index_folder"],exist_ok=True)
