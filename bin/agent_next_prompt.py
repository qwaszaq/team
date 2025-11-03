#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from tools.fs_bus import latest_inbox_message, read_json
from tools.agent_registry import slug_for

parser = argparse.ArgumentParser(description="Show latest PROMPT for an agent")
parser.add_argument("--agent", required=True, help="Agent name")
args = parser.parse_args()

slug = slug_for(args.agent)
path = latest_inbox_message(slug)
if not path:
    print("NO_PROMPT")
else:
    data = read_json(path)
    print(path)
    print(f"PROMPT_ID: {data.get('id')}")
    print("---")
    print(data.get("content", ""))
    # store last prompt id for convenience
    from pathlib import Path as _P
    last_id_file = _P(__file__).resolve().parents[1] / "bus" / "agents" / slug / "last_prompt_id.txt"
    last_id_file.write_text(str(data.get('id')))
