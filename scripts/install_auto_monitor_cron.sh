#!/bin/bash
# Install automatic monitoring as a cron job
# This ensures the system monitors itself WITHOUT human intervention

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/auto_detect_changes_and_assign.py"
LOG_FILE="$PROJECT_ROOT/logs/auto_monitor.log"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Cron job entry (runs every 4 hours)
CRON_ENTRY="0 */4 * * * cd $PROJECT_ROOT && /usr/bin/python3 $PYTHON_SCRIPT >> $LOG_FILE 2>&1"

echo "Installing automatic change monitoring..."
echo ""
echo "This will add a cron job that runs every 4 hours to:"
echo "  1. Detect changes in code, processes, docs"
echo "  2. Automatically generate Helena tasks"
echo "  3. Ensure zero knowledge drift"
echo ""
echo "Cron entry:"
echo "$CRON_ENTRY"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "auto_detect_changes_and_assign.py"; then
    echo "⚠️  Cron job already exists!"
    echo ""
    read -p "Replace it? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove old entry
        crontab -l | grep -v "auto_detect_changes_and_assign.py" | crontab -
        echo "✅ Removed old cron job"
    else
        echo "❌ Cancelled"
        exit 1
    fi
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo ""
echo "✅ Automatic monitoring installed!"
echo ""
echo "The system will now:"
echo "  ✅ Monitor changes every 4 hours automatically"
echo "  ✅ Generate Helena tasks without human intervention"
echo "  ✅ Log to: $LOG_FILE"
echo ""
echo "To verify:"
echo "  crontab -l"
echo ""
echo "To test manually:"
echo "  python3 $PYTHON_SCRIPT"
echo ""
echo "To view logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "🎯 SELF-ENFORCING SYSTEM: ACTIVE ✅"
