#!/usr/bin/env python3
"""
Test LMStudio and Embedding Models
Aleksander Nowak - Orchestrator
2025-11-05
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# Import our existing embedding client
from lmstudio_embeddings import LMStudioEmbeddings

# Test Local LLM
async def test_local_llm():
    """Test LMStudio local LLM capabilities"""
    print("\n" + "="*60)
    print("🧪 TESTING LMSTUDIO LOCAL LLM")
    print("="*60)
    
    import aiohttp
    
    # Test cases for local LLM
    test_cases = [
        {
            "name": "Simple completion",
            "prompt": "What is the capital of France?",
            "expected_quality": "factual accuracy"
        },
        {
            "name": "Document analysis",
            "prompt": """Analyze this financial statement excerpt:
            'Revenue increased by 23% year-over-year to $4.2M, driven primarily by 
            new customer acquisitions in Q3. Operating expenses rose by 18%, 
            resulting in improved margins of 32%.'
            
            Provide: 1) Key findings 2) Red flags 3) Further investigation areas""",
            "expected_quality": "analytical depth"
        },
        {
            "name": "Multi-step reasoning",
            "prompt": """A company transferred $500k to Account A, which then sent 
            $200k to Account B and $300k to Account C. Account B sent $150k to 
            Account D. What is the total in Account D and what percentage of the 
            original amount ended up there?""",
            "expected_quality": "calculation accuracy"
        }
    ]
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        for test in test_cases:
            print(f"\n📝 Test: {test['name']}")
            print(f"Prompt: {test['prompt'][:100]}...")
            
            start_time = time.time()
            
            try:
                # Call LMStudio API
                async with session.post(
                    "http://localhost:1234/v1/chat/completions",
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": test['prompt']}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        response = data['choices'][0]['message']['content']
                        elapsed = time.time() - start_time
                        
                        result = {
                            "test": test['name'],
                            "success": True,
                            "response": response,
                            "time": elapsed,
                            "quality_check": test['expected_quality']
                        }
                        
                        print(f"✅ Success! Time: {elapsed:.2f}s")
                        print(f"Response preview: {response[:200]}...")
                    else:
                        result = {
                            "test": test['name'],
                            "success": False,
                            "error": f"HTTP {resp.status}",
                            "time": 0
                        }
                        print(f"❌ Failed: HTTP {resp.status}")
                        
            except Exception as e:
                result = {
                    "test": test['name'],
                    "success": False,
                    "error": str(e),
                    "time": 0
                }
                print(f"❌ Error: {str(e)}")
                print("\n⚠️  Is LMStudio running on http://localhost:1234?")
                
            results.append(result)
    
    return results

# Test Embeddings
async def test_embeddings():
    """Test both embedding models"""
    print("\n" + "="*60)
    print("🧪 TESTING EMBEDDING MODELS")
    print("="*60)
    
    # Test documents
    test_documents = [
        {
            "type": "general",
            "text": "The company's strategic vision focuses on sustainable growth through innovation and customer satisfaction."
        },
        {
            "type": "financial",
            "text": "Q3 revenue: $4.2M (+23% YoY), EBITDA margin 32%, cash flow positive for 6 consecutive quarters."
        },
        {
            "type": "legal",
            "text": "Pursuant to Section 4.2 of the agreement, the party of the first part shall indemnify the party of the second part."
        },
        {
            "type": "technical",
            "text": "The API utilizes REST principles with OAuth2 authentication and returns JSON-formatted responses."
        }
    ]
    
    # Test similarity queries
    queries = [
        "financial performance and profitability",
        "legal obligations and contracts",
        "technology and software development",
        "business strategy and growth"
    ]
    
    results = {
        "e5-large": {"embeddings": [], "similarities": []},
        "jina": {"embeddings": [], "similarities": []}
    }
    
    try:
        # Test E5-Large model
        print("\n📊 Testing E5-Large Multilingual Model (1024 dims)")
        e5_client = LMStudioEmbeddings(
            base_url="http://localhost:1234/v1",
            model="text-embedding-intfloat-multilingual-e5-large-instruct"
        )
        
        # Generate embeddings
        e5_embeddings = []
        for doc in test_documents:
            print(f"  Embedding {doc['type']} document...")
            start_time = time.time()
            embedding = e5_client.embed(doc['text'])
            elapsed = time.time() - start_time
            
            e5_embeddings.append({
                "type": doc['type'],
                "embedding": embedding,
                "dims": len(embedding),
                "time": elapsed
            })
            print(f"    ✅ Done in {elapsed:.3f}s, dims: {len(embedding)}")
        
        results["e5-large"]["embeddings"] = e5_embeddings
        
        # Test similarity search
        print("\n  Testing semantic similarity:")
        for query in queries:
            query_embedding = e5_client.embed(query)
            similarities = []
            
            for i, doc_emb in enumerate(e5_embeddings):
                # Cosine similarity
                similarity = np.dot(query_embedding, doc_emb['embedding']) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb['embedding'])
                )
                similarities.append({
                    "document": test_documents[i]['type'],
                    "similarity": float(similarity)
                })
            
            # Sort by similarity
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            results["e5-large"]["similarities"].append({
                "query": query,
                "results": similarities
            })
            
            print(f"    Query: '{query}'")
            print(f"      Best match: {similarities[0]['document']} ({similarities[0]['similarity']:.3f})")
        
    except Exception as e:
        print(f"❌ E5-Large test failed: {str(e)}")
        results["e5-large"]["error"] = str(e)
    
    try:
        # Test Jina model
        print("\n📊 Testing Jina Embeddings Model (768 dims)")
        jina_client = LMStudioEmbeddings(
            base_url="http://localhost:1234/v1",
            model="jina-embeddings-v3"
        )
        
        # Generate embeddings
        jina_embeddings = []
        for doc in test_documents:
            print(f"  Embedding {doc['type']} document...")
            start_time = time.time()
            embedding = jina_client.embed(doc['text'])
            elapsed = time.time() - start_time
            
            jina_embeddings.append({
                "type": doc['type'],
                "embedding": embedding,
                "dims": len(embedding),
                "time": elapsed
            })
            print(f"    ✅ Done in {elapsed:.3f}s, dims: {len(embedding)}")
        
        results["jina"]["embeddings"] = jina_embeddings
        
        # Test similarity search
        print("\n  Testing semantic similarity:")
        for query in queries:
            query_embedding = jina_client.embed(query)
            similarities = []
            
            for i, doc_emb in enumerate(jina_embeddings):
                # Cosine similarity
                similarity = np.dot(query_embedding, doc_emb['embedding']) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb['embedding'])
                )
                similarities.append({
                    "document": test_documents[i]['type'],
                    "similarity": float(similarity)
                })
            
            # Sort by similarity
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            results["jina"]["similarities"].append({
                "query": query,
                "results": similarities
            })
            
            print(f"    Query: '{query}'")
            print(f"      Best match: {similarities[0]['document']} ({similarities[0]['similarity']:.3f})")
        
    except Exception as e:
        print(f"❌ Jina test failed: {str(e)}")
        results["jina"]["error"] = str(e)
    
    return results

# Test chunking capabilities
async def test_large_document_handling():
    """Test handling of large documents"""
    print("\n" + "="*60)
    print("🧪 TESTING LARGE DOCUMENT HANDLING")
    print("="*60)
    
    # Simulate a large document
    large_doc = """
    FINANCIAL ANALYSIS REPORT - Q4 2024
    
    Executive Summary:
    """ + " ".join([f"Sentence {i} containing various financial metrics and analysis." for i in range(1000)])
    
    print(f"Document size: {len(large_doc)} characters")
    print(f"Approximate tokens: {len(large_doc)//4}")
    
    # Test chunking strategies
    chunk_size = 2000  # characters
    chunks = []
    
    for i in range(0, len(large_doc), chunk_size):
        chunk = large_doc[i:i+chunk_size]
        chunks.append(chunk)
    
    print(f"Created {len(chunks)} chunks")
    
    # Test processing chunks
    results = []
    import aiohttp
    async with aiohttp.ClientSession() as session:
        for i, chunk in enumerate(chunks[:3]):  # Test first 3 chunks
            print(f"\n  Processing chunk {i+1}...")
            start_time = time.time()
            
            try:
                async with session.post(
                    "http://localhost:1234/v1/chat/completions",
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {"role": "system", "content": "Summarize the key points."},
                            {"role": "user", "content": chunk}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 200
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        summary = data['choices'][0]['message']['content']
                        elapsed = time.time() - start_time
                        
                        results.append({
                            "chunk": i,
                            "success": True,
                            "summary": summary,
                            "time": elapsed
                        })
                        print(f"    ✅ Processed in {elapsed:.2f}s")
                    else:
                        results.append({
                            "chunk": i,
                            "success": False,
                            "error": f"HTTP {resp.status}"
                        })
                        print(f"    ❌ Failed: HTTP {resp.status}")
                        
            except Exception as e:
                results.append({
                    "chunk": i,
                    "success": False,
                    "error": str(e)
                })
                print(f"    ❌ Error: {str(e)}")
    
    return {
        "total_chunks": len(chunks),
        "tested_chunks": len(results),
        "results": results
    }

# Main test runner
async def main():
    """Run all tests and save results"""
    print("\n" + "="*60)
    print("🚀 DESTINY TEAM - LMSTUDIO & EMBEDDINGS TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now()}")
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test 1: Local LLM
    print("\n\n▶️  TEST 1: LOCAL LLM (LMSTUDIO)")
    llm_results = await test_local_llm()
    all_results["tests"]["local_llm"] = llm_results
    
    # Test 2: Embeddings
    print("\n\n▶️  TEST 2: EMBEDDING MODELS")
    embedding_results = await test_embeddings()
    all_results["tests"]["embeddings"] = embedding_results
    
    # Test 3: Large document handling
    print("\n\n▶️  TEST 3: LARGE DOCUMENT HANDLING")
    chunking_results = await test_large_document_handling()
    all_results["tests"]["large_documents"] = chunking_results
    
    # Save results
    results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    # Summary statistics
    llm_success = sum(1 for r in llm_results if r.get('success', False))
    print(f"\nLocal LLM Tests: {llm_success}/{len(llm_results)} passed")
    
    e5_working = "error" not in all_results["tests"]["embeddings"].get("e5-large", {})
    jina_working = "error" not in all_results["tests"]["embeddings"].get("jina", {})
    print(f"E5-Large Embeddings: {'✅ Working' if e5_working else '❌ Failed'}")
    print(f"Jina Embeddings: {'✅ Working' if jina_working else '❌ Failed'}")
    
    chunk_success = sum(1 for r in chunking_results['results'] if r.get('success', False))
    print(f"Document Chunking: {chunk_success}/{len(chunking_results['results'])} chunks processed")
    
    print(f"\n📁 Detailed results saved to: {results_file}")
    
    return all_results

if __name__ == "__main__":
    asyncio.run(main())