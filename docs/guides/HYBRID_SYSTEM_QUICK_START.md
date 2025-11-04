# 🚀 HYBRID ON-PREM SYSTEM - Quick Start Guide

**Local LLM Worker + Cloud Supervisor = Professional Intelligence**

---

## 🎯 What This System Does

**Problem:** Cloud LLMs are expensive, raise privacy concerns, create dependencies

**Solution:** Hybrid architecture
- **Local LLM (LMStudio):** Executes investigations using on-prem tools (90% cost savings!)
- **Aleksander (Claude):** Supervises quality, reviews output, ensures professional standards
- **Local Tools:** Scraping, statistics, databases - all running locally
- **Result:** Privacy + Cost Savings + Professional Quality

---

## 📋 Prerequisites

### **1. LMStudio Installed**

Download from: https://lmstudio.ai/

**Recommended Models (choose one):**
- **Mixtral 8x7B Instruct** (Q4 or Q5) - Best balance
- **Llama 3 70B Instruct** (Q4) - High quality, needs more RAM
- **Qwen 2.5 32B Instruct** (Q5) - Good Polish language support
- **DeepSeek Coder 33B** (Q5) - If focus on code/technical

**Model Requirements:**
- Function calling support (OpenAI-compatible)
- Context window: 32k+ tokens
- RAM: 16GB minimum (32GB+ recommended for 70B models)

### **2. Python Environment**

```bash
# Python 3.9+
python --version

# Install dependencies
pip install -r requirements.txt
```

### **3. Local Toolkits**

Already implemented:
- ✅ ScrapingToolkit (`agents/analytical/tools/scraping_toolkit.py`)
- ✅ MathematicalToolkit (`agents/analytical/tools/mathematical_toolkit.py`)

Optional dependencies:
```bash
# For dynamic web scraping
pip install playwright
playwright install chromium

# For better user agents
pip install fake-useragent
```

---

## 🏁 Quick Start (5 minutes)

### **Step 1: Start LMStudio**

1. Open LMStudio
2. Load a model (e.g., Mixtral 8x7B Instruct)
3. Go to "Local Server" tab
4. Click "Start Server"
5. Verify server running at `http://localhost:1234`

### **Step 2: Test Local LLM**

```bash
cd /Users/artur/coursor-agents-destiny-folder

# Run basic test
python local_orchestrator.py
```

**What Happens:**
- Local LLM receives investigation task
- Uses tools (scrape_webpage, archive_source, calculate_statistics)
- Logs all actions to `./logs/local_llm/`
- Saves results to `./shared_workspace/results/`

**Expected Output:**
```
🚀 LOCAL LLM ORCHESTRATOR - Proof of Concept
============================================================
✅ LocalLLMOrchestrator initialized
   LMStudio: http://localhost:1234/v1
   Model: local-model
   Tools: 3 available

============================================================
🔍 INVESTIGATION: test_cpk_research
============================================================
Task: Research the concept of "Central Transportation Hub" (CPK) in Poland...

--- Iteration 1/5 ---
🤖 LLM Call: 2 messages
💬 LLM Response: 245 tokens
🔧 Executing 2 tool(s)...
🔧 Tool: scrape_webpage
🔧 Tool: archive_source

--- Iteration 2/5 ---
...

✅ INVESTIGATION COMPLETE
============================================================
Status: complete
Iterations: 3
Actions logged: 12
Result file: ./shared_workspace/results/result_test_cpk_research.json
```

### **Step 3: Supervisor Review**

```bash
# Aleksander (Claude via Cursor) reviews the work
python supervisor_interface.py
```

**What Happens:**
- Aleksander reads investigation logs
- Analyzes tool usage quality
- Checks source attribution compliance
- Evaluates analytical rigor
- Generates quality report

**Expected Output:**
```
🎯 SUPERVISOR INTERFACE - Quality Assurance
======================================================================

📋 Pending Investigations: 1

======================================================================
🔍 Reviewing: test_cpk_research
======================================================================

📊 SUPERVISOR QUALITY REPORT
======================================================================
Investigation ID: test_cpk_research
Supervisor: Aleksander (Claude Sonnet 4.5)

======================================================================
OVERALL GRADE: A
Ready for Publication: ✅ YES
======================================================================

📈 Execution Metrics:
   Status: complete
   Iterations: 3
   LLM Calls: 3
   Total Tokens: 1,247
   Efficiency: HIGH

🔧 Tool Usage:
   Total Calls: 8
   Tools: {'scrape_webpage': 4, 'archive_source': 4}
   Errors: 0
   Assessment: EXCELLENT

📚 Source Quality:
   Scraped: 4
   Archived: 4
   Archive Ratio: 100.0%
   Compliance: EXCELLENT
   Grade: A+
   Protocol Compliant: ✅

✅ Strengths:
   • Appropriate tool usage
   • Full SOURCE ATTRIBUTION PROTOCOL compliance
   • Efficient investigation (few iterations)
```

---

## 🎯 Production Workflow

### **Investigation Cycle:**

```
1. USER REQUEST (Artur)
   ↓
   "Zbadaj temat X używając lokalnego systemu"

2. ALEKSANDER (Supervisor) - Strategic Planning
   ↓
   Creates task definition:
   {
     "task": "Investigate X",
     "tools_required": ["scrape_webpage", "archive_source"],
     "quality_requirements": {...}
   }
   → Saves: shared_workspace/tasks/task_001.json

3. LOCAL LLM (Worker) - Tactical Execution
   ↓
   python local_orchestrator.py --task-file task_001.json
   
   - Reads task
   - Executes using tools
   - Logs everything
   - Saves result
   
   → Logs: logs/local_llm/investigation_001.jsonl
   → Result: shared_workspace/results/result_001.json

4. ALEKSANDER (Supervisor) - Quality Review
   ↓
   python supervisor_interface.py --review investigation_001
   
   - Analyzes logs
   - Checks quality
   - Generates report
   
   → Report: shared_workspace/reports/quality_report_001.json

5. DECISION:
   
   IF quality >= A:
      Aleksander synthesizes final professional report
      → DONE ✅
   
   ELSE:
      Aleksander creates guidance
      → shared_workspace/guidance/guidance_001.json
      → Local LLM iterates (back to step 3)
```

---

## 📝 Example: Custom Investigation

### **Scenario: Research Robert Telus CPK Transaction**

**Step 1: Create Task (Aleksander)**

```python
# In Cursor, Aleksander creates:
task = {
    "task_id": "telus_investigation",
    "objective": "Research Robert Telus CPK land transaction",
    "subtasks": [
        {
            "description": "Collect news articles about Telus and CPK",
            "tools": ["scrape_webpage", "archive_source"],
            "min_sources": 10
        },
        {
            "description": "Analyze land price data if available",
            "tools": ["calculate_statistics"],
            "analysis_required": "market comparison"
        }
    ],
    "quality_requirements": {
        "source_attribution": "mandatory",
        "archiving": "all_sources",
        "minimum_sources": 10
    }
}

# Save to shared_workspace/tasks/task_telus_investigation.json
```

**Step 2: Execute (Local LLM)**

```python
from local_orchestrator import LocalLLMOrchestrator

orchestrator = LocalLLMOrchestrator()

# Load task
with open("shared_workspace/tasks/task_telus_investigation.json") as f:
    task = json.load(f)

# Execute
result = orchestrator.run_investigation(
    task=task["objective"],
    context={"subtasks": task["subtasks"]},
    investigation_id="telus_investigation",
    max_iterations=20
)

# Result saved automatically to shared_workspace/results/
```

**Step 3: Review (Aleksander)**

```python
from supervisor_interface import SupervisorInterface

supervisor = SupervisorInterface()

# Generate quality report
report = supervisor.generate_quality_report("telus_investigation")

# Print report
supervisor.print_quality_report(report)

# If needs improvement, provide guidance
if not report['overall_assessment']['ready_for_publication']:
    guidance = supervisor.create_guidance(
        investigation_id="telus_investigation",
        guidance_text="""
        Investigation quality: B
        
        Issues:
        - Only 7 sources archived (required: 10)
        - Missing statistical analysis of land prices
        
        Next steps:
        1. Find 3 more credible sources about CPK land transactions
        2. Use calculate_statistics on any price data found
        3. Ensure all sources archived
        """,
        priority="high",
        specific_actions=[
            "Scrape 3 more news sources",
            "Archive all new sources",
            "Perform statistical analysis if data available"
        ]
    )
```

**Step 4: Iterate if Needed**

```python
# Local LLM reads guidance and continues
guidance_file = "shared_workspace/guidance/guidance_telus_investigation_20251104_160000.json"

with open(guidance_file) as f:
    guidance = json.load(f)

# Continue investigation with guidance
result = orchestrator.run_investigation(
    task=f"Continue previous investigation. Guidance: {guidance['guidance']}",
    investigation_id="telus_investigation_v2",
    max_iterations=10
)
```

**Step 5: Final Report (Aleksander)**

Once quality is A/A+, Aleksander synthesizes final professional report using all findings.

---

## 🔧 Configuration

### **LMStudio Settings**

Recommended settings for function calling:

```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_tokens": 2048,
  "repeat_penalty": 1.1,
  "context_length": 32768,
  "gpu_layers": -1
}
```

### **Orchestrator Configuration**

Edit `local_orchestrator.py`:

```python
orchestrator = LocalLLMOrchestrator(
    lmstudio_url="http://localhost:1234/v1",  # LMStudio endpoint
    model_name="mixtral-8x7b-instruct",       # Model identifier
    log_dir="./logs/local_llm",               # Where to store logs
    workspace_dir="./shared_workspace"        # Communication directory
)
```

### **Supervisor Configuration**

Edit `supervisor_interface.py`:

```python
supervisor = SupervisorInterface(
    workspace_dir="./shared_workspace"  # Must match orchestrator
)
```

---

## 📊 Monitoring & Debugging

### **Check Investigation Logs**

```bash
# View latest investigation log
tail -f logs/local_llm/investigation_*.jsonl

# Pretty print
cat logs/local_llm/investigation_20251104_153000.jsonl | jq .
```

### **Check Results**

```bash
# View investigation result
cat shared_workspace/results/result_inv_20251104_153000.json | jq .
```

### **Check Quality Reports**

```bash
# View supervisor assessment
cat shared_workspace/reports/quality_report_inv_20251104_153000.json | jq .
```

### **Common Issues**

**Issue 1: LMStudio Connection Failed**
```
Error: LMStudio API call failed: Connection refused

Solution:
1. Check LMStudio is running
2. Verify server started (green indicator)
3. Check URL: http://localhost:1234
4. Try curl http://localhost:1234/v1/models
```

**Issue 2: Tool Errors**
```
Error: ScrapingToolkit not available

Solution:
1. Check imports: from agents.analytical.tools.scraping_toolkit import ScrapingToolkit
2. Verify file exists: agents/analytical/tools/scraping_toolkit.py
3. Install dependencies: pip install beautifulsoup4 requests
```

**Issue 3: Model Not Responding**
```
Error: Timeout after 180 seconds

Solution:
1. Check model loaded in LMStudio
2. Increase timeout in call_llm() method
3. Try smaller model (less RAM required)
4. Check GPU layers setting (reduce if needed)
```

---

## 🎓 Best Practices

### **For Local LLM (Worker):**

1. **Always archive sources** - Use `archive_source` for every `scrape_webpage`
2. **Use appropriate tools** - Statistical data? Use `calculate_statistics`
3. **Log everything** - Structured logging helps supervisor review
4. **Be honest** - Report what you found vs. what you couldn't find
5. **Cite sources** - Include URLs, dates, credibility in all findings

### **For Aleksander (Supervisor):**

1. **Review thoroughly** - Check tool usage, source quality, analytical rigor
2. **Be specific in guidance** - "Find 3 more sources" not "do better"
3. **Praise good work** - Acknowledge when local LLM does well
4. **Set clear standards** - Define what "A" grade looks like
5. **Final synthesis** - Add professional polish to final reports

---

## 💰 Cost Comparison

### **Traditional Cloud-Only:**

**Example:** 100 investigations/month

```
Investigation: 500k tokens average
Cost: $15/million tokens (Claude)

Total: 100 × 500k × $15/1M = $750/month
Annual: $9,000
```

### **Hybrid On-Prem:**

```
Local LLM (execution): $0 (one-time hardware investment)
Aleksander (supervision): ~50k tokens/investigation
Cost: 100 × 50k × $15/1M = $75/month
Annual: $900

Savings: $8,100/year (90% reduction!) 💰
```

**Plus:**
- ✅ Privacy (data stays local)
- ✅ No rate limits
- ✅ Full control
- ✅ Professional quality maintained

---

## 🚀 Next Steps

### **Phase 1: Test Basic System (Today)**

1. ✅ Install LMStudio
2. ✅ Load model (Mixtral 8x7B recommended)
3. ✅ Run `local_orchestrator.py` test
4. ✅ Run `supervisor_interface.py` review
5. ✅ Verify full workflow works

### **Phase 2: Real Investigation (This Week)**

1. 🎯 Choose real investigation topic
2. 🎯 Aleksander creates detailed task
3. 🎯 Local LLM executes
4. 🎯 Aleksander reviews and iterates
5. 🎯 Synthesize professional final report

**Suggested First Investigation:**
- Analyze CPK public data (less sensitive than Telus initially)
- Scrape CPK official website
- Collect 10+ sources
- Statistical analysis of published data
- Full source attribution
- **Prove system works end-to-end**

### **Phase 3: Advanced Features (Next 2 Weeks)**

1. 🔨 Add Image Intelligence Toolkit
2. 🔨 Add Geolocation Toolkit
3. 🔨 Integrate with local databases (PostgreSQL, Qdrant)
4. 🔨 Automated guidance implementation
5. 🔨 Multi-investigation orchestration

---

## 📚 Additional Resources

**Documentation:**
- Full Architecture: `docs/architecture/HYBRID_ONPREM_INTELLIGENCE_SYSTEM.md`
- Source Attribution Protocol: `docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md`
- Toolkits Documentation: `agents/analytical/tools/README.md`

**Code:**
- Local Orchestrator: `local_orchestrator.py`
- Supervisor Interface: `supervisor_interface.py`
- Scraping Toolkit: `agents/analytical/tools/scraping_toolkit.py`
- Mathematical Toolkit: `agents/analytical/tools/mathematical_toolkit.py`

**Logs & Results:**
- Investigation Logs: `./logs/local_llm/`
- Results: `./shared_workspace/results/`
- Quality Reports: `./shared_workspace/reports/`
- Guidance: `./shared_workspace/guidance/`

---

## 🎯 Success Criteria

**System is successful when:**

1. ✅ Local LLM executes investigations autonomously
2. ✅ All sources properly attributed and archived
3. ✅ Aleksander can effectively review and guide
4. ✅ Quality maintained at Bellingcat standards
5. ✅ Cost reduced by 80-90%
6. ✅ Privacy preserved (sensitive data stays local)
7. ✅ Faster than cloud-only (no rate limits)

**Ready to start? Run `python local_orchestrator.py`!** 🚀

---

**Questions? Issues? Artur - just ask Aleksander in Cursor!** 🎯
