#!/bin/bash
# Helper script to queue files for batch processing

if [ $# -eq 0 ]; then
    echo "Usage: ./queue_for_batch.sh <file_path>"
    exit 1
fi

python3 hourly_batch_processor.py --queue "$1"
