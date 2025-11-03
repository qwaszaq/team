"""
Redis Caching Layer for Destiny Team

Ultra-fast caching for frequently accessed data, reducing load on
PostgreSQL, Neo4j, and Qdrant.
"""

import redis
import json
import pickle
from typing import Any, Optional, List, Dict
from datetime import timedelta


class RedisCache:
    """
    Redis caching layer for multi-agent system.
    
    Provides sub-millisecond access to frequently used data.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        prefix: str = "destiny:"
    ):
        """
        Initialize Redis cache.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number (0-15)
            prefix: Key prefix for namespacing
        """
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False  # We'll handle encoding
        )
        self.prefix = prefix
    
    def _make_key(self, key: str) -> str:
        """Create prefixed key"""
        return f"{self.prefix}{key}"
    
    # ==================== BASIC OPERATIONS ====================
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        full_key = self._make_key(key)
        value = self.client.get(full_key)
        
        if value is None:
            return None
        
        try:
            # Try JSON first (for simple types)
            return json.loads(value)
        except:
            # Fall back to pickle (for complex objects)
            return pickle.loads(value)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = no expiration)
            
        Returns:
            True if successful
        """
        full_key = self._make_key(key)
        
        # Serialize value
        try:
            # Try JSON first (faster, more readable)
            serialized = json.dumps(value)
        except:
            # Fall back to pickle (for complex objects)
            serialized = pickle.dumps(value)
        
        if ttl:
            return self.client.setex(full_key, ttl, serialized)
        else:
            return self.client.set(full_key, serialized)
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        full_key = self._make_key(key)
        return self.client.delete(full_key) > 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        full_key = self._make_key(key)
        return self.client.exists(full_key) > 0
    
    # ==================== SEARCH RESULT CACHING ====================
    
    def cache_search_results(
        self,
        query: str,
        project_id: str,
        results: List[Dict[str, Any]],
        ttl: int = 300  # 5 minutes default
    ) -> bool:
        """
        Cache search results.
        
        Args:
            query: Search query
            project_id: Project ID
            results: Search results
            ttl: Cache duration in seconds
        """
        # Create cache key from query + project
        import hashlib
        query_hash = hashlib.md5(
            f"{project_id}:{query}".encode()
        ).hexdigest()
        
        key = f"search:{query_hash}"
        return self.set(key, results, ttl=ttl)
    
    def get_cached_search(
        self,
        query: str,
        project_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results"""
        import hashlib
        query_hash = hashlib.md5(
            f"{project_id}:{query}".encode()
        ).hexdigest()
        
        key = f"search:{query_hash}"
        return self.get(key)
    
    # ==================== AGENT STATE CACHING ====================
    
    def cache_agent_state(
        self,
        agent_name: str,
        project_id: str,
        state: Dict[str, Any],
        ttl: int = 3600  # 1 hour
    ) -> bool:
        """Cache agent's current state"""
        key = f"agent_state:{project_id}:{agent_name}"
        return self.set(key, state, ttl=ttl)
    
    def get_agent_state(
        self,
        agent_name: str,
        project_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached agent state"""
        key = f"agent_state:{project_id}:{agent_name}"
        return self.get(key)
    
    # ==================== HOT MEMORY (Recent Messages) ====================
    
    def add_to_hot_memory(
        self,
        project_id: str,
        message: Dict[str, Any],
        max_size: int = 10
    ) -> bool:
        """
        Add message to hot memory (FIFO queue).
        
        Hot memory = last N messages for instant access.
        """
        key = f"hot_memory:{project_id}"
        
        # Add to list (left push)
        self.client.lpush(
            self._make_key(key),
            json.dumps(message)
        )
        
        # Trim to max size
        self.client.ltrim(
            self._make_key(key),
            0,
            max_size - 1
        )
        
        return True
    
    def get_hot_memory(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Get all messages from hot memory"""
        key = f"hot_memory:{project_id}"
        
        messages = self.client.lrange(
            self._make_key(key),
            0,
            -1
        )
        
        return [json.loads(msg) for msg in messages]
    
    # ==================== ACTIVE PROJECTS ====================
    
    def mark_project_active(
        self,
        project_id: str,
        ttl: int = 86400  # 24 hours
    ) -> bool:
        """Mark project as recently active"""
        key = f"active_project:{project_id}"
        return self.set(key, {"last_active": "now"}, ttl=ttl)
    
    def get_active_projects(self) -> List[str]:
        """Get list of recently active projects"""
        pattern = self._make_key("active_project:*")
        keys = self.client.keys(pattern)
        
        # Extract project IDs
        prefix_len = len(self._make_key("active_project:"))
        return [
            key.decode('utf-8')[prefix_len:]
            for key in keys
        ]
    
    # ==================== STATISTICS ====================
    
    def increment_stat(
        self,
        stat_name: str,
        amount: int = 1
    ) -> int:
        """Increment a counter"""
        key = f"stat:{stat_name}"
        return self.client.incrby(self._make_key(key), amount)
    
    def get_stat(self, stat_name: str) -> int:
        """Get counter value"""
        key = f"stat:{stat_name}"
        value = self.client.get(self._make_key(key))
        return int(value) if value else 0
    
    # ==================== SESSION MANAGEMENT ====================
    
    def create_session(
        self,
        session_id: str,
        data: Dict[str, Any],
        ttl: int = 3600
    ) -> bool:
        """Create a session"""
        key = f"session:{session_id}"
        return self.set(key, data, ttl=ttl)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        key = f"session:{session_id}"
        return self.get(key)
    
    def update_session(
        self,
        session_id: str,
        data: Dict[str, Any]
    ) -> bool:
        """Update session (preserves TTL)"""
        key = f"session:{session_id}"
        full_key = self._make_key(key)
        
        # Get current TTL
        ttl = self.client.ttl(full_key)
        if ttl < 0:
            ttl = 3600  # Default if no TTL
        
        return self.set(key, data, ttl=ttl)
    
    # ==================== UTILITIES ====================
    
    def clear_project_cache(self, project_id: str) -> int:
        """Clear all cached data for a project"""
        patterns = [
            f"search:*{project_id}*",
            f"agent_state:{project_id}:*",
            f"hot_memory:{project_id}",
            f"active_project:{project_id}"
        ]
        
        deleted = 0
        for pattern in patterns:
            keys = self.client.keys(self._make_key(pattern))
            if keys:
                deleted += self.client.delete(*keys)
        
        return deleted
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get Redis cache statistics"""
        info = self.client.info()
        
        return {
            "used_memory": info.get('used_memory_human'),
            "connected_clients": info.get('connected_clients'),
            "total_keys": self.client.dbsize(),
            "hit_rate": self._calculate_hit_rate(info)
        }
    
    def _calculate_hit_rate(self, info: Dict) -> float:
        """Calculate cache hit rate"""
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        if hits + misses == 0:
            return 0.0
        
        return hits / (hits + misses) * 100
    
    def test_connection(self) -> bool:
        """Test Redis connection"""
        try:
            self.client.ping()
            print(f"✅ Redis connected at {self.client.connection_pool.connection_kwargs['host']}:{self.client.connection_pool.connection_kwargs['port']}")
            
            # Show info
            info = self.client.info()
            print(f"Redis version: {info.get('redis_version')}")
            print(f"Used memory: {info.get('used_memory_human')}")
            print(f"Total keys: {self.client.dbsize()}")
            
            return True
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            return False
    
    def close(self):
        """Close Redis connection"""
        self.client.close()


# ==================== EXAMPLE ====================

def test_redis():
    """Test Redis cache"""
    print("=" * 70)
    print("  Redis Cache Test")
    print("=" * 70)
    print()
    
    # Initialize
    cache = RedisCache(host="localhost", port=6379)
    
    # Test connection
    if not cache.test_connection():
        return False
    print()
    
    # Test basic operations
    print("Testing basic operations...")
    cache.set("test_key", {"value": "test"}, ttl=60)
    result = cache.get("test_key")
    print(f"✅ Set and get: {result}")
    print()
    
    # Test hot memory
    print("Testing hot memory...")
    for i in range(5):
        cache.add_to_hot_memory(
            "test_project",
            {"message": f"Message {i}"}
        )
    
    hot = cache.get_hot_memory("test_project")
    print(f"✅ Hot memory: {len(hot)} messages")
    print()
    
    # Test search caching
    print("Testing search cache...")
    query = "test query"
    results = [{"result": 1}, {"result": 2}]
    
    cache.cache_search_results(query, "test_project", results)
    cached = cache.get_cached_search(query, "test_project")
    print(f"✅ Cached search results: {len(cached)} items")
    print()
    
    # Stats
    print("Cache statistics:")
    stats = cache.get_cache_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 70)
    print("  ✅ Redis Tests Complete!")
    print("=" * 70)
    
    cache.close()
    return True


if __name__ == "__main__":
    test_redis()
