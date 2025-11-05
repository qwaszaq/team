# 🚀 GETTING STARTED - Destiny Analytical System

**Quick guide to get up and running in 5 minutes!**

---

## ⚡ FASTEST START (Recommended)

```bash
# 1. Run automated setup
./setup.sh

# 2. Add your Claude API key (optional, for real supervision)
nano .env  # Add ANTHROPIC_API_KEY=your-key-here

# 3. Check system health
python3 health_check.py

# 4. Run live demo
python3 demo.py
```

**Done! System is operational! 🎉**

---

## 📋 MANUAL SETUP (Step by Step)

### **Step 1: Prerequisites**

Check you have:
```bash
python3 --version  # Need 3.10+
docker --version   # Optional, for databases
```

### **Step 2: Install Dependencies**

```bash
pip3 install -r requirements.txt --break-system-packages
# or
pip3 install -r requirements.txt
```

### **Step 3: Configure Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit .env
nano .env

# Add at minimum:
ANTHROPIC_API_KEY=your-key-here  # For real Claude supervision
LMSTUDIO_HOST=192.168.200.226    # Your LMStudio host
```

### **Step 4: Start Databases (Optional)**

```bash
# Start all databases
docker-compose up -d

# Or start specific databases
docker-compose up -d postgres
docker-compose up -d qdrant
docker-compose up -d elasticsearch
docker-compose up -d neo4j

# Check status
docker-compose ps
```

### **Step 5: Verify System**

```bash
# Run health check
python3 health_check.py
```

Expected output:
```
✅ LLM Client
✅ Embedding Pipeline
✅ Base Agents
✅ Additional Agents
✅ Orchestrator
...
OVERALL STATUS: 🟢 SYSTEM OPERATIONAL
```

---

## 🎯 QUICK TESTS

### **Test Individual Components:**

```bash
# Test LLM
python3 src/llm/lmstudio_client.py

# Test Embeddings
python3 src/data/embedding_pipeline.py

# Test Agents
python3 src/agents/base_agent.py

# Test Additional Agents
python3 src/agents/additional_agents.py

# Test Supervision
python3 src/supervision/claude_supervisor.py
```

### **Run Integration Tests:**

```bash
python3 tests/integration/test_end_to_end.py
```

Expected:
```
🎉 ALL TESTS PASSED! SYSTEM IS OPERATIONAL! 🎉
```

---

## 🚀 RUN YOUR FIRST ANALYSIS

### **Option 1: Run the Demo**

```bash
python3 demo.py
```

This will show:
- Simple analysis
- Multi-agent orchestration
- Specialized agents
- Quality supervision

### **Option 2: Python Script**

```python
from src.agents.orchestrator import MultiAgentOrchestrator

# Initialize
orchestrator = MultiAgentOrchestrator()

# Your documents
documents = [
    {
        "id": "doc_001",
        "content": "Revenue: $5M, up 25% YoY. Profit margin: 32%.",
        "type": "financial"
    }
]

# Run analysis
analysis = orchestrator.process_case(
    case_id="my_first_case",
    title="My First Analysis",
    documents=documents,
    analysis_types=["financial", "risk"]
)

# View results
print(analysis.synthesis)
```

### **Option 3: Use Specific Agents**

```python
from src.agents.base_agent import FinancialAnalystAgent, Task
from datetime import datetime

# Create agent
agent = FinancialAnalystAgent()

# Create task
task = Task(
    task_id="task_001",
    title="Analyze Q4",
    description="Review Q4 financials",
    task_type="financial",
    data={"revenue": "$5M", "growth": "25%"},
    created_at=datetime.now()
)

# Execute
result = agent.execute(task)
print(result.output['summary'])
```

---

## 🔧 COMMON TASKS

### **Add Claude Supervision (Real)**

```python
from src.supervision.claude_api_supervisor import ClaudeAPISupervisor

# Make sure ANTHROPIC_API_KEY is in .env
supervisor = ClaudeAPISupervisor()

# Review agent work
review = supervisor.review_task(
    task_id="task_001",
    agent_name="Financial Analyst",
    agent_role="financial",
    task_description="Financial analysis",
    agent_output={"summary": "..."},
    confidence=0.85
)

print(supervisor.format_review(review))
```

### **Use All 10 Agents**

```python
from src.agents.additional_agents import get_agent

# Get any agent
financial = get_agent("financial")
legal = get_agent("legal")
risk = get_agent("risk")
data_science = get_agent("data_science")
devops = get_agent("devops")
security = get_agent("security")
product = get_agent("product")
qa = get_agent("qa")
architecture = get_agent("architecture")
documentation = get_agent("documentation")

# All work the same way!
```

### **Check Configuration**

```python
from config import config

# Print all settings
config.print_config()

# Check specific setting
print(f"LMStudio: {config.LMSTUDIO_HOST}:{config.LMSTUDIO_PORT}")
print(f"Claude API: {'✅' if config.ANTHROPIC_API_KEY else '❌'}")
```

---

## 🐛 TROUBLESHOOTING

### **Issue: "Module not found"**

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --break-system-packages
```

### **Issue: "LMStudio not responding"**

```bash
# Check LMStudio is running
curl http://192.168.200.226:1234/v1/models

# Update host in .env if different
LMSTUDIO_HOST=your-actual-host
```

### **Issue: "Database connection failed"**

```bash
# Start databases
docker-compose up -d

# Wait for them to be ready
sleep 15

# Check status
docker-compose ps
```

### **Issue: "ANTHROPIC_API_KEY not set"**

```bash
# Add to .env
echo "ANTHROPIC_API_KEY=your-key-here" >> .env

# Or set temporarily
export ANTHROPIC_API_KEY=your-key-here
```

---

## 📚 NEXT STEPS

### **Learn More:**
- **README.md** - Complete documentation
- **QUICK_START.md** - Detailed quick start
- **COMPLETE_SYSTEM_OVERVIEW.md** - Full architecture

### **Advanced Topics:**
- Setting up all 4 databases
- Configuring production deployment
- Using Qdrant for large-scale cases
- Integrating with CI/CD

### **Get Help:**
- Check `COMPREHENSIVE_STATUS_REPORT.md` for system status
- Run `python3 health_check.py` for diagnostics
- Review test results in `TEST_RESULTS_SUMMARY.md`

---

## ✅ VERIFICATION CHECKLIST

Before deploying to production:

- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` configured (especially `ANTHROPIC_API_KEY`)
- [ ] LMStudio running and accessible
- [ ] Health check passing
- [ ] Integration tests passing
- [ ] Demo runs successfully
- [ ] Databases started (if needed)

---

## 🎉 YOU'RE READY!

**System Status: 🟢 OPERATIONAL**

You can now:
✅ Process documents  
✅ Run multi-agent analysis  
✅ Get AI supervision  
✅ Use all 10 specialized agents  
✅ Deploy to production  

**Happy analyzing!** 🚀

---

*Quick commands:*
```bash
./setup.sh              # Automated setup
python3 health_check.py # Check system
python3 demo.py         # Run demo
python3 tests/integration/test_end_to_end.py  # Test
```
