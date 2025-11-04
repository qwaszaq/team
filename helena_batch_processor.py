#!/usr/bin/env python3
"""
Helena's Batch Processing Replacement
=====================================
Replaces real-time processor with intelligent batching
"""

import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import logging

# Add project root
PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
sys.path.insert(0, str(PROJECT_ROOT))

from batch_processing_system import init_batch_processor, add_document_reference, add_message, add_agent_context

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Helena Batch - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HelenaBatch')

class HelenaBatchProcessor:
    """Helena's batch processing system for documents"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.pending_dir = self.project_root / "helena_batch_pending"
        self.pending_dir.mkdir(exist_ok=True)
        
        # Initialize batch processor
        self.batch_processor = init_batch_processor()
        logger.info("Helena Batch Processor initialized")
        
    def process_document(self, file_path: Path):
        """Process a document and add to batch queue"""
        logger.info(f"Processing document: {file_path}")
        
        try:
            # Read document content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract metadata
            doc_id = f"{file_path.stem}_{int(time.time())}"
            sha256 = hashlib.sha256(content.encode()).hexdigest()
            
            # Determine document type
            doc_type = self._determine_doc_type(file_path)
            
            # Add to batch queue
            add_document_reference({
                'es_doc_id': doc_id,
                'doc_type': doc_type,
                'filename': file_path.name,
                'file_size': file_path.stat().st_size,
                'sha256': sha256,
                'issuer': 'Helena Batch Processor',
                'investigation_id': self._extract_investigation_id(file_path),
                'tags': self._extract_tags(file_path, content),
                'metadata': {
                    'processed_by': 'helena_batch',
                    'source_path': str(file_path),
                    'content_preview': content[:500]
                }
            })
            
            # Add processing notification
            add_message({
                'id': f'helena_batch_{doc_id}',
                'project_id': 'helena_batch_processing',
                'sender': 'Helena',
                'content': f'Document {file_path.name} added to batch queue',
                'message_type': 'BATCH_QUEUED',
                'importance': 0.3
            })
            
            # Update agent context
            add_agent_context({
                'agent_name': 'Helena',
                'project_id': 'batch_processing',
                'context_key': 'last_processed',
                'context_value': {
                    'file': str(file_path),
                    'time': datetime.now().isoformat(),
                    'status': 'queued'
                }
            })
            
            logger.info(f"Document {file_path.name} queued successfully")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            
    def _determine_doc_type(self, file_path: Path) -> str:
        """Determine document type from path"""
        if 'commit' in str(file_path).lower():
            return 'commit'
        elif 'analysis' in str(file_path).lower():
            return 'analysis'
        elif 'report' in str(file_path).lower():
            return 'report'
        else:
            return 'document'
            
    def _extract_investigation_id(self, file_path: Path) -> str:
        """Extract investigation ID from path or content"""
        path_str = str(file_path).lower()
        
        if 'grupa_azoty' in path_str or 'azoty' in path_str:
            return 'grupa_azoty_financial'
        elif 'osint' in path_str:
            return 'general_osint'
        elif 'technical' in path_str:
            return 'technical_analysis'
        else:
            return 'general'
            
    def _extract_tags(self, file_path: Path, content: str) -> List[str]:
        """Extract relevant tags"""
        tags = []
        
        # Path-based tags
        if file_path.suffix == '.md':
            tags.append('markdown')
        
        # Content-based tags
        content_lower = content.lower()
        if 'postgresql' in content_lower or 'postgres' in content_lower:
            tags.append('postgresql')
        if 'performance' in content_lower:
            tags.append('performance')
        if 'critical' in content_lower:
            tags.append('critical')
        if 'batch' in content_lower:
            tags.append('batch-processing')
            
        return tags
        
    def watch_directory(self, directory: Path, interval: float = 1.0):
        """Watch directory for new files to batch process"""
        logger.info(f"Watching directory: {directory}")
        
        processed_files = set()
        
        try:
            while True:
                # Check for new files
                for file_path in directory.rglob("*.md"):
                    if file_path not in processed_files:
                        self.process_document(file_path)
                        processed_files.add(file_path)
                        
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Stopping directory watch")
            self.batch_processor.stop()
            
    def process_pending_queue(self):
        """Process all pending documents in batch"""
        pending_files = list(self.pending_dir.glob("*.json"))
        
        if not pending_files:
            logger.info("No pending files to process")
            return
            
        logger.info(f"Processing {len(pending_files)} pending files")
        
        for pending_file in pending_files:
            try:
                with open(pending_file, 'r') as f:
                    data = json.load(f)
                    
                # Add to appropriate batch queue
                if data['type'] == 'document_reference':
                    add_document_reference(data['data'])
                elif data['type'] == 'message':
                    add_message(data['data'])
                elif data['type'] == 'agent_context':
                    add_agent_context(data['data'])
                    
                # Remove pending file
                pending_file.unlink()
                
            except Exception as e:
                logger.error(f"Error processing pending file {pending_file}: {e}")
                
        logger.info("Pending queue processed")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Helena's Batch Processor")
    parser.add_argument('--watch', type=str, help='Directory to watch')
    parser.add_argument('--process-pending', action='store_true', help='Process pending queue')
    parser.add_argument('--test', action='store_true', help='Run test mode')
    
    args = parser.parse_args()
    
    processor = HelenaBatchProcessor()
    
    if args.test:
        # Test mode
        print("🧪 Running in test mode")
        test_file = PROJECT_ROOT / "POSTGRES_STUCK_ANALYSIS.md"
        if test_file.exists():
            processor.process_document(test_file)
            time.sleep(6)  # Wait for batch timeout
            processor.batch_processor.stop()
        else:
            print("❌ Test file not found")
            
    elif args.process_pending:
        processor.process_pending_queue()
        time.sleep(6)  # Wait for batch timeout
        processor.batch_processor.stop()
        
    elif args.watch:
        watch_dir = Path(args.watch)
        if watch_dir.exists():
            processor.watch_directory(watch_dir)
        else:
            print(f"❌ Directory not found: {watch_dir}")
            
    else:
        print("Helena's Batch Processor")
        print("========================")
        print()
        print("Usage:")
        print("  --watch <dir>     Watch directory for new files")
        print("  --process-pending Process pending queue")
        print("  --test           Run test mode")
        print()

if __name__ == "__main__":
    main()