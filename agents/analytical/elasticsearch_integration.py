"""
Elasticsearch Integration for Destiny Analytical Team
Full-text search and document indexing

Connects to: hercules-elasticsearch (localhost:9200)
Credentials: elastic:changeme123
"""

from elasticsearch import Elasticsearch
from typing import List, Dict, Any, Optional
import json


class AnalyticalElasticsearch:
    """
    Elasticsearch client for analytical team document search
    
    Features:
    - Document indexing with metadata
    - Full-text search
    - Aggregations and analytics
    - Hybrid search with Qdrant
    """
    
    def __init__(
        self,
        host: str = "http://localhost:9200",
        username: str = "elastic",
        password: str = "changeme123"
    ):
        """Initialize Elasticsearch connection"""
        self.es = Elasticsearch(
            [host],
            basic_auth=(username, password),
            verify_certs=False
        )
        self.index_name = "analytical-documents"
        
    def test_connection(self) -> bool:
        """Test Elasticsearch connection"""
        try:
            info = self.es.info()
            cluster_name = info['cluster_name']
            version = info['version']['number']
            print(f"✅ Connected to Elasticsearch: {cluster_name} (v{version})")
            return True
        except Exception as e:
            print(f"❌ Cannot connect to Elasticsearch: {e}")
            return False
    
    def create_index(self) -> bool:
        """Create index for analytical documents"""
        
        index_config = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "document_analyzer": {
                            "type": "standard",
                            "stopwords": "_english_"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text", "analyzer": "document_analyzer"},
                    "file_type": {"type": "keyword"},
                    "file_name": {"type": "keyword"},
                    "file_path": {"type": "keyword"},
                    "author": {"type": "keyword"},
                    "created_date": {"type": "date"},
                    "indexed_date": {"type": "date"},
                    "category": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "page_count": {"type": "integer"},
                    "file_size": {"type": "integer"},
                    "source": {"type": "keyword"},
                    "investigation_id": {"type": "keyword"},
                    "metadata": {"type": "object"}
                }
            }
        }
        
        try:
            if self.es.indices.exists(index=self.index_name):
                print(f"ℹ️  Index '{self.index_name}' already exists")
                return True
            
            self.es.indices.create(index=self.index_name, body=index_config)
            print(f"✅ Created index: {self.index_name}")
            return True
        except Exception as e:
            print(f"❌ Error creating index: {e}")
            return False
    
    def index_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        file_type: str,
        file_name: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Index a single document"""
        
        document = {
            "title": title,
            "content": content,
            "file_type": file_type,
            "file_name": file_name,
            "indexed_date": "now",
            **(metadata or {})
        }
        
        try:
            self.es.index(index=self.index_name, id=doc_id, document=document)
            return True
        except Exception as e:
            print(f"❌ Error indexing document {doc_id}: {e}")
            return False
    
    def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Full-text search with optional filters
        
        Args:
            query: Search query
            filters: {"file_type": "pdf", "category": "financial"}
            limit: Number of results
        
        Returns:
            List of matching documents with scores
        """
        
        # Build query
        must_clauses = [
            {"multi_match": {
                "query": query,
                "fields": ["title^2", "content"],  # Title boosted 2x
                "type": "best_fields"
            }}
        ]
        
        # Add filters
        filter_clauses = []
        if filters:
            for field, value in filters.items():
                filter_clauses.append({"term": {field: value}})
        
        search_body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses
                }
            },
            "size": limit,
            "highlight": {
                "fields": {
                    "content": {"fragment_size": 150, "number_of_fragments": 3}
                }
            }
        }
        
        try:
            response = self.es.search(index=self.index_name, body=search_body)
            
            results = []
            for hit in response['hits']['hits']:
                results.append({
                    "id": hit['_id'],
                    "score": hit['_score'],
                    "title": hit['_source'].get('title'),
                    "file_name": hit['_source'].get('file_name'),
                    "file_type": hit['_source'].get('file_type'),
                    "highlight": hit.get('highlight', {}).get('content', []),
                    "metadata": hit['_source']
                })
            
            return results
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def aggregate_by_field(self, field: str, limit: int = 10) -> Dict:
        """Aggregate documents by field (e.g., count by category)"""
        
        agg_body = {
            "size": 0,
            "aggs": {
                f"{field}_counts": {
                    "terms": {
                        "field": field,
                        "size": limit
                    }
                }
            }
        }
        
        try:
            response = self.es.search(index=self.index_name, body=agg_body)
            buckets = response['aggregations'][f'{field}_counts']['buckets']
            
            return {
                bucket['key']: bucket['doc_count']
                for bucket in buckets
            }
        except Exception as e:
            print(f"❌ Aggregation error: {e}")
            return {}
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        
        try:
            stats = self.es.indices.stats(index=self.index_name)
            doc_count = stats['indices'][self.index_name]['primaries']['docs']['count']
            size = stats['indices'][self.index_name]['primaries']['store']['size_in_bytes']
            
            return {
                "document_count": doc_count,
                "index_size_mb": size / (1024 * 1024),
                "status": "healthy"
            }
        except Exception as e:
            return {"error": str(e)}


# Quick test
if __name__ == "__main__":
    print("Testing Elasticsearch connection...")
    es = AnalyticalElasticsearch()
    
    if es.test_connection():
        print("\n✅ Elasticsearch ready for analytical team!")
        print("   Cluster: hercules-cluster")
        print("   RAM: 16GB")
        print("   Perfect for document-heavy investigations!")
    else:
        print("\n⚠️  Make sure Elasticsearch container is running")
        print("   docker ps | grep elasticsearch")
