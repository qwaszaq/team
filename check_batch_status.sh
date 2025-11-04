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
