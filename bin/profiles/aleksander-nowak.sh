# source this in the Orchestrator tab
export AGENT_NAME="Aleksander Nowak"
base="/Users/artur/coursor-agents-destiny-folder"
np(){ echo "(orchestrator has no inbox)"; }
ar(){ echo "(orchestrator does not reply via agent_save_response)"; }
who(){ echo "$AGENT_NAME"; }
status(){ "$base/bin/bus_status.py"; }
