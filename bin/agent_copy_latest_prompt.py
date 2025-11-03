#!/usr/bin/env python3
import sys
import subprocess
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from tools.fs_bus import latest_inbox_message, read_json
from tools.agent_registry import slug_for

if len(sys.argv) < 3 or sys.argv[1] != "--agent":
    print("Usage: agent_copy_latest_prompt.py --agent 'Name'", file=sys.stderr)
    sys.exit(1)

agent_name = sys.argv[2]
slug = slug_for(agent_name)
msg_path = latest_inbox_message(slug)
if not msg_path:
    print("NO_PROMPT")
    sys.exit(0)

msg = read_json(msg_path)
content = msg.get("content", "")
# copy to clipboard (macOS pbcopy)
try:
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    p.communicate(input=content.encode("utf-8"))
    print(f"COPIED:{msg.get('id')}")
except Exception as e:
    print(content)
    print(f"WARN: pbcopy failed: {e}", file=sys.stderr)

# also persist last_prompt_id.txt so agent_save_response can auto-pick it
last_id_file = BASE / "bus" / "agents" / slug / "last_prompt_id.txt"
last_id_file.parent.mkdir(parents=True, exist_ok=True)
last_id_file.write_text(str(msg.get('id')))
