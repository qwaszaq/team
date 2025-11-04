"""
Analytical Team Configuration

Privacy and LLM settings for analytical agents
"""

import os
from typing import Dict, Optional


class AnalyticalConfig:
    """
    Configuration for Analytical Team
    
    Key Features:
    - Privacy mode (local LLM for sensitive data)
    - Configurable per agent
    - Environment-based configuration
    """
    
    # ============================================
    # LLM CONFIGURATION
    # ============================================
    
    # LLM Mode: "LOCAL", "CLOUD", "HYBRID"
    # - LOCAL: All processing on local machine (LM Studio)
    # - CLOUD: Use cloud APIs (OpenAI, Anthropic)
    # - HYBRID: Route based on data sensitivity
    LLM_MODE = os.getenv("ANALYTICAL_LLM_MODE", "LOCAL")
    
    # LM Studio Server Configuration
    LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
    LM_STUDIO_TIMEOUT = int(os.getenv("LM_STUDIO_TIMEOUT", "120"))
    
    # Model Configuration
    # Default: gpt-oss-20b (20B parameter model - excellent for analytical reasoning)
    LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "gpt-oss-20b")
    
    # Embedding Model (for Qdrant and document retrieval)
    # Jina v4 is EXCELLENT for analytical documents:
    # - Handles tables, charts, structured data
    # - Up to 8192 tokens (vs 512 for most models)
    # - Optimized for retrieval (search/similarity)
    # - Multilingual support
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "jinaai/jina-embeddings-v4-text-retrieval")
    
    # ============================================
    # PRIVACY SETTINGS
    # ============================================
    
    # Mark data as sensitive by default
    DEFAULT_SENSITIVITY = os.getenv("DATA_SENSITIVE_BY_DEFAULT", "true").lower() == "true"
    
    # Agents that ALWAYS use local LLM (even in HYBRID mode)
    ALWAYS_LOCAL_AGENTS = [
        "Elena Volkov",  # OSINT (sensitive investigations)
        "Marcus Chen",   # Financial (confidential data)
        "Adrian Kowalski"  # Legal (attorney-client privilege)
    ]
    
    # ============================================
    # SEARCH INFRASTRUCTURE
    # ============================================
    
    # Elasticsearch Configuration
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER", "elastic")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "changeme123")
    ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "analytical-documents")
    
    # Qdrant Configuration
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "analytical-team")
    
    # ============================================
    # PROJECT SETTINGS
    # ============================================
    
    PROJECT_ID = os.getenv("ANALYTICAL_PROJECT_ID", "destiny-analytical-team")
    
    # Database separation (same infrastructure, different project ID)
    POSTGRES_PROJECT_ID = PROJECT_ID
    NEO4J_PROJECT_ID = PROJECT_ID
    REDIS_PROJECT_ID = PROJECT_ID
    
    # ============================================
    # AGENT-SPECIFIC SETTINGS
    # ============================================
    
    AGENT_SETTINGS = {
        "Elena Volkov": {
            "llm_mode": "LOCAL",  # Always local for OSINT
            "max_tokens": 1500,
            "temperature": 0.7,
            "tools_enabled": True
        },
        "Marcus Chen": {
            "llm_mode": "LOCAL",  # Always local for financial
            "max_tokens": 2000,
            "temperature": 0.5,  # More conservative
            "tools_enabled": True
        },
        "Sofia Martinez": {
            "llm_mode": "HYBRID",  # Can use cloud for public market data
            "max_tokens": 1500,
            "temperature": 0.7,
            "tools_enabled": True
        },
        "Adrian Kowalski": {
            "llm_mode": "LOCAL",  # Always local for legal
            "max_tokens": 2000,
            "temperature": 0.6,
            "tools_enabled": True
        },
        "Maya Patel": {
            "llm_mode": "HYBRID",  # Statistical analysis can be flexible
            "max_tokens": 1500,
            "temperature": 0.5,
            "tools_enabled": True
        },
        "Lucas Rivera": {
            "llm_mode": "HYBRID",  # Report writing can be flexible
            "max_tokens": 2500,
            "temperature": 0.7,
            "tools_enabled": True
        },
        "Viktor Kovalenko": {
            "llm_mode": "LOCAL",  # Orchestrator sees all sensitive data
            "max_tokens": 1500,
            "temperature": 0.7,
            "tools_enabled": False
        },
        "Damian Rousseau": {
            "llm_mode": "LOCAL",  # Devil's advocate needs full context
            "max_tokens": 1500,
            "temperature": 0.8,  # More creative for alternatives
            "tools_enabled": False
        },
        "Alex Morgan": {
            "llm_mode": "LOCAL",  # Technical liaison handles sensitive docs
            "max_tokens": 1500,
            "temperature": 0.6,
            "tools_enabled": True
        }
    }
    
    @classmethod
    def get_agent_config(cls, agent_name: str) -> Dict:
        """Get configuration for specific agent"""
        return cls.AGENT_SETTINGS.get(
            agent_name,
            {
                "llm_mode": cls.LLM_MODE,
                "max_tokens": 1500,
                "temperature": 0.7,
                "tools_enabled": True
            }
        )
    
    @classmethod
    def is_sensitive_agent(cls, agent_name: str) -> bool:
        """Check if agent always uses local LLM"""
        return agent_name in cls.ALWAYS_LOCAL_AGENTS
    
    @classmethod
    def get_llm_mode(cls, agent_name: str, data_sensitive: bool = True) -> str:
        """
        Determine LLM mode for agent and data
        
        Args:
            agent_name: Name of agent
            data_sensitive: Whether data is sensitive
        
        Returns:
            "LOCAL" or "CLOUD"
        """
        agent_config = cls.get_agent_config(agent_name)
        agent_mode = agent_config.get("llm_mode", cls.LLM_MODE)
        
        # Always local for sensitive agents
        if cls.is_sensitive_agent(agent_name):
            return "LOCAL"
        
        # Agent-specific mode
        if agent_mode == "LOCAL":
            return "LOCAL"
        elif agent_mode == "CLOUD":
            return "CLOUD"
        elif agent_mode == "HYBRID":
            # Route based on data sensitivity
            return "LOCAL" if data_sensitive else "CLOUD"
        else:
            # Default to local for safety
            return "LOCAL"
    
    @classmethod
    def print_configuration(cls):
        """Print current configuration"""
        print("=" * 60)
        print("ANALYTICAL TEAM CONFIGURATION")
        print("=" * 60)
        
        print(f"\n🔒 PRIVACY MODE:")
        print(f"   LLM Mode: {cls.LLM_MODE}")
        print(f"   Sensitive by Default: {cls.DEFAULT_SENSITIVITY}")
        print(f"   Always Local Agents: {', '.join(cls.ALWAYS_LOCAL_AGENTS)}")
        
        print(f"\n🤖 LM STUDIO:")
        print(f"   Endpoint: {cls.LM_STUDIO_BASE_URL}")
        print(f"   Model: {cls.LM_STUDIO_MODEL or 'Auto-detect'}")
        print(f"   Timeout: {cls.LM_STUDIO_TIMEOUT}s")
        
        print(f"\n🔍 SEARCH INFRASTRUCTURE:")
        print(f"   Elasticsearch: {cls.ELASTICSEARCH_URL}")
        print(f"   Qdrant: {cls.QDRANT_URL}")
        
        print(f"\n📁 PROJECT:")
        print(f"   Project ID: {cls.PROJECT_ID}")
        
        print("\n" + "=" * 60)


# Quick test
if __name__ == "__main__":
    AnalyticalConfig.print_configuration()
    
    print("\nAgent-specific LLM routing:")
    agents = ["Elena Volkov", "Sofia Martinez", "Lucas Rivera"]
    
    for agent in agents:
        sensitive_mode = AnalyticalConfig.get_llm_mode(agent, data_sensitive=True)
        public_mode = AnalyticalConfig.get_llm_mode(agent, data_sensitive=False)
        
        print(f"\n{agent}:")
        print(f"  Sensitive data → {sensitive_mode}")
        print(f"  Public data → {public_mode}")
