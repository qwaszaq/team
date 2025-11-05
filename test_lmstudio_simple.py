#!/usr/bin/env python3
"""
Simplified test for LMStudio - no external dependencies
Aleksander Nowak - Orchestrator
2025-11-05
"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime

def test_lmstudio_llm():
    """Test LMStudio local LLM with simple HTTP request"""
    print("\n" + "="*60)
    print("🧪 TESTING LMSTUDIO LOCAL LLM")
    print("="*60)
    
    url = "http://localhost:1234/v1/chat/completions"
    
    # Test cases
    test_prompts = [
        "What is 2+2?",
        "Analyze this: Revenue increased 23% to $4.2M. What does this indicate?",
        "List 3 risks in financial analysis."
    ]
    
    results = []
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n📝 Test {i+1}: {prompt}")
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            start_time = time.time()
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                elapsed = time.time() - start_time
                
                answer = result['choices'][0]['message']['content']
                print(f"✅ Success! Time: {elapsed:.2f}s")
                print(f"Response: {answer[:100]}...")
                
                results.append({
                    "test": i+1,
                    "prompt": prompt,
                    "success": True,
                    "response": answer,
                    "time": elapsed
                })
                
        except urllib.error.URLError as e:
            print(f"❌ Connection failed: {e}")
            print("⚠️  Is LMStudio running on http://localhost:1234?")
            results.append({
                "test": i+1,
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "test": i+1,
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })
    
    return results

def test_lmstudio_embeddings():
    """Test LMStudio embeddings"""
    print("\n" + "="*60)
    print("🧪 TESTING LMSTUDIO EMBEDDINGS")
    print("="*60)
    
    url = "http://localhost:1234/v1/embeddings"
    
    test_texts = [
        "Financial analysis shows strong growth",
        "Legal compliance audit required",
        "Technical infrastructure assessment"
    ]
    
    results = []
    
    for text in test_texts:
        print(f"\n📝 Embedding: {text}")
        
        data = {
            "model": "text-embedding-intfloat-multilingual-e5-large-instruct",
            "input": text
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            start_time = time.time()
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                elapsed = time.time() - start_time
                
                embedding = result['data'][0]['embedding']
                print(f"✅ Success! Time: {elapsed:.2f}s")
                print(f"Embedding dims: {len(embedding)}")
                
                results.append({
                    "text": text,
                    "success": True,
                    "dims": len(embedding),
                    "time": elapsed
                })
                
        except urllib.error.URLError as e:
            print(f"❌ Connection failed: {e}")
            print("⚠️  Is embedding model loaded in LMStudio?")
            results.append({
                "text": text,
                "success": False,
                "error": str(e)
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "text": text,
                "success": False,
                "error": str(e)
            })
    
    return results

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 LMSTUDIO SIMPLE TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now()}")
    
    # Test LLM
    print("\n\n▶️  TEST 1: LOCAL LLM")
    llm_results = test_lmstudio_llm()
    
    # Test Embeddings
    print("\n\n▶️  TEST 2: EMBEDDINGS")
    embedding_results = test_lmstudio_embeddings()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    llm_success = sum(1 for r in llm_results if r.get('success', False))
    print(f"\nLocal LLM Tests: {llm_success}/{len(llm_results)} passed")
    
    emb_success = sum(1 for r in embedding_results if r.get('success', False))
    print(f"Embedding Tests: {emb_success}/{len(embedding_results)} passed")
    
    # Save results
    results = {
        "timestamp": str(datetime.now()),
        "llm_tests": llm_results,
        "embedding_tests": embedding_results
    }
    
    filename = f"test_results_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to: {filename}")
    
    # Recommendations
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS")
    print("="*60)
    
    if llm_success == 0:
        print("\n❌ LLM not working. Please:")
        print("1. Start LMStudio")
        print("2. Load a model (e.g., gpt-oss-20b)")
        print("3. Start the server on port 1234")
    elif llm_success < len(llm_results):
        print("\n⚠️  Some LLM tests failed. Check model stability.")
    else:
        print("\n✅ LLM working perfectly!")
    
    if emb_success == 0:
        print("\n❌ Embeddings not working. Please:")
        print("1. Load an embedding model in LMStudio")
        print("2. Try: text-embedding-intfloat-multilingual-e5-large-instruct")
    elif emb_success < len(embedding_results):
        print("\n⚠️  Some embedding tests failed. Check model.")
    else:
        print("\n✅ Embeddings working perfectly!")
    
    return results

if __name__ == "__main__":
    main()