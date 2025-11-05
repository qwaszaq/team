#!/usr/bin/env python3
"""
Elasticsearch Batch Processor
==============================
Batch-friendly ingestion system for Elasticsearch with PostgreSQL reference tracking
"""

import json
import time
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict
import requests
import psycopg2
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('elasticsearch_batch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ESBatchProcessor')

@dataclass
class ESDocument:
    """Elasticsearch document structure"""
    es_doc_id: str
    es_index: str
    filename: str
    content: str
    issuer: str
    report_url: str
    file_size: int
    sha256: str
    doc_type: str
    report_period: Optional[str] = None
    report_year: Optional[int] = None
    financial_metrics: Optional[Dict] = None
    entities: Optional[List[str]] = None
    indexed_at: Optional[str] = None
    data_classification: str = "public"
    investigation_id: Optional[str] = None
    tags: Optional[List[str]] = None
    confidence_score: float = 1.0

class ElasticsearchBatchProcessor:
    """Batch processor for Elasticsearch with integrated PostgreSQL tracking"""
    
    def __init__(self, 
                 es_url: str = "http://localhost:9200",
                 es_user: str = "elastic",
                 es_password: str = "changeme123",
                 batch_size: int = 100,
                 pg_conn_string: str = "dbname=destiny_team user=user password=password host=localhost"):
        
        self.es_url = es_url
        self.es_auth = (es_user, es_password)
        self.batch_size = batch_size
        self.pg_conn_string = pg_conn_string
        
        # Batch queues
        self.document_queue: List[ESDocument] = []
        self.reference_queue: List[Dict] = []
        
        # Statistics
        self.stats = defaultdict(int)
        
        # Verify Elasticsearch connection
        self._verify_es_connection()
        
    def _verify_es_connection(self):
        """Verify Elasticsearch is accessible"""
        try:
            response = requests.get(f"{self.es_url}/_cluster/health", auth=self.es_auth)
            response.raise_for_status()
            health = response.json()
            logger.info(f"✅ Elasticsearch cluster status: {health['status']}")
        except Exception as e:
            logger.error(f"❌ Elasticsearch connection failed: {e}")
            raise
            
    def add_document(self, 
                    file_path: Path, 
                    content: str,
                    metadata: Optional[Dict[str, Any]] = None) -> ESDocument:
        """Add document to batch queue"""
        
        # Generate document ID
        doc_id = self._generate_doc_id(file_path, content)
        
        # Extract metadata
        doc_metadata = self._extract_metadata(file_path, content, metadata or {})
        
        # Create ES document
        es_doc = ESDocument(
            es_doc_id=doc_id,
            es_index=doc_metadata.get('index', 'osint_documents'),
            filename=file_path.name,
            content=content,
            issuer=doc_metadata.get('issuer', 'Unknown'),
            report_url=doc_metadata.get('report_url', ''),
            file_size=file_path.stat().st_size if file_path.exists() else 0,
            sha256=hashlib.sha256(content.encode()).hexdigest(),
            doc_type=doc_metadata.get('doc_type', 'document'),
            report_period=doc_metadata.get('report_period'),
            report_year=doc_metadata.get('report_year'),
            financial_metrics=doc_metadata.get('financial_metrics'),
            entities=doc_metadata.get('entities', []),
            indexed_at=datetime.now().isoformat(),
            investigation_id=doc_metadata.get('investigation_id'),
            tags=doc_metadata.get('tags', []),
            confidence_score=doc_metadata.get('confidence_score', 1.0)
        )
        
        # Queue for batch processing
        self.document_queue.append(es_doc)
        self.stats['queued'] += 1
        
        logger.info(f"📄 Queued document: {file_path.name} (Queue size: {len(self.document_queue)})")
        
        # Check if we should flush
        if len(self.document_queue) >= self.batch_size:
            self.flush()
            
        return es_doc
        
    def _generate_doc_id(self, file_path: Path, content: str) -> str:
        """Generate unique document ID"""
        id_source = f"{file_path.name}:{len(content)}:{hashlib.md5(content.encode()).hexdigest()[:8]}"
        return hashlib.sha256(id_source.encode()).hexdigest()[:16]
        
    def _extract_metadata(self, file_path: Path, content: str, user_metadata: Dict) -> Dict:
        """Extract metadata from file path and content"""
        metadata = user_metadata.copy()
        
        # Extract from filename
        filename_lower = file_path.name.lower()
        
        # Determine document type
        if 'raport' in filename_lower or 'report' in filename_lower:
            metadata['doc_type'] = 'report'
        elif 'sprawozdanie' in filename_lower:
            metadata['doc_type'] = 'financial_statement'
        elif 'analiza' in filename_lower or 'analysis' in filename_lower:
            metadata['doc_type'] = 'analysis'
            
        # Extract year
        import re
        year_match = re.search(r'20\d{2}', file_path.name)
        if year_match:
            metadata['report_year'] = int(year_match.group())
            
        # Extract period
        if 'q1' in filename_lower or '1q' in filename_lower:
            metadata['report_period'] = 'Q1'
        elif 'q2' in filename_lower or '2q' in filename_lower:
            metadata['report_period'] = 'Q2'
        elif 'q3' in filename_lower or '3q' in filename_lower:
            metadata['report_period'] = 'Q3'
        elif 'q4' in filename_lower or '4q' in filename_lower:
            metadata['report_period'] = 'Q4'
        elif 'annual' in filename_lower or 'roczn' in filename_lower:
            metadata['report_period'] = 'Annual'
            
        # Auto-tagging
        tags = metadata.get('tags', [])
        if 'grupa' in filename_lower and 'azoty' in filename_lower:
            tags.extend(['grupa-azoty', 'chemical-industry'])
        if 'financial' in content.lower() or 'finansow' in content.lower():
            tags.append('financial')
        if 'sustainability' in content.lower():
            tags.append('sustainability')
            
        metadata['tags'] = list(set(tags))  # Remove duplicates
        
        return metadata
        
    def flush(self):
        """Flush all queued documents to Elasticsearch and PostgreSQL"""
        if not self.document_queue:
            logger.info("No documents to flush")
            return
            
        start_time = time.time()
        logger.info(f"🚀 Flushing {len(self.document_queue)} documents...")
        
        # Prepare bulk operations
        bulk_data = self._prepare_bulk_data()
        
        # Execute bulk index to Elasticsearch
        es_results = self._bulk_index_to_es(bulk_data)
        
        # Create PostgreSQL references
        pg_results = self._bulk_create_pg_references()
        
        # Clear queues
        self.document_queue.clear()
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Flush complete in {elapsed:.2f}s")
        logger.info(f"   ES indexed: {es_results['successful']}")
        logger.info(f"   PG references: {pg_results['created']}")
        
    def _prepare_bulk_data(self) -> str:
        """Prepare bulk data for Elasticsearch"""
        bulk_lines = []
        
        for doc in self.document_queue:
            # Index action
            action = {
                "index": {
                    "_index": doc.es_index,
                    "_id": doc.es_doc_id
                }
            }
            bulk_lines.append(json.dumps(action))
            
            # Document data
            doc_dict = asdict(doc)
            # Remove fields that shouldn't be indexed
            doc_dict.pop('es_doc_id', None)
            doc_dict.pop('es_index', None)
            
            bulk_lines.append(json.dumps(doc_dict))
            
        return '\n'.join(bulk_lines) + '\n'
        
    def _bulk_index_to_es(self, bulk_data: str) -> Dict:
        """Execute bulk index operation"""
        try:
            response = requests.post(
                f"{self.es_url}/_bulk",
                data=bulk_data,
                headers={'Content-Type': 'application/x-ndjson'},
                auth=self.es_auth
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Count results
            successful = sum(1 for item in result.get('items', []) 
                           if item['index'].get('result') in ['created', 'updated'])
            failed = sum(1 for item in result.get('items', []) 
                        if 'error' in item['index'])
            
            self.stats['es_indexed'] += successful
            self.stats['es_failed'] += failed
            
            if failed > 0:
                logger.warning(f"⚠️  {failed} documents failed to index")
                
            return {'successful': successful, 'failed': failed}
            
        except Exception as e:
            logger.error(f"Bulk index error: {e}")
            return {'successful': 0, 'failed': len(self.document_queue)}
            
    def _bulk_create_pg_references(self) -> Dict:
        """Create PostgreSQL references for indexed documents"""
        conn = None
        created = 0
        
        try:
            conn = psycopg2.connect(self.pg_conn_string)
            cur = conn.cursor()
            
            # Prepare batch insert
            values = []
            params = []
            
            for doc in self.document_queue:
                values.append("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                params.extend([
                    doc.es_index,
                    doc.es_doc_id,
                    doc.doc_type,
                    doc.issuer,
                    doc.report_url,
                    doc.filename,
                    doc.file_size,
                    doc.sha256,
                    doc.indexed_at,
                    doc.data_classification,
                    doc.investigation_id,
                    doc.tags,
                    json.dumps({'report_year': doc.report_year, 'report_period': doc.report_period})
                ])
                
            # Single batch insert
            query = f"""
            INSERT INTO es_document_references 
            (es_index, es_doc_id, doc_type, issuer, report_url, filename,
             file_size, sha256, indexed_at, data_classification, 
             investigation_id, tags, metadata)
            VALUES {','.join(values)}
            ON CONFLICT (es_doc_id) DO UPDATE SET
                indexed_at = EXCLUDED.indexed_at,
                tags = EXCLUDED.tags,
                metadata = EXCLUDED.metadata;
            """
            
            cur.execute(query, params)
            created = cur.rowcount
            conn.commit()
            
            self.stats['pg_referenced'] += created
            
            return {'created': created}
            
        except Exception as e:
            logger.error(f"PostgreSQL reference error: {e}")
            if conn:
                conn.rollback()
            return {'created': 0}
        finally:
            if conn:
                conn.close()
                
    def process_directory(self, directory: Path, pattern: str = "*.pdf"):
        """Process all matching files in directory"""
        logger.info(f"📁 Processing directory: {directory}")
        
        files = list(directory.glob(pattern))
        logger.info(f"Found {len(files)} files matching {pattern}")
        
        for i, file_path in enumerate(files, 1):
            try:
                # For PDFs, we'd normally extract text here
                # For now, using placeholder
                content = f"[PDF content from {file_path.name}]"
                
                # Add to batch
                self.add_document(
                    file_path=file_path,
                    content=content,
                    metadata={
                        'index': 'osint_reports_pdf',
                        'issuer': 'Grupa Azoty' if 'azoty' in str(file_path).lower() else 'Unknown',
                        'investigation_id': 'grupa_azoty_financial'
                    }
                )
                
                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(files)} files queued")
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                self.stats['errors'] += 1
                
        # Final flush
        self.flush()
        
    def get_stats(self) -> Dict:
        """Get processing statistics"""
        return dict(self.stats)

class SearchOrchestrator:
    """Unified search interface across Elasticsearch, Qdrant, PostgreSQL, and Neo4j"""
    
    def __init__(self, es_processor: ElasticsearchBatchProcessor):
        self.es_processor = es_processor
        
    def full_text_search(self, query: str, index: str = 'osint_reports_pdf') -> List[Dict]:
        """Full-text search in Elasticsearch"""
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["content", "filename", "issuer"],
                    "type": "best_fields"
                }
            },
            "highlight": {
                "fields": {
                    "content": {"fragment_size": 150}
                }
            },
            "size": 20
        }
        
        try:
            response = requests.post(
                f"{self.es_processor.es_url}/{index}/_search",
                json=search_body,
                auth=self.es_processor.es_auth
            )
            response.raise_for_status()
            
            results = []
            for hit in response.json()['hits']['hits']:
                results.append({
                    'id': hit['_id'],
                    'score': hit['_score'],
                    'source': hit['_source'],
                    'highlights': hit.get('highlight', {})
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
            
    def time_series_aggregation(self, field: str, index: str = 'osint_reports_pdf') -> Dict:
        """Aggregate data over time"""
        agg_body = {
            "aggs": {
                "timeline": {
                    "date_histogram": {
                        "field": "report_year",
                        "interval": "year",
                        "min_doc_count": 1
                    },
                    "aggs": {
                        "by_period": {
                            "terms": {
                                "field": "report_period"
                            }
                        }
                    }
                }
            },
            "size": 0
        }
        
        try:
            response = requests.post(
                f"{self.es_processor.es_url}/{index}/_search",
                json=agg_body,
                auth=self.es_processor.es_auth
            )
            response.raise_for_status()
            
            return response.json()['aggregations']
            
        except Exception as e:
            logger.error(f"Aggregation error: {e}")
            return {}

def main():
    """Test the batch processor"""
    logger.info("🚀 Elasticsearch Batch Processor Test")
    logger.info("=" * 50)
    
    # Initialize processor
    processor = ElasticsearchBatchProcessor(
        batch_size=50  # Process in batches of 50
    )
    
    # Test with sample documents
    test_dir = Path("/Users/artur/coursor-agents-destiny-folder/investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs")
    
    if test_dir.exists():
        processor.process_directory(test_dir)
        
        # Show statistics
        stats = processor.get_stats()
        logger.info("📊 Processing Statistics:")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
            
        # Test search
        orchestrator = SearchOrchestrator(processor)
        
        logger.info("\n🔍 Testing search...")
        results = orchestrator.full_text_search("financial statement")
        logger.info(f"Found {len(results)} results")
        
        # Test aggregation
        logger.info("\n📈 Testing aggregation...")
        timeline = orchestrator.time_series_aggregation("report_year")
        logger.info(f"Timeline data: {json.dumps(timeline, indent=2)}")
        
    else:
        logger.warning(f"Test directory not found: {test_dir}")
        
if __name__ == "__main__":
    main()