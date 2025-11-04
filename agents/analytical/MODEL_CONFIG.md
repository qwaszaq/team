# LM Studio Model Configuration - Analytical Team

## 🤖 **Configured Model: gpt-oss-20b**

Your analytical team is configured to use **gpt-oss-20b** running on LM Studio Server.

---

## **Model Specifications**

```
Model: gpt-oss-20b
Parameters: 20 Billion
Architecture: GPT-based
Context Window: 44,000 tokens (MASSIVE!)
Hosting: LM Studio Server (localhost:1234)
Privacy: 100% Local (no external API calls)
Cost: FREE (no API charges)
```

---

## **Why gpt-oss-20b is Perfect for Analytical Work:**

### **✅ Strengths:**

1. **MASSIVE 44K Token Context Window** ⭐
   - Can handle ENTIRE reports in one go (~33,000 words!)
   - Maintains context across very complex analysis
   - Perfect for:
     * Full legal contracts (no chunking needed!)
     * Complete financial statements with all footnotes
     * Entire investigation reports
     * Multiple documents in single context
     * Long-form analytical reasoning

2. **Strong Reasoning**
   - 20B parameters = excellent analytical capabilities
   - Good at connecting disparate information
   - Effective at multi-step reasoning

3. **Document Understanding**
   - Handles structured data (tables, lists)
   - Good at extracting key information
   - Effective at summarization

4. **Privacy-First**
   - All processing stays on your machine
   - No data sent to external servers
   - Perfect for sensitive investigations

---

## **Performance Expectations**

### **Speed:**
```
- Simple query (50 tokens): ~2-5 seconds
- Complex analysis (500 tokens): ~10-20 seconds
- Long report (2000 tokens): ~40-60 seconds
```

### **Token Limits:**
```
- Max context: 44,000 tokens (MASSIVE! ~33,000 words)
- Max output: Configurable (default 1500-2500 per agent)
- Context retention: Exceptional for 20B model with 44K window
- Practical use: Can fit entire reports, multiple documents, long conversations
```

**What 44K tokens means in practice:**
- ~33,000 words
- ~66 pages of text (single-spaced)
- Entire Harry Potter book (~77K words needs 2 contexts)
- 10-15 full research papers
- Complete legal contracts with appendices
- Full year financial statements with all notes
- Entire investigation case file

### **Hardware Requirements:**
```
Minimum:
- RAM: 32GB (20B model needs substantial memory)
- VRAM: 12GB GPU (or CPU with 48GB+ RAM)
- Storage: ~40GB for model files

Recommended:
- RAM: 64GB
- VRAM: 24GB GPU (faster inference)
- Storage: SSD for faster loading
```

---

## **Agent-Specific Settings**

Each analytical agent has custom settings optimized for their role:

```python
AGENT_SETTINGS = {
    "Elena Volkov": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.7,  # Balanced creativity/accuracy
    },
    "Marcus Chen": {
        "model": "gpt-oss-20b",
        "max_tokens": 3000,  # More for comprehensive financial analysis
        "temperature": 0.5,  # More conservative for numbers
        "note": "44K context = entire financial statement in one go!"
    },
    "Sofia Martinez": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.7,
    },
    "Adrian Kowalski": {
        "model": "gpt-oss-20b",
        "max_tokens": 3000,  # More for legal reasoning
        "temperature": 0.6,  # Balanced for legal analysis
        "note": "44K context = entire contract with all clauses!"
    },
    "Maya Patel": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.5,  # Conservative for statistics
    },
    "Lucas Rivera": {
        "model": "gpt-oss-20b",
        "max_tokens": 4000,  # Most for comprehensive report writing
        "temperature": 0.7,  # Balanced for prose
        "note": "44K context = can read and synthesize multiple full reports!"
    },
    "Viktor Kovalenko": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.7,
    },
    "Damian Rousseau": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.8,  # More creative for alternatives
    },
    "Alex Morgan": {
        "model": "gpt-oss-20b",
        "max_tokens": 1500,
        "temperature": 0.6,
    }
}
```

---

## **Configuration**

### **Environment Variable:**

```bash
# .env file
LM_STUDIO_MODEL=gpt-oss-20b
LM_STUDIO_URL=http://localhost:1234/v1
LM_STUDIO_TIMEOUT=120
```

### **Python Configuration:**

```python
from agents.analytical.config import AnalyticalConfig

# Current model
print(AnalyticalConfig.LM_STUDIO_MODEL)
# Output: gpt-oss-20b

# LM Studio endpoint
print(AnalyticalConfig.LM_STUDIO_BASE_URL)
# Output: http://localhost:1234/v1
```

---

## **Verification**

### **Test Connection:**

```python
from agents.analytical.local_llm_integration import LocalLLM

# Initialize (will connect to gpt-oss-20b)
llm = LocalLLM(model="gpt-oss-20b")

# Test chat
messages = [
    {"role": "system", "content": "You are a financial analyst."},
    {"role": "user", "content": "Explain ROI in one sentence."}
]

response = llm.chat(messages, temperature=0.7, max_tokens=100)
print(response)
```

### **Expected Output:**
```
✅ Connected to LM Studio Server
   Model: gpt-oss-20b
   Endpoint: http://localhost:1234/v1

Response: Return on Investment (ROI) is a financial metric that measures 
the profitability of an investment by comparing the gain or loss to its cost, 
typically expressed as a percentage.
```

---

## **Model Comparison**

| Feature | gpt-oss-20b | Smaller Models (7B) | Larger Models (70B+) |
|---------|-------------|---------------------|---------------------|
| **Reasoning** | ✅ Excellent | ⚠️ Good | ✅✅ Best |
| **Speed** | ✅ Fast | ✅✅ Very Fast | ⚠️ Slow |
| **Memory** | ⚠️ 32GB+ | ✅ 16GB | ❌ 64GB+ |
| **Context Retention** | ✅ Excellent | ⚠️ Good | ✅✅ Best |
| **Analytical Tasks** | ✅ Excellent | ⚠️ Adequate | ✅✅ Best |
| **Cost** | ✅ FREE | ✅ FREE | ✅ FREE |
| **Privacy** | ✅ 100% Local | ✅ 100% Local | ✅ 100% Local |

**Verdict:** gpt-oss-20b is the **sweet spot** for analytical work - excellent reasoning with reasonable resource requirements.

---

## **Optimization Tips**

### **1. For Faster Inference:**

```python
# Reduce max_tokens for simple tasks
llm.chat(messages, max_tokens=500)  # Instead of 1500

# Lower temperature for deterministic output
llm.chat(messages, temperature=0.3)  # Instead of 0.7
```

### **2. For Better Quality:**

```python
# Increase max_tokens for complex analysis
llm.chat(messages, max_tokens=2500)

# Higher temperature for creative alternatives
llm.chat(messages, temperature=0.8)  # For Damian (Devil's Advocate)
```

### **3. For Resource Conservation:**

```python
# Use GPU acceleration (if available)
# gpt-oss-20b will automatically use GPU if detected

# Monitor memory usage
# 20B model typically uses 24-32GB RAM
```

---

## **Embeddings Configuration**

For semantic search (Qdrant), you're using **Jina v4** (separate model):

```
Chat Model: gpt-oss-20b (LM Studio)
Embedding Model: jinaai/jina-embeddings-v4-text-retrieval (LM Studio)

Why separate?
- gpt-oss-20b: Excellent for reasoning and generation
- Jina v4: Optimized for document embeddings (8192 tokens, table-aware)
```

---

## **Troubleshooting**

### **Issue: Model not loading**

```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# Verify gpt-oss-20b is loaded
# Should show: {"data": [{"id": "gpt-oss-20b", ...}]}
```

### **Issue: Slow responses**

```python
# Reduce max_tokens
AnalyticalConfig.AGENT_SETTINGS["agent_name"]["max_tokens"] = 1000

# Or reduce temperature
AnalyticalConfig.AGENT_SETTINGS["agent_name"]["temperature"] = 0.5
```

### **Issue: Out of memory**

```bash
# Free up RAM
# Close other applications
# Or reduce batch processing

# Check model size
# gpt-oss-20b requires ~24GB minimum
```

---

## **Best Practices**

### **For Analytical Team:**

1. **Investigation Tasks** (Viktor, Elena):
   - Use default settings (1500 tokens, temp 0.7)
   - Allow model to explore and connect information

2. **Financial Analysis** (Marcus):
   - Conservative temperature (0.5)
   - More tokens (2000) for detailed analysis
   - Verify calculations separately

3. **Legal Research** (Adrian):
   - Moderate temperature (0.6)
   - More tokens (2000) for complex reasoning
   - Cross-reference citations

4. **Data Analysis** (Maya):
   - Lower temperature (0.5) for consistency
   - Standard tokens (1500)
   - Use for interpretation, not calculation

5. **Report Writing** (Lucas):
   - Balanced temperature (0.7)
   - Maximum tokens (2500) for long-form content
   - Multiple passes for refinement

6. **Critical Review** (Damian):
   - Higher temperature (0.8) for creativity
   - Standard tokens (1500)
   - Encourage alternative perspectives

---

## **Summary**

✅ **Model:** gpt-oss-20b (20 billion parameters)  
✅ **Performance:** Excellent for analytical reasoning  
✅ **Privacy:** 100% local processing  
✅ **Cost:** FREE (no API charges)  
✅ **Integration:** Fully configured and ready  
✅ **Status:** Production ready  

**Your analytical team is powered by a strong local LLM with complete privacy!** 🔒🤖
