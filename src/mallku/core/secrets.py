import json
import os
from pathlib import Path

DEFAULT_SECRET_PATH = Path(os.environ.get("INDALEKO_SECRETS_PATH", "./.secrets/mallku-secrets.json"))

def load_secrets(path: Path = DEFAULT_SECRET_PATH) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_secrets(secrets: dict, path: Path = DEFAULT_SECRET_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(secrets, f, indent=2)

def get_secret(key: str, fallback: str | None = None, path: Path = DEFAULT_SECRET_PATH) -> str | None:
    return os.environ.get(key.upper(), load_secrets(path).get(key, fallback))
