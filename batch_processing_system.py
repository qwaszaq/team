#!/usr/bin/env python3
"""
Batch Processing System for PostgreSQL
======================================
Replace real-time processing with intelligent batching to prevent database overload
"""

import json
import time
import queue
import threading
import psycopg2
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BatchProcessor')

class BatchProcessor:
    """Intelligent batch processor for database operations"""
    
    def __init__(self, 
                 batch_size: int = 100,
                 batch_timeout: float = 5.0,
                 max_connections: int = 3):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.max_connections = max_connections
        
        # Queues for different operation types
        self.insert_queue = queue.Queue()
        self.update_queue = queue.Queue()
        self.message_queue = queue.Queue()
        
        # Batch accumulators
        self.batches = {
            'inserts': defaultdict(list),
            'updates': defaultdict(list),
            'messages': []
        }
        
        # Control flags
        self.running = False
        self.last_flush = time.time()
        
        # Database connection pool
        self.connections = []
        self._init_connection_pool()
        
    def _init_connection_pool(self):
        """Initialize connection pool with limited connections"""
        conn_string = "dbname=destiny_team user=user password=password host=localhost"
        
        for i in range(self.max_connections):
            try:
                conn = psycopg2.connect(conn_string)
                conn.set_session(autocommit=False)
                self.connections.append(conn)
                logger.info(f"Connection {i+1}/{self.max_connections} established")
            except Exception as e:
                logger.error(f"Failed to create connection {i+1}: {e}")
                
    def add_operation(self, operation_type: str, table: str, data: Dict[str, Any]):
        """Add operation to appropriate queue"""
        operation = {
            'table': table,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        if operation_type == 'insert':
            self.insert_queue.put(operation)
        elif operation_type == 'update':
            self.update_queue.put(operation)
        elif operation_type == 'message':
            self.message_queue.put(operation)
            
        # Check if we should flush
        if self._should_flush():
            self.flush_all()
            
    def _should_flush(self) -> bool:
        """Determine if batches should be flushed"""
        # Flush if timeout reached
        if time.time() - self.last_flush > self.batch_timeout:
            return True
            
        # Flush if any batch is full
        for batch_type, batches in self.batches.items():
            if isinstance(batches, list) and len(batches) >= self.batch_size:
                return True
            elif isinstance(batches, dict):
                for table_batch in batches.values():
                    if len(table_batch) >= self.batch_size:
                        return True
                        
        return False
        
    def process_batch_worker(self):
        """Worker thread for processing batches"""
        logger.info("Batch processor worker started")
        
        while self.running:
            try:
                # Accumulate operations
                self._accumulate_operations()
                
                # Check if we should flush
                if self._should_flush():
                    self.flush_all()
                    
                # Small sleep to prevent CPU spinning
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Batch processor error: {e}")
                time.sleep(1)
                
    def _accumulate_operations(self):
        """Move operations from queues to batches"""
        # Process inserts
        while not self.insert_queue.empty():
            try:
                op = self.insert_queue.get_nowait()
                self.batches['inserts'][op['table']].append(op)
            except queue.Empty:
                break
                
        # Process updates
        while not self.update_queue.empty():
            try:
                op = self.update_queue.get_nowait()
                self.batches['updates'][op['table']].append(op)
            except queue.Empty:
                break
                
        # Process messages
        while not self.message_queue.empty():
            try:
                op = self.message_queue.get_nowait()
                self.batches['messages'].append(op)
            except queue.Empty:
                break
                
    def flush_all(self):
        """Flush all batches to database"""
        start_time = time.time()
        total_ops = 0
        
        # Get available connection
        if not self.connections:
            logger.error("No database connections available")
            return
            
        conn = self.connections[0]
        cur = conn.cursor()
        
        try:
            # Process document references batch
            if 'es_document_references' in self.batches['inserts']:
                refs_batch = self.batches['inserts']['es_document_references']
                if refs_batch:
                    total_ops += self._flush_document_references(cur, refs_batch)
                    self.batches['inserts']['es_document_references'] = []
                    
            # Process messages batch
            if self.batches['messages']:
                total_ops += self._flush_messages(cur, self.batches['messages'])
                self.batches['messages'] = []
                
            # Process agent contexts batch
            if 'agent_contexts' in self.batches['updates']:
                ctx_batch = self.batches['updates']['agent_contexts']
                if ctx_batch:
                    total_ops += self._flush_agent_contexts(cur, ctx_batch)
                    self.batches['updates']['agent_contexts'] = []
                    
            # Commit transaction
            conn.commit()
            
            elapsed = time.time() - start_time
            if total_ops > 0:
                logger.info(f"Flushed {total_ops} operations in {elapsed:.2f}s ({total_ops/elapsed:.1f} ops/sec)")
                
        except Exception as e:
            logger.error(f"Flush error: {e}")
            conn.rollback()
            
        finally:
            self.last_flush = time.time()
            
    def _flush_document_references(self, cur, batch: List[Dict]) -> int:
        """Flush document references using COPY for maximum performance"""
        if not batch:
            return 0
            
        # Build values for multi-row insert
        values = []
        params = []
        
        for op in batch:
            data = op['data']
            values.append("""(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            params.extend([
                data.get('es_index', 'osint_reports_pdf'),
                data['es_doc_id'],
                data.get('doc_type', 'document'),
                data.get('issuer', ''),
                data.get('report_url', ''),
                data.get('filename', ''),
                data.get('file_size', 0),
                data.get('sha256', ''),
                data.get('indexed_at', datetime.now()),
                data.get('data_classification', 'public'),
                data.get('investigation_id'),
                data.get('tags', []),
                json.dumps(data.get('metadata', {}))
            ])
            
        # Single batch insert
        query = f"""
        INSERT INTO es_document_references 
        (es_index, es_doc_id, doc_type, issuer, report_url, filename,
         file_size, sha256, indexed_at, data_classification, investigation_id, tags, metadata)
        VALUES {','.join(values)}
        ON CONFLICT (es_doc_id) DO UPDATE SET
            issuer = EXCLUDED.issuer,
            tags = EXCLUDED.tags,
            metadata = EXCLUDED.metadata;
        """
        
        cur.execute(query, params)
        logger.debug(f"Flushed {len(batch)} document references")
        return len(batch)
        
    def _flush_messages(self, cur, batch: List[Dict]) -> int:
        """Flush messages batch"""
        if not batch:
            return 0
            
        for op in batch:
            data = op['data']
            cur.execute("""
                INSERT INTO messages 
                (id, project_id, sender, recipient, message_type, content, 
                 context, timestamp, requires_response, response_to, importance, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                data['id'],
                data['project_id'],
                data['sender'],
                data.get('recipient', 'Team'),
                data.get('message_type', 'NOTIFICATION'),
                data['content'],
                json.dumps(data.get('context', {})),
                data.get('timestamp', datetime.now()),
                data.get('requires_response', False),
                data.get('response_to'),
                data.get('importance', 0.5),
                data.get('tags', [])
            ))
            
        logger.debug(f"Flushed {len(batch)} messages")
        return len(batch)
        
    def _flush_agent_contexts(self, cur, batch: List[Dict]) -> int:
        """Flush agent contexts batch"""
        if not batch:
            return 0
            
        for op in batch:
            data = op['data']
            cur.execute("""
                INSERT INTO agent_contexts 
                (agent_name, project_id, context_key, context_value, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (agent_name, project_id, context_key)
                DO UPDATE SET 
                    context_value = EXCLUDED.context_value,
                    updated_at = EXCLUDED.updated_at;
            """, (
                data['agent_name'],
                data['project_id'],
                data['context_key'],
                json.dumps(data.get('context_value', {})),
                datetime.now()
            ))
            
        logger.debug(f"Flushed {len(batch)} agent contexts")
        return len(batch)
        
    def start(self):
        """Start batch processor"""
        if self.running:
            return
            
        self.running = True
        self.worker_thread = threading.Thread(target=self.process_batch_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        logger.info("Batch processor started")
        
    def stop(self):
        """Stop batch processor"""
        logger.info("Stopping batch processor...")
        self.running = False
        
        # Final flush
        self.flush_all()
        
        # Close connections
        for conn in self.connections:
            conn.close()
            
        logger.info("Batch processor stopped")

# Global batch processor instance
batch_processor = None

def init_batch_processor():
    """Initialize global batch processor"""
    global batch_processor
    batch_processor = BatchProcessor(
        batch_size=100,
        batch_timeout=5.0,
        max_connections=3
    )
    batch_processor.start()
    return batch_processor

def add_document_reference(doc_data: Dict[str, Any]):
    """Add document reference to batch queue"""
    if batch_processor:
        batch_processor.add_operation('insert', 'es_document_references', doc_data)
    else:
        logger.error("Batch processor not initialized")

def add_message(message_data: Dict[str, Any]):
    """Add message to batch queue"""
    if batch_processor:
        batch_processor.add_operation('message', 'messages', message_data)
    else:
        logger.error("Batch processor not initialized")

def add_agent_context(context_data: Dict[str, Any]):
    """Add agent context update to batch queue"""
    if batch_processor:
        batch_processor.add_operation('update', 'agent_contexts', context_data)
    else:
        logger.error("Batch processor not initialized")

if __name__ == "__main__":
    # Test batch processor
    print("🚀 Testing Batch Processor")
    print("=" * 50)
    
    # Initialize
    processor = init_batch_processor()
    
    # Simulate operations
    print("Adding test operations...")
    
    for i in range(250):
        # Document reference
        add_document_reference({
            'es_doc_id': f'test_doc_{i}',
            'issuer': 'Test Issuer',
            'filename': f'test_{i}.pdf',
            'file_size': 1024 * (i + 1),
            'investigation_id': 'test_investigation',
            'tags': ['test', 'batch'],
            'metadata': {'index': i}
        })
        
        # Message every 10 docs
        if i % 10 == 0:
            add_message({
                'id': f'msg_{i}',
                'project_id': 'test_project',
                'sender': 'BatchTest',
                'content': f'Processing batch item {i}',
                'importance': 0.5
            })
            
    print("Waiting for batch processing...")
    time.sleep(10)
    
    print("Stopping processor...")
    processor.stop()
    
    print("✅ Test complete!")