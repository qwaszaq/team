import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

BASE = Path(__file__).resolve().parents[1]
BUS = BASE / "bus"


def _atomic_write(path: Path, data: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)
    return path


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def write_prompt(to_slug: str, payload: Dict[str, Any]) -> Path:
    """Write a PROMPT message to agent's inbox. Returns message path."""
    msg_id = str(uuid.uuid4())
    message = {
        "id": msg_id,
        "from": "Aleksander Nowak",
        "to": to_slug,
        "type": "PROMPT",
        "content": payload.get("content", ""),
        "context": payload.get("context", {}),
        "created_at": now_iso()
    }
    inbox = BUS / "agents" / to_slug / "inbox"
    path = inbox / f"{msg_id}.json"
    return _atomic_write(path, message)


def write_response(from_slug: str, response_to_id: str, content: str, context: Optional[Dict[str, Any]] = None) -> Path:
    """Write a RESPONSE message to agent's outbox."""
    msg_id = str(uuid.uuid4())
    message = {
        "id": msg_id,
        "from": from_slug,
        "to": "orchestrator",
        "type": "RESPONSE",
        "response_to": response_to_id,
        "content": content,
        "context": context or {},
        "created_at": now_iso()
    }
    outbox = BUS / "agents" / from_slug / "outbox"
    path = outbox / f"{msg_id}.json"
    return _atomic_write(path, message)


def latest_inbox_message(agent_slug: str) -> Optional[Path]:
    inbox = BUS / "agents" / agent_slug / "inbox"
    if not inbox.exists():
        return None
    msgs = sorted(inbox.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return msgs[0] if msgs else None


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def orchestrator_outbox_write(payload: Dict[str, Any]) -> Path:
    outbox = BUS / "orchestrator" / "outbox"
    msg_id = payload.get("id") or str(uuid.uuid4())
    payload.setdefault("created_at", now_iso())
    path = outbox / f"{msg_id}.json"
    return _atomic_write(path, payload)
