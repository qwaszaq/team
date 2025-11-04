#!/usr/bin/env python3
"""
Hourly Batch Processor
======================
Processes accumulated documents once per hour for maximum efficiency
"""

import json
import time
import schedule
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import psycopg2
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hourly_batch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('HourlyBatch')

class HourlyBatchProcessor:
    """Process accumulated files once per hour"""
    
    def __init__(self):
        self.project_root = Path("/Users/artur/coursor-agents-destiny-folder")
        self.queue_dir = self.project_root / "batch_queue"
        self.processed_dir = self.project_root / "batch_processed"
        self.queue_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        
        # Database connection string
        self.conn_string = "dbname=destiny_team user=user password=password host=localhost"
        
        # Statistics
        self.stats = {
            'last_run': None,
            'total_processed': 0,
            'total_errors': 0
        }
        
    def queue_document(self, file_path: Path, metadata: Dict[str, Any] = None):
        """Add document to hourly batch queue"""
        queue_entry = {
            'file_path': str(file_path),
            'queued_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # Save to queue directory
        queue_file = self.queue_dir / f"{file_path.stem}_{int(time.time())}.json"
        with open(queue_file, 'w') as f:
            json.dump(queue_entry, f, indent=2)
            
        logger.info(f"Queued document: {file_path.name}")
        
    def process_hourly_batch(self):
        """Process all queued documents in a single batch"""
        start_time = datetime.now()
        logger.info("=" * 60)
        logger.info(f"🕐 Starting hourly batch processing at {start_time}")
        
        # Get all queued files
        queue_files = list(self.queue_dir.glob("*.json"))
        
        if not queue_files:
            logger.info("No files in queue to process")
            return
            
        logger.info(f"Found {len(queue_files)} files to process")
        
        # Group operations by type
        operations = {
            'document_references': [],
            'messages': [],
            'agent_contexts': []
        }
        
        # Process queue files
        for queue_file in queue_files:
            try:
                with open(queue_file, 'r') as f:
                    entry = json.load(f)
                    
                # Process based on file type
                file_path = Path(entry['file_path'])
                if file_path.exists():
                    ops = self._process_document(file_path, entry.get('metadata', {}))
                    
                    # Accumulate operations
                    for op_type, op_data in ops.items():
                        if op_data:
                            operations[op_type].extend(op_data)
                            
                # Move to processed
                processed_file = self.processed_dir / queue_file.name
                queue_file.rename(processed_file)
                
            except Exception as e:
                logger.error(f"Error processing queue file {queue_file}: {e}")
                self.stats['total_errors'] += 1
                
        # Execute batch operations
        if any(operations.values()):
            self._execute_batch_operations(operations)
            
        # Update statistics
        self.stats['last_run'] = start_time
        self.stats['total_processed'] += len(queue_files)
        
        # Log summary
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Batch processing complete")
        logger.info(f"   Processed: {len(queue_files)} files")
        logger.info(f"   Duration: {elapsed:.2f} seconds")
        logger.info(f"   Rate: {len(queue_files)/elapsed:.1f} files/second")
        logger.info("=" * 60)
        
        # Clean old processed files (keep last 7 days)
        self._cleanup_old_files()
        
    def _process_document(self, file_path: Path, metadata: Dict) -> Dict[str, List]:
        """Process a single document and return operations"""
        operations = {
            'document_references': [],
            'messages': [],
            'agent_contexts': []
        }
        
        try:
            # Read document
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Create document reference
            import hashlib
            doc_id = f"{file_path.stem}_{int(time.time())}"
            
            operations['document_references'].append({
                'es_index': 'batch_documents',
                'es_doc_id': doc_id,
                'doc_type': self._determine_doc_type(file_path),
                'filename': file_path.name,
                'file_size': file_path.stat().st_size,
                'sha256': hashlib.sha256(content.encode()).hexdigest(),
                'issuer': 'Hourly Batch Processor',
                'investigation_id': metadata.get('investigation_id', 'general'),
                'tags': self._extract_tags(file_path, content),
                'metadata': {
                    'batch_processed': True,
                    'original_path': str(file_path),
                    **metadata
                }
            })
            
            # Create processing message
            operations['messages'].append({
                'id': f'batch_{doc_id}',
                'project_id': 'hourly_batch',
                'sender': 'HourlyBatchProcessor',
                'content': f'Processed {file_path.name} in hourly batch',
                'message_type': 'BATCH_PROCESSED',
                'importance': 0.2,
                'timestamp': datetime.now()
            })
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            
        return operations
        
    def _execute_batch_operations(self, operations: Dict[str, List]):
        """Execute all operations in a single transaction"""
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            
            # Insert document references
            if operations['document_references']:
                self._batch_insert_references(cur, operations['document_references'])
                
            # Insert messages
            if operations['messages']:
                self._batch_insert_messages(cur, operations['messages'])
                
            # Update agent contexts
            if operations['agent_contexts']:
                self._batch_update_contexts(cur, operations['agent_contexts'])
                
            # Commit all operations
            conn.commit()
            logger.info(f"Committed {sum(len(ops) for ops in operations.values())} operations")
            
        except Exception as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
                
    def _batch_insert_references(self, cur, references: List[Dict]):
        """Batch insert document references"""
        if not references:
            return
            
        # Build multi-row insert
        values = []
        params = []
        
        for ref in references:
            values.append("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            params.extend([
                ref['es_index'],
                ref['es_doc_id'],
                ref['doc_type'],
                ref.get('issuer', ''),
                ref.get('report_url', ''),
                ref['filename'],
                ref.get('file_size', 0),
                ref.get('sha256', ''),
                datetime.now(),
                ref.get('data_classification', 'public'),
                ref.get('investigation_id'),
                ref.get('tags', []),
                json.dumps(ref.get('metadata', {}))
            ])
            
        query = f"""
        INSERT INTO es_document_references 
        (es_index, es_doc_id, doc_type, issuer, report_url, filename,
         file_size, sha256, indexed_at, data_classification, investigation_id, tags, metadata)
        VALUES {','.join(values)}
        ON CONFLICT (es_doc_id) DO UPDATE SET
            metadata = EXCLUDED.metadata,
            indexed_at = EXCLUDED.indexed_at;
        """
        
        cur.execute(query, params)
        logger.info(f"Inserted {len(references)} document references")
        
    def _batch_insert_messages(self, cur, messages: List[Dict]):
        """Batch insert messages"""
        for msg in messages:
            cur.execute("""
                INSERT INTO messages 
                (id, project_id, sender, recipient, message_type, content, 
                 context, timestamp, requires_response, importance, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                msg['id'],
                msg['project_id'],
                msg['sender'],
                msg.get('recipient', 'Team'),
                msg['message_type'],
                msg['content'],
                json.dumps(msg.get('context', {})),
                msg['timestamp'],
                msg.get('requires_response', False),
                msg.get('importance', 0.5),
                msg.get('tags', [])
            ))
            
    def _batch_update_contexts(self, cur, contexts: List[Dict]):
        """Batch update agent contexts"""
        for ctx in contexts:
            cur.execute("""
                INSERT INTO agent_contexts 
                (agent_name, project_id, context_key, context_value, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (agent_name, project_id, context_key)
                DO UPDATE SET 
                    context_value = EXCLUDED.context_value,
                    updated_at = EXCLUDED.updated_at;
            """, (
                ctx['agent_name'],
                ctx['project_id'],
                ctx['context_key'],
                json.dumps(ctx['context_value']),
                datetime.now()
            ))
            
    def _determine_doc_type(self, file_path: Path) -> str:
        """Determine document type"""
        name_lower = file_path.name.lower()
        if 'analysis' in name_lower:
            return 'analysis'
        elif 'report' in name_lower:
            return 'report'
        elif 'commit' in name_lower:
            return 'commit'
        else:
            return 'document'
            
    def _extract_tags(self, file_path: Path, content: str) -> List[str]:
        """Extract relevant tags"""
        tags = ['hourly-batch']
        
        # Add more tags based on content/path
        if 'critical' in content.lower():
            tags.append('critical')
        if 'postgres' in content.lower():
            tags.append('postgresql')
            
        return tags
        
    def _cleanup_old_files(self):
        """Clean up old processed files"""
        cutoff_time = time.time() - (7 * 24 * 60 * 60)  # 7 days
        
        for file in self.processed_dir.glob("*.json"):
            if file.stat().st_mtime < cutoff_time:
                file.unlink()
                logger.debug(f"Cleaned up old file: {file.name}")
                
    def run_scheduler(self):
        """Run the hourly scheduler"""
        logger.info("🕐 Hourly Batch Processor Started")
        logger.info(f"Queue directory: {self.queue_dir}")
        logger.info(f"Schedule: Every hour at :00")
        logger.info("-" * 60)
        
        # Schedule hourly runs
        schedule.every().hour.at(":00").do(self.process_hourly_batch)
        
        # Also run at startup
        logger.info("Running initial batch processing...")
        self.process_hourly_batch()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hourly Batch Processor")
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    parser.add_argument('--queue', type=str, help='Queue a file for processing')
    parser.add_argument('--status', action='store_true', help='Show processor status')
    
    args = parser.parse_args()
    
    processor = HourlyBatchProcessor()
    
    if args.queue:
        # Queue a file
        file_path = Path(args.queue)
        if file_path.exists():
            processor.queue_document(file_path)
            print(f"✅ Queued: {file_path.name}")
        else:
            print(f"❌ File not found: {file_path}")
            
    elif args.status:
        # Show status
        print("Hourly Batch Processor Status")
        print("=" * 40)
        print(f"Queue directory: {processor.queue_dir}")
        queue_count = len(list(processor.queue_dir.glob("*.json")))
        print(f"Files in queue: {queue_count}")
        print(f"Last run: {processor.stats.get('last_run', 'Never')}")
        print(f"Total processed: {processor.stats.get('total_processed', 0)}")
        
    elif args.run_once:
        # Run once
        processor.process_hourly_batch()
        
    else:
        # Run scheduler
        try:
            processor.run_scheduler()
        except KeyboardInterrupt:
            logger.info("\n🛑 Hourly Batch Processor stopped")

if __name__ == "__main__":
    main()