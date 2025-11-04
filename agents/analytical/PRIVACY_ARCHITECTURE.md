# Privacy Architecture - Analytical Team

## 🔒 **PRIVACY-FIRST DESIGN**

The Destiny Analytical Team is designed with **privacy as a core principle**, not an afterthought.

---

## **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYTICAL TEAM                           │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Elena   │  │  Marcus  │  │  Sofia   │  │  Adrian  │   │
│  │  OSINT   │  │ Financial│  │  Market  │  │  Legal   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │              │          │
│       └─────────────┴──────────────┴──────────────┘          │
│                         │                                    │
│              ┌──────────▼──────────┐                        │
│              │   LLM ROUTER        │                        │
│              │  (Privacy Engine)   │                        │
│              └──────────┬──────────┘                        │
│                         │                                    │
│           ┌─────────────┴─────────────┐                    │
│           │                           │                     │
│    ┌──────▼──────┐           ┌───────▼────────┐           │
│    │  LOCAL LLM  │           │   CLOUD LLM    │           │
│    │ (LM Studio) │           │  (Optional)    │           │
│    │             │           │                │           │
│    │ 🔒 PRIVATE  │           │ ☁️  PUBLIC     │           │
│    │ Sensitive   │           │ Non-sensitive  │           │
│    │ Data        │           │ Data           │           │
│    └─────────────┘           └────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

    ↓ All data stays local        ↓ Optional cloud routing
    
┌──────────────┐              ┌──────────────┐
│ Your Machine │              │ Cloud APIs   │
│              │              │ (if enabled) │
│ - LM Studio  │              │              │
│ - Postgres   │              │ - OpenAI     │
│ - Qdrant     │              │ - Anthropic  │
│ - Elasticsearch              │              │
└──────────────┘              └──────────────┘
```

---

## **Three Privacy Modes**

### **1. LOCAL Mode (Maximum Privacy)** 🔒

```python
ANALYTICAL_LLM_MODE=LOCAL
```

**ALL agents use LM Studio Server:**
- ✅ All AI processing on your machine
- ✅ Sensitive data NEVER leaves your infrastructure
- ✅ No external API calls
- ✅ No usage tracking
- ✅ No rate limits
- ✅ No API costs

**Perfect for:**
- Confidential investigations
- Financial fraud analysis
- Legal document review
- OSINT on sensitive targets
- Attorney-client privileged data
- Trade secrets
- PII (Personally Identifiable Information)

---

### **2. CLOUD Mode** ☁️

```python
ANALYTICAL_LLM_MODE=CLOUD
```

**ALL agents use cloud APIs (OpenAI/Anthropic):**
- ✅ Faster inference (large models)
- ✅ Latest model versions
- ✅ No local GPU needed
- ⚠️  Data sent to external servers
- 💰 API costs apply

**Use for:**
- Non-sensitive public data analysis
- Market research on public companies
- General competitive intelligence
- Public domain documents

---

### **3. HYBRID Mode** 🔄

```python
ANALYTICAL_LLM_MODE=HYBRID
```

**Intelligent routing based on data sensitivity:**

| Agent | Sensitive Data → | Public Data → |
|-------|-----------------|---------------|
| **Elena** (OSINT) | 🔒 LOCAL | 🔒 LOCAL (always) |
| **Marcus** (Financial) | 🔒 LOCAL | 🔒 LOCAL (always) |
| **Adrian** (Legal) | 🔒 LOCAL | 🔒 LOCAL (always) |
| **Sofia** (Market) | 🔒 LOCAL | ☁️ CLOUD |
| **Maya** (Data) | 🔒 LOCAL | ☁️ CLOUD |
| **Lucas** (Reports) | 🔒 LOCAL | ☁️ CLOUD |
| **Viktor** (Orchestrator) | 🔒 LOCAL | 🔒 LOCAL (always) |
| **Damian** (Devil's Advocate) | 🔒 LOCAL | 🔒 LOCAL (always) |
| **Alex** (Technical) | 🔒 LOCAL | 🔒 LOCAL (always) |

**Key Agents ALWAYS use LOCAL (even in HYBRID):**
- Elena Volkov - OSINT (sensitive investigations)
- Marcus Chen - Financial (confidential data)
- Adrian Kowalski - Legal (attorney-client privilege)
- Viktor Kovalenko - Orchestrator (sees all data)
- Damian Rousseau - Devil's Advocate (full context)
- Alex Morgan - Technical Liaison (handles sensitive docs)

---

## **Data Classification**

```python
# Mark task as sensitive
task = Task(
    description="Investigate Company XYZ CEO",
    metadata={"sensitive": True}  # ← Routes to LOCAL LLM
)

# Mark task as public
task = Task(
    description="Analyze public market trends",
    metadata={"sensitive": False}  # ← Can route to CLOUD (if HYBRID mode)
)
```

**Default behavior:**
```python
DATA_SENSITIVE_BY_DEFAULT=true
```
All data is treated as sensitive unless explicitly marked public.

---

## **Privacy Guarantees**

### **When using LOCAL mode:**

| Feature | Status |
|---------|--------|
| **Data Location** | ✅ Your machine only |
| **Network Traffic** | ✅ None (to AI providers) |
| **API Keys** | ✅ Not needed |
| **Usage Tracking** | ✅ None |
| **Data Retention** | ✅ You control |
| **Compliance** | ✅ GDPR, HIPAA compatible |
| **Costs** | ✅ Free (no API charges) |
| **Rate Limits** | ✅ Unlimited |

### **LM Studio Server Security:**
- Runs on `localhost:1234` by default
- Not exposed to internet
- No authentication needed (local only)
- All data stays in RAM/disk on your machine

---

## **Configuration Examples**

### **Example 1: Maximum Privacy (Default)**

```bash
# .env file
ANALYTICAL_LLM_MODE=LOCAL
LM_STUDIO_URL=http://localhost:1234/v1
DATA_SENSITIVE_BY_DEFAULT=true
```

**Result:**
- All 9 agents use LM Studio
- Zero external API calls
- Complete privacy

---

### **Example 2: Hybrid with Public Data**

```bash
# .env file
ANALYTICAL_LLM_MODE=HYBRID
LM_STUDIO_URL=http://localhost:1234/v1
DATA_SENSITIVE_BY_DEFAULT=true
OPENAI_API_KEY=sk-...  # Only for non-sensitive data
```

**Result:**
- Sensitive data → LM Studio (LOCAL)
- Public data → OpenAI (CLOUD) - for non-critical agents only
- Critical agents (Elena, Marcus, Adrian, Viktor, Damian, Alex) → ALWAYS LOCAL

---

### **Example 3: Remote LM Studio Server**

```bash
# .env file
ANALYTICAL_LLM_MODE=LOCAL
LM_STUDIO_URL=http://192.168.1.100:1234/v1  # ← On another machine in LAN
```

**Result:**
- All agents use LM Studio on private network
- Still private (no internet exposure)
- Can use powerful server GPU

---

## **Technical Implementation**

### **1. LLM Router** (`local_llm_integration.py`)

```python
class AnalyticalAgentLLM:
    def analyze(self, agent_name, task, is_sensitive=True):
        # Determine routing
        mode = AnalyticalConfig.get_llm_mode(agent_name, is_sensitive)
        
        if mode == "LOCAL":
            return self.local_llm.chat(messages)  # ← LM Studio
        else:
            return self.cloud_llm.chat(messages)  # ← OpenAI/Anthropic
```

### **2. Agent Integration**

Each agent can use the LLM client:

```python
from agents.analytical.local_llm_integration import AnalyticalAgentLLM

class ElenaAgent(BaseAgent):
    def __init__(self):
        super().__init__(...)
        self.llm = AnalyticalAgentLLM(mode="LOCAL")
    
    def analyze_target(self, target, sensitive=True):
        result = self.llm.analyze(
            agent_name=self.name,
            agent_role=self.role,
            task_description=f"Investigate {target}",
            context="OSINT investigation",
            is_sensitive=sensitive  # ← Routes appropriately
        )
        return result
```

---

## **Comparison: Destiny Teams**

| Feature | **Technical Team** | **Analytical Team** |
|---------|-------------------|---------------------|
| **Primary Use** | Software development | Investigations & analysis |
| **Data Sensitivity** | Code (medium) | PII, financial, legal (high) |
| **Privacy Mode** | Optional | **Built-in from day 1** |
| **LLM Options** | Cloud-first | **Local-first** |
| **Default Mode** | Cloud/API | **LOCAL (LM Studio)** |
| **External Calls** | Common | **Minimized/none** |

---

## **Benefits of Local LLM**

### **Privacy Benefits:**
1. ✅ **GDPR Compliance** - No data transferred to US servers
2. ✅ **HIPAA Compatible** - Healthcare data stays local
3. ✅ **Attorney-Client Privilege** - Legal analysis remains confidential
4. ✅ **Trade Secrets** - Competitive intelligence stays private
5. ✅ **Financial Confidentiality** - Sensitive financial data protected

### **Operational Benefits:**
1. ✅ **No Rate Limits** - Unlimited queries
2. ✅ **No API Costs** - Free after initial setup
3. ✅ **No Network Dependency** - Works offline
4. ✅ **Predictable Performance** - No API throttling
5. ✅ **Full Control** - You choose the model

### **Security Benefits:**
1. ✅ **No Data Leakage** - Can't leak what never leaves
2. ✅ **No Third-Party Access** - No cloud provider involved
3. ✅ **No Training Data Contamination** - Your data won't train their models
4. ✅ **Audit Trail** - Complete control and logging
5. ✅ **Air-Gap Capable** - Can run fully disconnected

---

## **Recommended Setup**

### **For Maximum Privacy:**

1. **Run LM Studio Server locally**
   - Load a capable model (e.g., Mistral 7B, Llama 3 8B, Gemma 27B)
   - Allocate sufficient RAM/VRAM

2. **Set environment variables**
   ```bash
   ANALYTICAL_LLM_MODE=LOCAL
   DATA_SENSITIVE_BY_DEFAULT=true
   ```

3. **Start analytical agents**
   - All processing stays local
   - Zero external API calls

### **Hardware Recommendations:**

| Model Size | RAM | VRAM (GPU) | Performance |
|-----------|-----|------------|-------------|
| **7B** (Mistral, Llama) | 16GB | 8GB | Good |
| **13B** (Llama, Vicuna) | 32GB | 16GB | Better |
| **27B** (Gemma 3) | 64GB | 24GB | Best |

**CPU-only mode works too** (slower but private!)

---

## **Privacy Checklist**

Before deploying analytical team with sensitive data:

- [ ] LM Studio Server running locally
- [ ] `ANALYTICAL_LLM_MODE=LOCAL` set
- [ ] `DATA_SENSITIVE_BY_DEFAULT=true` set
- [ ] No external API keys configured
- [ ] Firewall blocks outbound AI API calls (optional extra security)
- [ ] All databases local (Postgres, Qdrant, Elasticsearch, Neo4j, Redis)
- [ ] Network traffic monitoring enabled (verify no leaks)
- [ ] Test with sample sensitive data first

---

## **Summary**

The Analytical Team is designed for **privacy-first operations**:

✅ **LOCAL mode by default** (LM Studio)  
✅ **Sensitive agents always local** (Elena, Marcus, Adrian, Viktor, Damian, Alex)  
✅ **Configurable per agent** (fine-grained control)  
✅ **No external dependencies required** (fully self-hosted)  
✅ **GDPR/HIPAA compatible** (data never leaves your infrastructure)  
✅ **Zero API costs** (free after setup)  
✅ **Unlimited usage** (no rate limits)  

**Your data, your machine, your control.** 🔒
