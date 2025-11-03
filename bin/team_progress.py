#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from tools.agent_registry import load_agents
from tools.progress import load_progress

agents = load_agents()
progress = load_progress()

rows = []
# orchestrator first
rows.append((agents["orchestrator"]["name"], agents["orchestrator"]["slug"], progress.get(agents["orchestrator"]["slug"], 0)))
for a in agents.get("agents", []):
    rows.append((a["name"], a["slug"], progress.get(a["slug"], 0)))

print("TEAM PROGRESS\n==============\n")
for name, slug, val in rows:
    bar_len = int(val / 5)  # 20 chars max
    bar = "#" * bar_len + "." * (20 - bar_len)
    print(f"{name:24s} {val:3d}% [{bar}]  ({slug})")
