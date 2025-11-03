#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from tools.fs_bus import write_prompt
from tools.agent_registry import slug_for

parser = argparse.ArgumentParser(description="Write a PROMPT to an agent inbox")
parser.add_argument("--to", required=True, help="Agent name (e.g., 'Katarzyna Wiśniewska')")
parser.add_argument("--content", required=True, help="Prompt content")
parser.add_argument("--context", default="{}", help="JSON context dict")
args = parser.parse_args()

slug = slug_for(args.to)
ctx = json.loads(args.context)
path = write_prompt(slug, {"content": args.content, "context": ctx})
print(str(path))
