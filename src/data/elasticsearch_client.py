"""
Elasticsearch Client for Document Storage
Paweł Kowalski
2025-11-05
"""

import urllib.request
import urllib.error
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib


class ElasticsearchClient:
    """
    Elasticsearch client for document storage and full-text search
    
    Features:
    - Store raw documents (PDF, DOC content)
    - Full-text search
    - Metadata management
    - Aggregations
    
    Use for:
    - Document repository (1000s of files)
    - Full-text keyword search
    - Document versioning
    - Metadata queries
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 9200,
        index_name: str = "destiny_documents"
    ):
        """
        Initialize Elasticsearch client
        
        Args:
            host: Elasticsearch host
            port: Elasticsearch port
            index_name: Index name
        """
        self.base_url = f"http://{host}:{port}"
        self.index_name = index_name
        self.available = self._check_availability()
        
        if self.available:
            self._ensure_index()
    
    def _check_availability(self) -> bool:
        """Check if Elasticsearch is available"""
        try:
            req = urllib.request.Request(f"{self.base_url}/_cluster/health")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    def _ensure_index(self):
        """Ensure index exists with proper mappings"""
        # Check if index exists
        try:
            req = urllib.request.Request(f"{self.base_url}/{self.index_name}")
            with urllib.request.urlopen(req, timeout=5):
                return  # Index exists
        except urllib.error.HTTPError as e:
            if e.code == 404:
                self._create_index()
    
    def _create_index(self):
        """Create Elasticsearch index"""
        mappings = {
            "mappings": {
                "properties": {
                    "case_id": {"type": "keyword"},
                    "document_id": {"type": "keyword"},
                    "filename": {"type": "text"},
                    "content": {"type": "text"},
                    "document_type": {"type": "keyword"},
                    "file_size": {"type": "integer"},
                    "created_at": {"type": "date"},
                    "metadata": {"type": "object", "enabled": True}
                }
            }
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/{self.index_name}",
            data=json.dumps(mappings).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10):
                print(f"✅ Elasticsearch index created: {self.index_name}")
        except Exception as e:
            print(f"⚠️  Index creation failed: {e}")
    
    def store_document(
        self,
        case_id: str,
        document_id: str,
        filename: str,
        content: str,
        document_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store document in Elasticsearch
        
        Args:
            case_id: Case identifier
            document_id: Document identifier
            filename: Original filename
            content: Document content
            document_type: Type of document
            metadata: Optional metadata
            
        Returns:
            Document ID
        """
        if not self.available:
            raise Exception("Elasticsearch not available")
        
        doc = {
            "case_id": case_id,
            "document_id": document_id,
            "filename": filename,
            "content": content,
            "document_type": document_type,
            "file_size": len(content),
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/{self.index_name}/_doc/{document_id}",
            data=json.dumps(doc).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        with urllib.request.urlopen(req, timeout=10):
            return document_id
    
    def full_text_search(
        self,
        query: str,
        case_id: Optional[str] = None,
        document_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Full-text search across documents
        
        Args:
            query: Search query
            case_id: Optional case filter
            document_type: Optional document type filter
            limit: Max results
            
        Returns:
            List of matching documents
        """
        if not self.available:
            raise Exception("Elasticsearch not available")
        
        # Build query
        must_clauses = [
            {
                "multi_match": {
                    "query": query,
                    "fields": ["content", "filename"],
                    "type": "best_fields"
                }
            }
        ]
        
        # Add filters
        filter_clauses = []
        if case_id:
            filter_clauses.append({"term": {"case_id": case_id}})
        if document_type:
            filter_clauses.append({"term": {"document_type": document_type}})
        
        search_body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses
                }
            },
            "size": limit,
            "_source": ["document_id", "filename", "document_type", "content", "metadata"],
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/{self.index_name}/_search",
            data=json.dumps(search_body).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            hits = []
            for hit in result.get('hits', {}).get('hits', []):
                doc = hit['_source']
                doc['score'] = hit['_score']
                doc['highlight'] = hit.get('highlight', {})
                hits.append(doc)
            
            return hits
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document by ID
        
        Args:
            document_id: Document identifier
            
        Returns:
            Document or None
        """
        if not self.available:
            return None
        
        try:
            req = urllib.request.Request(
                f"{self.base_url}/{self.index_name}/_doc/{document_id}"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('_source')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
    
    def get_case_documents(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Get all documents for a case
        
        Args:
            case_id: Case identifier
            
        Returns:
            List of documents
        """
        if not self.available:
            return []
        
        search_body = {
            "query": {
                "term": {"case_id": case_id}
            },
            "size": 1000
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/{self.index_name}/_search",
            data=json.dumps(search_body).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return [hit['_source'] for hit in result.get('hits', {}).get('hits', [])]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        if not self.available:
            return {"available": False}
        
        try:
            req = urllib.request.Request(f"{self.base_url}/{self.index_name}/_stats")
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                stats = result.get('_all', {}).get('primaries', {})
                
                return {
                    "available": True,
                    "document_count": stats.get('docs', {}).get('count', 0),
                    "size_in_bytes": stats.get('store', {}).get('size_in_bytes', 0)
                }
        except:
            return {"available": False, "error": "Failed to get stats"}


def test_elasticsearch_client():
    """Test Elasticsearch client"""
    print("🧪 Testing Elasticsearch Client...\n")
    
    # Initialize
    print("1. Connecting to Elasticsearch...")
    client = ElasticsearchClient()
    
    if not client.available:
        print("   ⚠️  Elasticsearch not available - start with: docker-compose up -d elasticsearch")
        return
    
    print("   ✅ Elasticsearch connected")
    
    # Store test document
    print("\n2. Storing test document...")
    doc_id = client.store_document(
        case_id="test_case",
        document_id="test_doc_001",
        filename="test_report.pdf",
        content="This is a financial report. Revenue was $100k. Profit margin 25%.",
        document_type="financial",
        metadata={"author": "Test", "year": 2024}
    )
    print(f"   ✅ Stored: {doc_id}")
    
    # Full-text search
    print("\n3. Full-text search...")
    results = client.full_text_search("revenue profit", case_id="test_case")
    print(f"   ✅ Found {len(results)} results")
    if results:
        print(f"   Top result: {results[0]['filename']} (score: {results[0]['score']:.2f})")
    
    # Get document
    print("\n4. Get document by ID...")
    doc = client.get_document("test_doc_001")
    if doc:
        print(f"   ✅ Retrieved: {doc['filename']}")
    
    # Get stats
    print("\n5. Index statistics...")
    stats = client.get_stats()
    print(f"   Documents: {stats.get('document_count', 0)}")
    print(f"   Size: {stats.get('size_in_bytes', 0)} bytes")
    
    print("\n✅ Elasticsearch tests complete!")


if __name__ == "__main__":
    test_elasticsearch_client()
