#!/bin/bash
###############################################################################
# Start Real-Time Helena Document Processor
###############################################################################
#
# This script starts the file watcher that automatically processes .md files
# the MOMENT you save them. No delays. No manual steps. Just save and done.
#
# Usage: ./start_realtime_helena.sh
#

echo "========================================================================"
echo "         🚀 Starting Real-Time Helena Document Processor"
echo "========================================================================"
echo ""

# Project directory
PROJECT_DIR="/Users/artur/coursor-agents-destiny-folder"
cd "$PROJECT_DIR" || exit 1

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install watchdog if needed (will skip if already installed)
echo ""
echo "📦 Checking dependencies..."
python3 -c "import watchdog" 2>/dev/null || {
    echo "📦 Installing watchdog..."
    pip3 install watchdog
}

echo "✅ Dependencies ready"
echo ""

# Make scripts executable
chmod +x scripts/realtime_md_watcher.py
chmod +x scripts/helena_realtime_processor.py

# Start the watcher
echo "🚀 Starting real-time watcher..."
echo ""
echo "📝 From now on, every time you SAVE a .md file:"
echo "   1. System detects it instantly"
echo "   2. Helena processes it automatically"
echo "   3. Content added to databases"
echo "   4. Done in ~5-10 seconds"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the watcher
python3 scripts/realtime_md_watcher.py
