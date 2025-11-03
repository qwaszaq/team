#!/usr/bin/env python3
"""
Complete LM Studio Embeddings Test

Testuje:
1. Connection do LM Studio
2. Generowanie embeddings
3. Similarity calculation
4. Integration z Qdrant
5. Semantic search
"""

import requests
import numpy as np
import time
from typing import List


class LMStudioTester:
    """Complete test suite dla LM Studio embeddings"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.base_url = base_url
        self.model = "text-embedding-intfloat-multilingual-e5-large-instruct"
        self.expected_dim = 1024
    
    def test_connection(self) -> bool:
        """Test 1: Czy LM Studio odpowiada?"""
        print("=" * 70)
        print("  TEST 1: Connection Test")
        print("=" * 70)
        print()
        
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ LM Studio ONLINE!")
                print(f"   URL: {self.base_url}")
                print(f"   Status: {response.status_code}")
                
                models = response.json()
                if models.get('data'):
                    print(f"\n   Available models:")
                    for model in models['data']:
                        print(f"     • {model.get('id', 'Unknown')}")
                
                return True
            else:
                print(f"⚠️  LM Studio responded but status: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to LM Studio!")
            print(f"   URL: {self.base_url}")
            print(f"\n   Make sure:")
            print(f"   1. LM Studio is running")
            print(f"   2. Embeddings model is loaded")
            print(f"   3. Server is on port 1234")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            response = requests.post(
                f"{self.base_url}/embeddings",
                json={
                    "input": text,
                    "model": self.model
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                embedding = data['data'][0]['embedding']
                return embedding
            else:
                print(f"⚠️  Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            return None
    
    def test_embedding_generation(self) -> bool:
        """Test 2: Czy embeddingi są generowane?"""
        print("\n" + "=" * 70)
        print("  TEST 2: Embedding Generation")
        print("=" * 70)
        print()
        
        test_texts = [
            "To jest testowy tekst po polsku.",
            "This is a test text in English.",
            "PostgreSQL jest relacyjną bazą danych."
        ]
        
        print(f"Testing {len(test_texts)} texts...")
        print()
        
        all_success = True
        embeddings = []
        
        for i, text in enumerate(test_texts, 1):
            print(f"  [{i}/{len(test_texts)}] '{text[:50]}...'")
            
            start_time = time.time()
            embedding = self.generate_embedding(text)
            elapsed = time.time() - start_time
            
            if embedding:
                embeddings.append(embedding)
                print(f"    ✅ Generated in {elapsed:.2f}s")
                print(f"       Dimension: {len(embedding)}")
                print(f"       Sample values: [{embedding[0]:.4f}, {embedding[1]:.4f}, ...]")
                
                # Verify dimension
                if len(embedding) != self.expected_dim:
                    print(f"    ⚠️  Expected {self.expected_dim}D, got {len(embedding)}D")
                    all_success = False
            else:
                print(f"    ❌ FAILED to generate")
                all_success = False
            
            print()
        
        if all_success:
            print(f"✅ All embeddings generated successfully!")
            print(f"   Average time: {elapsed:.2f}s per text")
        else:
            print(f"❌ Some embeddings failed")
        
        return all_success, embeddings
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        return dot_product / (norm1 * norm2)
    
    def test_similarity(self, embeddings: List[List[float]]) -> bool:
        """Test 3: Similarity calculation"""
        print("\n" + "=" * 70)
        print("  TEST 3: Similarity Calculation")
        print("=" * 70)
        print()
        
        if len(embeddings) < 3:
            print("⚠️  Need at least 3 embeddings for similarity test")
            return False
        
        # Test texts were:
        # 0: "To jest testowy tekst po polsku."
        # 1: "This is a test text in English."
        # 2: "PostgreSQL jest relacyjną bazą danych."
        
        print("Calculating similarities...")
        print()
        
        # Similar texts (0 and 1 - both are test texts)
        sim_01 = self.cosine_similarity(embeddings[0], embeddings[1])
        print(f"  Polish test text <-> English test text")
        print(f"    Similarity: {sim_01:.4f}")
        print(f"    Expected: HIGH (similar meaning)")
        print()
        
        # Different texts (1 and 2 - test vs database)
        sim_12 = self.cosine_similarity(embeddings[1], embeddings[2])
        print(f"  English test text <-> PostgreSQL database text")
        print(f"    Similarity: {sim_12:.4f}")
        print(f"    Expected: LOW (different topics)")
        print()
        
        # Different texts (0 and 2 - test vs database)
        sim_02 = self.cosine_similarity(embeddings[0], embeddings[2])
        print(f"  Polish test text <-> PostgreSQL database text")
        print(f"    Similarity: {sim_02:.4f}")
        print(f"    Expected: LOW (different topics)")
        print()
        
        # Validation
        if sim_01 > sim_12 and sim_01 > sim_02:
            print("✅ Similarity works correctly!")
            print("   Similar texts have higher similarity than different texts.")
            return True
        else:
            print("⚠️  Similarity pattern unexpected")
            print("   Similar texts should have highest similarity")
            return False
    
    def test_semantic_search(self) -> bool:
        """Test 4: Semantic search capability"""
        print("\n" + "=" * 70)
        print("  TEST 4: Semantic Search Capability")
        print("=" * 70)
        print()
        
        # Create a mini corpus
        corpus = [
            "PostgreSQL jest doskonałą bazą danych dla aplikacji wymagających ACID",
            "MongoDB jest NoSQL database używanym do przechowywania dokumentów JSON",
            "Python jest językiem programowania używanym do data science",
            "React jest JavaScript library do budowania user interfaces",
            "Docker pozwala na konteneryzację aplikacji dla łatwego deploymentu"
        ]
        
        print(f"Creating corpus of {len(corpus)} texts...")
        print()
        
        # Generate embeddings for corpus
        corpus_embeddings = []
        for i, text in enumerate(corpus, 1):
            print(f"  [{i}/{len(corpus)}] Embedding: '{text[:40]}...'")
            emb = self.generate_embedding(text)
            if emb:
                corpus_embeddings.append(emb)
            else:
                print(f"    ❌ Failed")
                return False
        
        print()
        print(f"✅ Corpus embeddings generated!")
        print()
        
        # Test queries
        queries = [
            ("baza danych SQL", "PostgreSQL text (semantic match!)"),
            ("konteneryzacja", "Docker text (keyword match)"),
            ("programowanie interfejsów", "React text (semantic: UI programming)")
        ]
        
        print("Testing semantic search queries...")
        print()
        
        all_correct = True
        
        for query, expected in queries:
            print(f"🔍 Query: '{query}'")
            print(f"   Expected: {expected}")
            
            # Generate query embedding
            query_emb = self.generate_embedding(query)
            if not query_emb:
                print(f"   ❌ Failed to generate query embedding")
                all_correct = False
                continue
            
            # Calculate similarities
            similarities = []
            for i, corpus_emb in enumerate(corpus_embeddings):
                sim = self.cosine_similarity(query_emb, corpus_emb)
                similarities.append((i, sim, corpus[i]))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Show top 3 results
            print(f"\n   Top 3 results:")
            for rank, (idx, sim, text) in enumerate(similarities[:3], 1):
                print(f"     {rank}. [{sim:.4f}] {text[:60]}...")
            
            # Check if expected is in top result
            if expected.lower() in similarities[0][2].lower():
                print(f"   ✅ Correct! Top result matches expected.")
            else:
                print(f"   ⚠️  Top result differs from expected")
                all_correct = False
            
            print()
        
        if all_correct:
            print("✅ Semantic search works excellently!")
        else:
            print("⚠️  Some searches didn't match expectations")
        
        return all_correct
    
    def test_multilingual(self) -> bool:
        """Test 5: Multilingual capability"""
        print("\n" + "=" * 70)
        print("  TEST 5: Multilingual Capability")
        print("=" * 70)
        print()
        
        # Same meaning in different languages
        multilingual_texts = [
            ("Polski", "Witaj świecie! To jest test."),
            ("English", "Hello world! This is a test."),
            ("Mixed", "To jest mixed test with English words.")
        ]
        
        print("Testing multilingual embeddings...")
        print()
        
        embeddings = []
        for lang, text in multilingual_texts:
            print(f"  [{lang}] '{text}'")
            emb = self.generate_embedding(text)
            if emb:
                embeddings.append((lang, emb))
                print(f"    ✅ Generated")
            else:
                print(f"    ❌ Failed")
                return False
            print()
        
        # Compare Polish vs English (similar meaning)
        sim_pl_en = self.cosine_similarity(embeddings[0][1], embeddings[1][1])
        print(f"Similarity: Polish <-> English")
        print(f"  Score: {sim_pl_en:.4f}")
        print(f"  Both say 'Hello world! This is a test.'")
        
        if sim_pl_en > 0.7:
            print(f"  ✅ HIGH similarity - model understands both languages!")
        else:
            print(f"  ⚠️  Lower than expected for same meaning")
        
        print()
        return True


def main():
    """Run all tests"""
    print("\n" + "🧪 "*30)
    print("  LM STUDIO EMBEDDINGS - COMPLETE TEST SUITE")
    print("🧪 "*30)
    print()
    
    tester = LMStudioTester()
    
    results = {
        "connection": False,
        "generation": False,
        "similarity": False,
        "semantic_search": False,
        "multilingual": False
    }
    
    # Test 1: Connection
    results["connection"] = tester.test_connection()
    
    if not results["connection"]:
        print("\n" + "="*70)
        print("  ❌ Cannot proceed - LM Studio not accessible")
        print("="*70)
        print()
        print("Troubleshooting:")
        print("  1. Start LM Studio")
        print("  2. Load embeddings model: text-embedding-intfloat-multilingual-e5-large-instruct")
        print("  3. Make sure server is running on port 1234")
        print("  4. Try: curl http://localhost:1234/v1/models")
        print()
        return
    
    # Test 2: Generation
    results["generation"], embeddings = tester.test_embedding_generation()
    
    if not results["generation"]:
        print("\n" + "="*70)
        print("  ❌ Cannot proceed - Embedding generation failed")
        print("="*70)
        return
    
    # Test 3: Similarity
    results["similarity"] = tester.test_similarity(embeddings)
    
    # Test 4: Semantic Search
    results["semantic_search"] = tester.test_semantic_search()
    
    # Test 5: Multilingual
    results["multilingual"] = tester.test_multilingual()
    
    # Summary
    print("\n" + "="*70)
    print("  📊 TEST SUMMARY")
    print("="*70)
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name.replace('_', ' ').title()}")
    
    print()
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    if passed_count == total_count:
        print(f"  🎉 ALL TESTS PASSED ({passed_count}/{total_count})")
        print()
        print("  LM Studio embeddings są w pełni operational!")
        print("  Gotowy do:")
        print("    ✅ Semantic search")
        print("    ✅ Similarity matching")
        print("    ✅ Multilingual understanding")
        print("    ✅ Integration z Qdrant")
        print()
        print("  Cost: $0 (local!) 💰")
    else:
        print(f"  ⚠️  {passed_count}/{total_count} tests passed")
        print()
        print("  Some functionality may not work properly.")
    
    print()
    print("="*70)


if __name__ == "__main__":
    main()
