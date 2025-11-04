#!/bin/bash
# Start Real-Time Watcher with Conda Team Environment
# This script ensures the watcher uses the correct conda env

cd /Users/artur/coursor-agents-destiny-folder

# Kill any existing watcher
pkill -f realtime_md_watcher

# Start watcher with conda team environment
nohup conda run -n team python scripts/realtime_md_watcher.py > logs/watcher.log 2>&1 &

WATCHER_PID=$!
echo "✅ Watcher started with conda team environment (PID: $WATCHER_PID)"
echo "📝 Log: tail -f logs/watcher.log"
