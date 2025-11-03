#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: auto_handshake_ack.sh '<Agent Name>' '<Role Label>'" >&2
  exit 1
fi
AGENT="$1"
ROLE="$2"
BASE="/Users/artur/coursor-agents-destiny-folder"
# Use last_prompt_id.txt automatically
echo "READY - ${ROLE}" | "$BASE/bin/agent_save_response.py" --agent "$AGENT"