#!/usr/bin/env python3
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BUS = BASE / "bus"

AGENTS = [p.name for p in (BUS / "agents").iterdir() if p.is_dir()]

def count(pattern):
    return len(list(pattern.glob("*.json")))

print("BUS STATUS\n========\n")
print(f"Orchestrator outbox: {count(BUS / 'orchestrator' / 'outbox')} items")
print()
for slug in sorted(AGENTS):
    inbox = count(BUS / 'agents' / slug / 'inbox')
    outbox = count(BUS / 'agents' / slug / 'outbox')
    print(f"{slug:24s} | inbox: {inbox:3d} | outbox: {outbox:3d}")
