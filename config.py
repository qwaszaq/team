"""
Configuration Management
Team Destiny
2025-11-05
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()


class Config:
    """System configuration"""
    
    # ============================================
    # CLAUDE API
    # ============================================
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4.5-20241022")
    
    # ============================================
    # LMSTUDIO
    # ============================================
    LMSTUDIO_HOST: str = os.getenv("LMSTUDIO_HOST", "192.168.200.226")
    LMSTUDIO_PORT: int = int(os.getenv("LMSTUDIO_PORT", "1234"))
    LMSTUDIO_LLM_MODEL: str = os.getenv("LMSTUDIO_LLM_MODEL", "openai/gpt-oss-20b")
    LMSTUDIO_EMBEDDING_MODEL: str = os.getenv(
        "LMSTUDIO_EMBEDDING_MODEL",
        "text-embedding-multilingual-e5-large-instruct"
    )
    
    @property
    def LMSTUDIO_BASE_URL(self) -> str:
        return f"http://{self.LMSTUDIO_HOST}:{self.LMSTUDIO_PORT}/v1"
    
    # ============================================
    # DATABASES
    # ============================================
    
    # PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "destiny_analytical")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "destiny")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "destiny_dev_2024")
    
    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "destiny_embeddings")
    
    # Elasticsearch
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_INDEX: str = os.getenv("ELASTICSEARCH_INDEX", "destiny_documents")
    
    # Neo4j
    NEO4J_HOST: str = os.getenv("NEO4J_HOST", "localhost")
    NEO4J_HTTP_PORT: int = int(os.getenv("NEO4J_HTTP_PORT", "7474"))
    NEO4J_BOLT_PORT: int = int(os.getenv("NEO4J_BOLT_PORT", "7687"))
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "destiny_dev_2024")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # ============================================
    # SYSTEM SETTINGS
    # ============================================
    SUPERVISION_MODE: str = os.getenv("SUPERVISION_MODE", "supervised")
    VECTOR_THRESHOLD: int = int(os.getenv("VECTOR_THRESHOLD", "100000"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "120"))
    
    # ============================================
    # MONITORING & LOGGING
    # ============================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/destiny.log")
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9090"))
    
    # ============================================
    # FEATURE FLAGS
    # ============================================
    ENABLE_CLAUDE_SUPERVISION: bool = os.getenv("ENABLE_CLAUDE_SUPERVISION", "false").lower() == "true"
    ENABLE_POSTGRES: bool = os.getenv("ENABLE_POSTGRES", "true").lower() == "true"
    ENABLE_QDRANT: bool = os.getenv("ENABLE_QDRANT", "false").lower() == "true"
    ENABLE_ELASTICSEARCH: bool = os.getenv("ENABLE_ELASTICSEARCH", "false").lower() == "true"
    ENABLE_NEO4J: bool = os.getenv("ENABLE_NEO4J", "false").lower() == "true"
    
    # ============================================
    # ENVIRONMENT
    # ============================================
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return cls.ENVIRONMENT == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development"""
        return cls.ENVIRONMENT == "development"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        issues = []
        
        # Check Claude API key if supervision enabled
        if cls.ENABLE_CLAUDE_SUPERVISION and not cls.ANTHROPIC_API_KEY:
            issues.append("ANTHROPIC_API_KEY required when ENABLE_CLAUDE_SUPERVISION=true")
        
        # Check LMStudio
        if not cls.LMSTUDIO_HOST:
            issues.append("LMSTUDIO_HOST required")
        
        # Check at least one database enabled
        if not any([cls.ENABLE_POSTGRES, cls.ENABLE_QDRANT, cls.ENABLE_ELASTICSEARCH, cls.ENABLE_NEO4J]):
            issues.append("At least one database must be enabled")
        
        if issues:
            print("⚠️  Configuration Issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print configuration summary"""
        print("="*70)
        print("DESTINY ANALYTICAL SYSTEM - CONFIGURATION")
        print("="*70)
        print(f"\nEnvironment: {cls.ENVIRONMENT}")
        print(f"Debug: {cls.DEBUG}")
        
        print("\nLMStudio:")
        print(f"  Host: {cls.LMSTUDIO_HOST}:{cls.LMSTUDIO_PORT}")
        print(f"  LLM: {cls.LMSTUDIO_LLM_MODEL}")
        print(f"  Embeddings: {cls.LMSTUDIO_EMBEDDING_MODEL}")
        
        print("\nSupervision:")
        print(f"  Mode: {cls.SUPERVISION_MODE}")
        print(f"  Claude API: {'✅ Configured' if cls.ANTHROPIC_API_KEY else '❌ Not configured'}")
        print(f"  Enabled: {cls.ENABLE_CLAUDE_SUPERVISION}")
        
        print("\nDatabases:")
        print(f"  PostgreSQL: {'✅ Enabled' if cls.ENABLE_POSTGRES else '⏸️  Disabled'}")
        print(f"  Qdrant: {'✅ Enabled' if cls.ENABLE_QDRANT else '⏸️  Disabled'}")
        print(f"  Elasticsearch: {'✅ Enabled' if cls.ENABLE_ELASTICSEARCH else '⏸️  Disabled'}")
        print(f"  Neo4j: {'✅ Enabled' if cls.ENABLE_NEO4J else '⏸️  Disabled'}")
        
        print("\nPerformance:")
        print(f"  Vector Threshold: {cls.VECTOR_THRESHOLD:,}")
        print(f"  Max Workers: {cls.MAX_WORKERS}")
        print(f"  Batch Size: {cls.BATCH_SIZE}")
        
        print("\n" + "="*70)


# Create global config instance
config = Config()


if __name__ == "__main__":
    # Test configuration
    config.print_config()
    print("\nValidating configuration...")
    if config.validate():
        print("✅ Configuration valid!")
    else:
        print("❌ Configuration has issues")
