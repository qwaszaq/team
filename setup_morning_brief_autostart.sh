#!/bin/bash
###############################################################################
# Setup Morning Brief Agent - Auto-start on System Boot
###############################################################################

echo "========================================================================"
echo "         🌅 Setting up Morning Brief Agent Auto-start"
echo "========================================================================"
echo ""

PROJECT_DIR="/Users/artur/coursor-agents-destiny-folder"
PLIST_SOURCE="$PROJECT_DIR/com.destiny.morningbrief.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.destiny.morningbrief.plist"

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"

# Make scripts executable
chmod +x "$PROJECT_DIR/scripts/morning_brief_for_aleksander.py"
chmod +x "$PROJECT_DIR/scripts/morning_brief.py"

echo "✅ Scripts made executable"

# Check if LaunchAgents directory exists
mkdir -p "$HOME/Library/LaunchAgents"

# Copy plist if it doesn't exist in LaunchAgents
if [ ! -f "$PLIST_DEST" ]; then
    # Create the plist file
    cat > "$PLIST_DEST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.destiny.morningbrief</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/artur/coursor-agents-destiny-folder/scripts/morning_brief_for_aleksander.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StartInterval</key>
    <integer>28800</integer>
    
    <key>StandardOutPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/morning_brief.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/morning_brief_error.log</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/artur/coursor-agents-destiny-folder</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF
    
    echo "✅ Created LaunchAgent plist"
else
    echo "ℹ️  LaunchAgent plist already exists"
fi

# Unload if already loaded (to refresh)
launchctl unload "$PLIST_DEST" 2>/dev/null

# Load the LaunchAgent
launchctl load "$PLIST_DEST"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent loaded successfully"
else
    echo "⚠️  Warning: Could not load LaunchAgent"
fi

echo ""
echo "========================================================================"
echo "✅ Morning Brief Agent Auto-start Setup Complete!"
echo "========================================================================"
echo ""
echo "📋 Configuration:"
echo "   • Runs at system boot (login)"
echo "   • Runs every 8 hours (28800 seconds)"
echo "   • Logs to: logs/morning_brief.log"
echo ""
echo "🧪 Test it now:"
echo "   python3 scripts/morning_brief_for_aleksander.py"
echo ""
echo "📊 View logs:"
echo "   tail -f logs/morning_brief.log"
echo ""
echo "🔧 Manage LaunchAgent:"
echo "   launchctl list | grep destiny        # Check if running"
echo "   launchctl stop com.destiny.morningbrief   # Stop"
echo "   launchctl start com.destiny.morningbrief  # Start"
echo "   launchctl unload $PLIST_DEST    # Disable"
echo "   launchctl load $PLIST_DEST      # Enable"
echo ""
echo "========================================================================"
