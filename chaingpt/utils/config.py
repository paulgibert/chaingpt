# Standard lib
from typing import Dict

# 3rd party
import yaml


# TODO: Add checks to config to ensure expected fields are present
CONFIG_FILE_NAME = "config.yaml"


def _load_config() -> Dict:
    """
    Searches for a file called config.yaml in the current working
    directory and loads its contents.
    """
    with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = _load_config()