#!/bin/bash
# Setup Hourly Batch Processing

echo "🕐 Setting Up Hourly Batch Processing"
echo "====================================="
echo ""

# Create required directories
mkdir -p batch_queue
mkdir -p batch_processed
mkdir -p logs

# Create systemd service (for Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > hourly_batch.service << 'EOF'
[Unit]
Description=Hourly Batch Processor for PostgreSQL
After=postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/Users/artur/coursor-agents-destiny-folder
ExecStart=/usr/bin/python3 /Users/artur/coursor-agents-destiny-folder/hourly_batch_processor.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF
    echo "✅ Created systemd service file"
fi

# Create launchd plist (for macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    cat > com.destiny.hourly-batch.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.destiny.hourly-batch</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/artur/coursor-agents-destiny-folder/hourly_batch_processor.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/artur/coursor-agents-destiny-folder</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardErrorPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/hourly_batch_error.log</string>
    
    <key>StandardOutPath</key>
    <string>/Users/artur/coursor-agents-destiny-folder/logs/hourly_batch_output.log</string>
</dict>
</plist>
EOF
    echo "✅ Created launchd plist file"
    echo ""
    echo "To install as a service on macOS:"
    echo "  cp com.destiny.hourly-batch.plist ~/Library/LaunchAgents/"
    echo "  launchctl load ~/Library/LaunchAgents/com.destiny.hourly-batch.plist"
fi

# Create cron entry option
echo ""
echo "Alternative: Add to crontab for hourly execution:"
echo "0 * * * * cd /Users/artur/coursor-agents-destiny-folder && /usr/bin/python3 hourly_batch_processor.py --run-once >> logs/hourly_batch_cron.log 2>&1"
echo ""

# Create queue helper script
cat > queue_for_batch.sh << 'EOF'
#!/bin/bash
# Helper script to queue files for batch processing

if [ $# -eq 0 ]; then
    echo "Usage: ./queue_for_batch.sh <file_path>"
    exit 1
fi

python3 hourly_batch_processor.py --queue "$1"
EOF

chmod +x queue_for_batch.sh
echo "✅ Created queue helper script: ./queue_for_batch.sh"
echo ""

# Create status check script
cat > check_batch_status.sh << 'EOF'
#!/bin/bash
# Check batch processor status

echo "🕐 Batch Processor Status"
echo "========================"
echo ""

# Check if running
if pgrep -f "hourly_batch_processor.py" > /dev/null; then
    echo "✅ Processor is RUNNING"
    echo "   PID: $(pgrep -f hourly_batch_processor.py)"
else
    echo "❌ Processor is NOT RUNNING"
fi

echo ""

# Show queue status
python3 hourly_batch_processor.py --status

echo ""

# Show recent logs
if [ -f logs/hourly_batch.log ]; then
    echo "Recent log entries:"
    echo "-------------------"
    tail -10 logs/hourly_batch.log
fi
EOF

chmod +x check_batch_status.sh
echo "✅ Created status check script: ./check_batch_status.sh"
echo ""

# Test the processor
echo "Testing hourly batch processor..."
python3 hourly_batch_processor.py --run-once

echo ""
echo "✅ Setup complete!"
echo ""
echo "Quick Start Commands:"
echo "--------------------"
echo "1. Start processor:     python3 hourly_batch_processor.py"
echo "2. Queue a file:        ./queue_for_batch.sh <file>"
echo "3. Check status:        ./check_batch_status.sh"
echo "4. Run once manually:   python3 hourly_batch_processor.py --run-once"
echo ""
echo "The processor will:"
echo "- Run every hour at :00"
echo "- Process all queued files in a single transaction"
echo "- Keep logs for 7 days"
echo "- Handle errors gracefully"
echo ""