#!/usr/bin/env python3
"""
Check LMStudio Models Availability
Aleksander Nowak - Orchestrator
2025-11-05
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

LMSTUDIO_HOST = "192.168.200.226"
LMSTUDIO_PORT = "1234"
BASE_URL = f"http://{LMSTUDIO_HOST}:{LMSTUDIO_PORT}/v1"

def check_models():
    """Check available models via /v1/models endpoint"""
    print("\n" + "="*60)
    print("🔍 CHECKING LMSTUDIO MODELS")
    print("="*60)
    print(f"Server: {BASE_URL}")
    
    try:
        url = f"{BASE_URL}/models"
        print(f"\n📡 Requesting: {url}")
        
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            print("\n✅ Connected successfully!")
            print(f"\n📦 Available Models: {len(data.get('data', []))}")
            
            models = data.get('data', [])
            
            # Separate LLM and embedding models
            llm_models = []
            embedding_models = []
            
            for model in models:
                model_id = model.get('id', 'unknown')
                model_type = model.get('object', 'unknown')
                
                # Check if it's embedding or chat model
                if 'embed' in model_id.lower() or 'embedding' in model_id.lower():
                    embedding_models.append(model)
                else:
                    llm_models.append(model)
            
            print("\n" + "="*60)
            print("🤖 LLM MODELS:")
            print("="*60)
            
            if llm_models:
                for i, model in enumerate(llm_models, 1):
                    model_id = model.get('id', 'unknown')
                    print(f"\n{i}. {model_id}")
                    print(f"   Object: {model.get('object', 'unknown')}")
                    if model.get('created'):
                        print(f"   Created: {model.get('created')}")
            else:
                print("\n⚠️  No LLM models found!")
            
            print("\n" + "="*60)
            print("📊 EMBEDDING MODELS:")
            print("="*60)
            
            if embedding_models:
                for i, model in enumerate(embedding_models, 1):
                    model_id = model.get('id', 'unknown')
                    print(f"\n{i}. {model_id}")
                    print(f"   Object: {model.get('object', 'unknown')}")
                    if model.get('created'):
                        print(f"   Created: {model.get('created')}")
            else:
                print("\n⚠️  No embedding models found!")
            
            # Save to file
            results = {
                "timestamp": str(datetime.now()),
                "server": BASE_URL,
                "total_models": len(models),
                "llm_models": [
                    {
                        "id": m.get('id'),
                        "object": m.get('object'),
                        "created": m.get('created')
                    }
                    for m in llm_models
                ],
                "embedding_models": [
                    {
                        "id": m.get('id'),
                        "object": m.get('object'),
                        "created": m.get('created')
                    }
                    for m in embedding_models
                ],
                "all_models": models
            }
            
            filename = f"lmstudio_models_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n📁 Results saved to: {filename}")
            
            return results
            
    except urllib.error.URLError as e:
        print(f"\n❌ Connection failed: {e}")
        print(f"\n⚠️  Is LMStudio running on {BASE_URL}?")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_llm_chat(model_id="gpt-oss-20b"):
    """Test LLM chat completion"""
    print("\n" + "="*60)
    print(f"🧪 TESTING LLM: {model_id}")
    print("="*60)
    
    url = f"{BASE_URL}/chat/completions"
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2+2? Answer briefly."}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 Sending request to: {url}")
        print(f"📝 Prompt: What is 2+2?")
        
        import time
        start_time = time.time()
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            elapsed = time.time() - start_time
            
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content']
                print(f"\n✅ Success! Time: {elapsed:.2f}s")
                print(f"📤 Response: {answer}")
                
                if 'usage' in result:
                    usage = result['usage']
                    print(f"\n📊 Token Usage:")
                    print(f"   Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"   Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"   Total tokens: {usage.get('total_tokens', 'N/A')}")
                
                return True
            else:
                print(f"\n⚠️  Unexpected response format")
                print(json.dumps(result, indent=2))
                return False
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"\n❌ HTTP Error {e.code}: {e.reason}")
        print(f"Response: {error_body}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_embeddings(model_id=None):
    """Test embedding generation"""
    print("\n" + "="*60)
    print("🧪 TESTING EMBEDDINGS")
    print("="*60)
    
    url = f"{BASE_URL}/embeddings"
    
    # Try to detect embedding model if not provided
    if not model_id:
        # Common embedding model names
        possible_models = [
            "text-embedding-intfloat-multilingual-e5-large-instruct",
            "text-embedding-ada-002",
            "nomic-embed-text",
            "jina-embeddings"
        ]
        model_id = possible_models[0]  # Default to E5-Large
    
    test_text = "Financial analysis shows strong growth"
    
    data = {
        "model": model_id,
        "input": test_text
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 Sending request to: {url}")
        print(f"📝 Text: {test_text}")
        print(f"🤖 Model: {model_id}")
        
        import time
        start_time = time.time()
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            elapsed = time.time() - start_time
            
            if 'data' in result and len(result['data']) > 0:
                embedding = result['data'][0]['embedding']
                print(f"\n✅ Success! Time: {elapsed:.2f}s")
                print(f"📐 Embedding dimensions: {len(embedding)}")
                print(f"📊 First 5 values: {embedding[:5]}")
                
                return True
            else:
                print(f"\n⚠️  Unexpected response format")
                print(json.dumps(result, indent=2))
                return False
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"\n❌ HTTP Error {e.code}: {e.reason}")
        print(f"Response: {error_body}")
        print("\n💡 Trying alternative model names...")
        
        # Try other common embedding model names
        for alt_model in ["text-embedding-ada-002", "nomic-embed-text", "jina-embeddings-v3"]:
            print(f"\n🔄 Trying: {alt_model}")
            data["model"] = alt_model
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if 'data' in result:
                        embedding = result['data'][0]['embedding']
                        print(f"✅ Success with {alt_model}! Dims: {len(embedding)}")
                        return True
            except:
                continue
        
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main check function"""
    print("\n" + "="*60)
    print("🚀 LMSTUDIO MODELS AVAILABILITY CHECK")
    print("="*60)
    print(f"Server: {BASE_URL}")
    print(f"Started at: {datetime.now()}")
    
    # Check available models
    models_info = check_models()
    
    if not models_info:
        print("\n❌ Could not connect to LMStudio server")
        print("Please check:")
        print(f"1. Is LMStudio running on {LMSTUDIO_HOST}:{LMSTUDIO_PORT}?")
        print("2. Is the server accessible from this machine?")
        return
    
    # Test LLM if available
    llm_models = models_info.get('llm_models', [])
    if llm_models:
        print("\n\n" + "="*60)
        print("🧪 TESTING LLM CAPABILITIES")
        print("="*60)
        
        # Try gpt-oss-20b first
        model_id = "gpt-oss-20b"
        if not test_llm_chat(model_id):
            # Try first available LLM model
            if llm_models:
                alt_model = llm_models[0].get('id', 'unknown')
                print(f"\n🔄 Trying alternative model: {alt_model}")
                test_llm_chat(alt_model)
    else:
        print("\n⚠️  No LLM models available for testing")
    
    # Test Embeddings
    embedding_models = models_info.get('embedding_models', [])
    if embedding_models:
        print("\n\n" + "="*60)
        print("🧪 TESTING EMBEDDING CAPABILITIES")
        print("="*60)
        
        # Try each embedding model
        for emb_model in embedding_models:
            model_id = emb_model.get('id')
            if model_id:
                print(f"\n📊 Testing model: {model_id}")
                test_embeddings(model_id)
    else:
        print("\n⚠️  No embedding models found")
        print("\n💡 Trying default embedding model...")
        test_embeddings()
    
    print("\n" + "="*60)
    print("✅ CHECK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()