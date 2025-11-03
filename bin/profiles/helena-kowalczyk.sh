# source this in the Knowledge Manager tab
export AGENT_NAME="Dr. Helena Kowalczyk"
base="/Users/artur/coursor-agents-destiny-folder"
np(){ "$base/bin/agent_next_prompt.py" --agent "$AGENT_NAME"; }
ar(){ pbpaste | "$base/bin/agent_save_response.py" --agent "$AGENT_NAME"; }
arx(){ "$base/bin/agent_save_response.py" --agent "$AGENT_NAME" --in-reply-to "$1" --content "$2"; }
who(){ echo "$AGENT_NAME"; }
status(){ "$base/bin/bus_status.py"; }
