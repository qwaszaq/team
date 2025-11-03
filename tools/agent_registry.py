import json
from pathlib import Path
from typing import Dict, List

BASE = Path(__file__).resolve().parents[1]
AGENTS_FILE = BASE / "agents.json"


def load_agents() -> Dict:
    return json.loads(AGENTS_FILE.read_text())


def slug_for(name: str) -> str:
    data = load_agents()
    if data.get("orchestrator", {}).get("name") == name:
        return data["orchestrator"]["slug"]
    for a in data.get("agents", []):
        if a["name"] == name:
            return a["slug"]
    raise KeyError(f"Unknown agent name: {name}")


def name_for_slug(slug: str) -> str:
    data = load_agents()
    if data.get("orchestrator", {}).get("slug") == slug:
        return data["orchestrator"]["name"]
    for a in data.get("agents", []):
        if a["slug"] == slug:
            return a["name"]
    raise KeyError(f"Unknown agent slug: {slug}")
