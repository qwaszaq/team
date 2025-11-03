import json
from pathlib import Path
from typing import Dict

BASE = Path(__file__).resolve().parents[1]
PROGRESS_DIR = BASE / "progress"
PROGRESS_FILE = PROGRESS_DIR / "agents.json"


def _ensure_file() -> None:
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    if not PROGRESS_FILE.exists():
        # initialize zeros for all agents
        from tools.agent_registry import load_agents
        data = load_agents()
        progress: Dict[str, int] = {}
        progress[data["orchestrator"]["slug"]] = 0
        for a in data.get("agents", []):
            progress[a["slug"]] = 0
        PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2))


essential_delta = 5  # default increment per response


def load_progress() -> Dict[str, int]:
    _ensure_file()
    return json.loads(PROGRESS_FILE.read_text())


def save_progress(p: Dict[str, int]) -> None:
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2))


def bump(agent_slug: str, delta: int = essential_delta) -> int:
    p = load_progress()
    current = int(p.get(agent_slug, 0))
    new_val = max(0, min(100, current + delta))
    p[agent_slug] = new_val
    save_progress(p)
    return new_val


def set_value(agent_slug: str, value: int) -> int:
    val = max(0, min(100, int(value)))
    p = load_progress()
    p[agent_slug] = val
    save_progress(p)
    return val
