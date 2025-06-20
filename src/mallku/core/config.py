import os
from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path(os.environ.get("INDALEKO_CONFIG", "./config/default.yaml"))


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")
    with open(path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return {**config, **os.environ}  # simple override layer
