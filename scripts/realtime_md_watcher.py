#!/usr/bin/env python3
"""
Real-Time Markdown File Watcher & Helena Auto-Processor
=========================================================

Purpose: Automatically process .md files the MOMENT they are saved
Author: AI Assistant + Artur
Created: 2025-11-04

HOW IT WORKS:
1. Watches project directory for .md file changes (save, create, modify)
2. IMMEDIATELY detects when you save a .md file
3. Analyzes what changed
4. Automatically triggers Helena to process and add to databases
5. You get confirmation within seconds

NO WAITING. NO CRON. NO DELAYS. INSTANT.
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import subprocess

# Import watchdog (should be pre-installed in venv)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

# Project configuration
PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
DOCS_DIR = PROJECT_ROOT / "docs"
WATCHED_EXTENSIONS = ['.md']
IGNORE_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    'venv',
    '.venv',
    'helena_tasks',  # Don't process Helena's own task files
    'demo_',
    'test_',
    'INDEX.md',  # Don't process auto-generated index
    'MORNING_BRIEF'  # Don't process morning briefs
]


class MarkdownFileHandler(FileSystemEventHandler):
    """Handles real-time .md file changes"""
    
    def __init__(self):
        super().__init__()
        self.processing = set()  # Track files being processed to avoid duplicates
        self.last_processed = {}  # Track last processing time
        self.cooldown = 2  # seconds between processing same file
        
    def should_process(self, file_path: str) -> bool:
        """Check if file should be processed"""
        
        # Convert to Path object
        path = Path(file_path)
        
        # Must be .md file
        if path.suffix not in WATCHED_EXTENSIONS:
            return False
            
        # Must exist and be a file
        if not path.exists() or not path.is_file():
            return False
            
        # Check ignore patterns
        path_str = str(path)
        if any(pattern in path_str for pattern in IGNORE_PATTERNS):
            return False
            
        # Check if already processing
        if path_str in self.processing:
            return False
            
        # Check cooldown (avoid processing same file multiple times in quick succession)
        last_time = self.last_processed.get(path_str, 0)
        if time.time() - last_time < self.cooldown:
            return False
            
        return True
        
    def on_modified(self, event):
        """Called when a file is modified (saved)"""
        if isinstance(event, FileModifiedEvent) and not event.is_directory:
            self.handle_file_change(event.src_path, "modified")
            
    def on_created(self, event):
        """Called when a file is created"""
        if isinstance(event, FileCreatedEvent) and not event.is_directory:
            self.handle_file_change(event.src_path, "created")
            
    def handle_file_change(self, file_path: str, change_type: str):
        """Process a file change"""
        
        if not self.should_process(file_path):
            return
            
        # Mark as processing
        self.processing.add(file_path)
        self.last_processed[file_path] = time.time()
        
        try:
            # Get relative path
            rel_path = Path(file_path).relative_to(PROJECT_ROOT)
            
            print("\n" + "="*80)
            print(f"🔔 DETECTED: {rel_path} ({change_type})")
            print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
            print("="*80)
            
            # Analyze the file
            analysis = self.analyze_markdown_file(file_path)
            
            if analysis['should_propagate']:
                print(f"📊 Type: {analysis['document_type']}")
                print(f"📝 Title: {analysis['title']}")
                print(f"📏 Size: {analysis['size_kb']:.1f} KB")
                print("\n🤖 TRIGGERING HELENA AUTO-PROCESSING...")
                
                # Process immediately
                self.trigger_helena_processing(file_path, analysis)
            else:
                print("ℹ️  Not significant enough for database propagation")
                print("   (Small file or test/demo content)")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Remove from processing set
            if file_path in self.processing:
                self.processing.remove(file_path)
                
    def analyze_markdown_file(self, file_path: str) -> Dict:
        """Analyze markdown file to determine if it needs propagation"""
        
        path = Path(file_path)
        
        try:
            content = path.read_text(encoding='utf-8')
        except:
            content = ""
            
        # Extract title (first h1)
        title = "Untitled"
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
                
        # Determine document type
        doc_type = self.classify_document(path.name, content)
        
        # Determine if should propagate
        size_kb = len(content.encode('utf-8')) / 1024
        should_propagate = (
            size_kb > 0.2 and  # At least 200 bytes (changed from 1KB - more permissive)
            doc_type != 'unknown' and
            not any(x in path.name.lower() for x in ['test', 'demo', 'example'])  # Still ignore test files
        )
        
        return {
            'title': title,
            'document_type': doc_type,
            'size_kb': size_kb,
            'line_count': len(content.split('\n')),
            'should_propagate': should_propagate,
            'content_preview': content[:500]
        }
        
    def classify_document(self, filename: str, content: str) -> str:
        """Classify what type of document this is"""
        
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Check filename patterns
        if 'protocol' in filename_lower or 'process' in filename_lower:
            return 'protocol'
        elif 'guide' in filename_lower or 'tutorial' in filename_lower:
            return 'guide'
        elif 'team' in filename_lower or 'agent' in filename_lower:
            return 'team_documentation'
        elif 'analysis' in filename_lower or 'report' in filename_lower:
            return 'analysis'
        elif 'status' in filename_lower or 'summary' in filename_lower:
            return 'status_report'
        elif 'architecture' in filename_lower or 'design' in filename_lower:
            return 'architecture'
        elif 'api' in filename_lower:
            return 'api_documentation'
        
        # Check content patterns
        if 'protocol' in content_lower and 'procedure' in content_lower:
            return 'protocol'
        elif 'agent' in content_lower and ('responsibility' in content_lower or 'role' in content_lower):
            return 'team_documentation'
        elif 'architecture' in content_lower or 'system design' in content_lower:
            return 'architecture'
            
        return 'general_documentation'
        
    def trigger_helena_processing(self, file_path: str, analysis: Dict):
        """Trigger Helena to immediately process this file"""
        
        rel_path = Path(file_path).relative_to(PROJECT_ROOT)
        
        # Create immediate processing request for Helena
        task_data = {
            'file_path': str(rel_path),
            'document_type': analysis['document_type'],
            'title': analysis['title'],
            'detected_at': datetime.now().isoformat(),
            'processing_mode': 'realtime',
            'priority': 'immediate',
            'content_preview': analysis['content_preview']
        }
        
        # Save to Helena's processing queue
        queue_dir = PROJECT_ROOT / "helena_tasks" / "realtime_queue"
        queue_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        queue_file = queue_dir / f"realtime_{timestamp}_{Path(file_path).stem}.json"
        
        with open(queue_file, 'w') as f:
            json.dump(task_data, f, indent=2)
            
        print(f"✅ Queued for Helena: {queue_file.name}")
        
        # Try to trigger Helena immediately
        self.call_helena_processor(queue_file, task_data)
        
    def call_helena_processor(self, queue_file: Path, task_data: Dict):
        """Call Helena's real-time processor"""
        
        print("\n📞 Calling Helena's processor...")
        
        # Check if helena_realtime_processor exists (use SIMPLE version!)
        processor_script = PROJECT_ROOT / "scripts" / "helena_realtime_processor_simple.py"
        
        if processor_script.exists():
            try:
                # Run processor with timeout (blocking but with limit)
                print(f"🤖 Processing: {queue_file.name}")
                
                result = subprocess.run(
                    [sys.executable, str(processor_script), str(queue_file)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(PROJECT_ROOT)
                )
                
                if result.returncode == 0:
                    print(f"✅ Helena processed successfully!")
                    # Show key results
                    if "Success rate: 4/4" in result.stdout:
                        print("   📊 4/4 databases updated")
                else:
                    print(f"⚠️  Processing failed (code: {result.returncode})")
                    if result.stderr:
                        print(f"   Error: {result.stderr[:200]}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏱️  Processing timeout - task may still be running")
            except Exception as e:
                print(f"⚠️  Could not trigger Helena: {e}")
                print(f"   Task queued: {queue_file}")
        else:
            print("ℹ️  Helena processor not found - task queued for batch processing")
            print(f"   Queue file: {queue_file}")


class RealtimeMarkdownWatcher:
    """Main watcher service"""
    
    def __init__(self):
        self.observer = Observer()
        self.handler = MarkdownFileHandler()
        
    def start(self):
        """Start watching"""
        
        print("\n" + "="*80)
        print(" "*20 + "🚀 REAL-TIME MARKDOWN WATCHER")
        print(" "*15 + "Instant Processing for Helena")
        print("="*80)
        print()
        print(f"📁 Watching: {PROJECT_ROOT}")
        print(f"📁 Documentation: {DOCS_DIR}")
        print(f"📝 Extensions: {', '.join(WATCHED_EXTENSIONS)}")
        print(f"🤖 Auto-processor: Helena")
        print()
        print("✨ How it works:")
        print("   1. You save a .md file in docs/ or root")
        print("   2. System detects it INSTANTLY")
        print("   3. Helena processes it automatically")
        print("   4. Content added to all databases")
        print("   5. Done! (usually under 10 seconds)")
        print()
        print("📝 Save your docs to:")
        print("   • docs/protocols/ - Process & protocols")
        print("   • docs/team/ - Team & agent info")
        print("   • docs/status/ - Status reports")
        print("   • docs/guides/ - Guides & tutorials")
        print("   • docs/architecture/ - System design")
        print()
        print("⌨️  Press Ctrl+C to stop")
        print("="*80)
        print()
        
        # Schedule the observer
        self.observer.schedule(
            self.handler,
            str(PROJECT_ROOT),
            recursive=True
        )
        
        # Start observing
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping watcher...")
            self.observer.stop()
            print("✅ Stopped cleanly")
            
        self.observer.join()


def main():
    """Main entry point"""
    
    watcher = RealtimeMarkdownWatcher()
    
    try:
        watcher.start()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
