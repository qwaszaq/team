#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from tools.fs_bus import write_response
from tools.agent_registry import slug_for

parser = argparse.ArgumentParser(description="Save a RESPONSE from an agent")
parser.add_argument("--agent", required=True, help="Agent name")
parser.add_argument("--in-reply-to", help="PROMPT id to reply to (optional, auto from last_prompt_id.txt)")
parser.add_argument("--content", help="Response content (if not using stdin)")
parser.add_argument("--context", default="{}", help="JSON context dict")
args = parser.parse_args()

slug = slug_for(args.agent)
content = args.content if args.content is not None else sys.stdin.read()
ctx = json.loads(args.context)
reply_id = args.in_reply_to
if not reply_id:
    last_id_file = BASE / "bus" / "agents" / slug / "last_prompt_id.txt"
    if last_id_file.exists():
        reply_id = last_id_file.read_text().strip()
    else:
        print("ERROR: --in-reply-to not provided and no last_prompt_id.txt found", file=sys.stderr)
        sys.exit(1)

path = write_response(slug, reply_id, content, ctx)
print(str(path))
