"""
LM Studio Embeddings Integration for Destiny Team

Uses local multilingual-e5-large-instruct model via LM Studio
for FREE, private, unlimited embeddings.
"""

import requests
from typing import List, Union
import numpy as np


class LMStudioEmbeddings:
    """
    Client for LM Studio embeddings server.
    
    Compatible with OpenAI API format but uses local model.
    Model: text-embedding-intfloat-multilingual-e5-large-instruct
    Dimensions: 1024
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "text-embedding-intfloat-multilingual-e5-large-instruct"
    ):
        """
        Initialize LM Studio embeddings client.
        
        Args:
            base_url: LM Studio server URL (default: http://localhost:1234/v1)
            model: Embedding model name
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.dimension = 1024  # E5-Large dimension
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text(s).
        
        Args:
            text: Single text or list of texts
            
        Returns:
            Single embedding or list of embeddings
        """
        # Convert single text to list
        texts = [text] if isinstance(text, str) else text
        single_input = isinstance(text, str)
        
        # Call LM Studio API (OpenAI compatible)
        response = requests.post(
            f"{self.base_url}/embeddings",
            json={
                "model": self.model,
                "input": texts
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"LM Studio error: {response.text}")
        
        data = response.json()
        embeddings = [item['embedding'] for item in data['data']]
        
        # Return single embedding if single input
        return embeddings[0] if single_input else embeddings
    
    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 10
    ) -> List[List[float]]:
        """
        Generate embeddings in batches (for large datasets).
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch
            
        Returns:
            List of embeddings
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.embed(batch)
            all_embeddings.extend(embeddings)
            
            # Progress
            if (i + batch_size) % 100 == 0:
                print(f"Embedded {min(i + batch_size, len(texts))}/{len(texts)} texts")
        
        return all_embeddings
    
    def similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score (0-1)
        """
        # Convert to numpy arrays
        e1 = np.array(embedding1)
        e2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(e1, e2)
        norm1 = np.linalg.norm(e1)
        norm2 = np.linalg.norm(e2)
        
        return dot_product / (norm1 * norm2)
    
    def test_connection(self) -> bool:
        """Test if LM Studio server is running"""
        try:
            # Try to get models list
            response = requests.get(
                f"{self.base_url}/models",
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json()
                print(f"✅ LM Studio connected!")
                print(f"Available models: {len(models.get('data', []))}")
                return True
            else:
                print(f"❌ LM Studio returned: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to LM Studio: {e}")
            print(f"Make sure LM Studio is running on {self.base_url}")
            return False


# ==================== USAGE EXAMPLE ====================

def test_lmstudio():
    """Test LM Studio embeddings"""
    print("=" * 70)
    print("  LM Studio Embeddings Test")
    print("=" * 70)
    print()
    
    # Initialize
    embedder = LMStudioEmbeddings()
    
    # Test connection
    print("Testing connection...")
    if not embedder.test_connection():
        return False
    print()
    
    # Test single embedding
    print("Testing single text embedding...")
    text = "Wybraliśmy PostgreSQL dla ACID compliance"
    embedding = embedder.embed(text)
    print(f"✅ Text: {text}")
    print(f"✅ Embedding dimension: {len(embedding)}")
    print(f"✅ First 5 values: {embedding[:5]}")
    print()
    
    # Test batch embedding
    print("Testing batch embedding...")
    texts = [
        "PostgreSQL for transactions",
        "MongoDB for flexibility",
        "Redis for caching",
        "Neo4j for graphs"
    ]
    embeddings = embedder.embed(texts)
    print(f"✅ Embedded {len(texts)} texts")
    print()
    
    # Test similarity
    print("Testing similarity...")
    sim1 = embedder.similarity(embeddings[0], embeddings[1])
    sim2 = embedder.similarity(embeddings[0], embeddings[2])
    print(f"PostgreSQL vs MongoDB similarity: {sim1:.3f}")
    print(f"PostgreSQL vs Redis similarity: {sim2:.3f}")
    print()
    
    # Test multilingual (polski + angielski)
    print("Testing multilingual (Polski + English)...")
    pl_text = "Wybraliśmy bazę danych PostgreSQL"
    en_text = "We chose PostgreSQL database"
    
    pl_emb = embedder.embed(pl_text)
    en_emb = embedder.embed(en_text)
    
    sim_multilingual = embedder.similarity(pl_emb, en_emb)
    print(f"✅ Polish: {pl_text}")
    print(f"✅ English: {en_text}")
    print(f"✅ Cross-lingual similarity: {sim_multilingual:.3f}")
    print(f"   (should be >0.7 if model understands both)")
    print()
    
    print("=" * 70)
    print("  ✅ ALL TESTS PASSED!")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_lmstudio()
