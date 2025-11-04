# Analytical Team - Quick Start Guide

**For:** All Destiny Team Members  
**Author:** Helena Kowalczyk (Knowledge Manager) & Aleksander Nowak  
**Date:** November 3, 2025  

---

## 🚀 **What is the Analytical Team?**

A **9-agent intelligence and research team** that complements our technical capabilities with:
- 🔍 OSINT & Investigation
- 💰 Financial Analysis & Forensics
- 📊 Market Research & Competitive Intelligence
- ⚖️ Legal Research & Compliance
- 📈 Data Analysis & Statistics
- 📝 Professional Report Writing

---

## **👥 Meet the Team (5-Second Intro)**

| Agent | Use When You Need... | Example |
|-------|---------------------|---------|
| **Viktor Kovalenko** | Investigation planning, strategy | "Plan investigation of Company XYZ" |
| **Elena Volkov** | OSINT, background checks | "Research competitor's social media presence" |
| **Marcus Chen** | Financial analysis, fraud detection | "Analyze Company ABC's financial health" |
| **Sofia Martinez** | Market research, competitor intel | "Research market for new feature idea" |
| **Adrian Kowalski** | Legal research, compliance | "Review open-source license compatibility" |
| **Maya Patel** | Data analysis, statistics | "Analyze user behavior patterns" |
| **Lucas Rivera** | Reports, summaries, presentations | "Create executive summary of findings" |
| **Damian Rousseau** | Challenge ideas, find flaws | "What could go wrong with this plan?" |
| **Alex Morgan** | Document processing, search | "Index 1000 PDFs for searchability" |

---

## **🎯 When to Use Analytical vs Technical Team**

### **Use Technical Team when you need:**
- ✅ Software development
- ✅ Database design
- ✅ System architecture
- ✅ UI/UX design
- ✅ DevOps & infrastructure
- ✅ QA testing

### **Use Analytical Team when you need:**
- ✅ Market research
- ✅ Competitive intelligence
- ✅ Financial analysis
- ✅ Legal research
- ✅ OSINT / investigations
- ✅ Data analysis & statistics
- ✅ Professional reports

### **Use BOTH when project requires:**
- 🤝 Build + Research (e.g., "Research market then build MVP")
- 🤝 Investigation + Dashboard (e.g., "Intelligence platform")
- 🤝 Compliance + Automation (e.g., "Automated compliance checking")

---

## **💻 How to Use (Code Examples)**

### **Option 1: Direct Team Usage**

```python
from agents.analytical.analytical_team import AnalyticalTeam

# Initialize team
team = AnalyticalTeam()

# Launch investigation
results = team.investigate(
    subject="Company XYZ",
    investigation_type="comprehensive",  # or "osint", "financial", "legal"
    priority="high"
)

# Results from all relevant agents
print(results.keys())  # ['planning', 'osint', 'financial', 'market', 'legal', ...]
```

### **Option 2: Delegate to Specific Agent**

```python
# Delegate to Sofia for market research
result = team.delegate_to_agent(
    agent_name="Sofia Martinez",
    task_title="Market Analysis Q4",
    task_description="Analyze market trends for Q4 2024 in AI sector",
    priority="medium"
)

print(result.thoughts)  # Sofia's analysis
```

### **Option 3: Cross-Team Delegation**

```python
from agents.cross_team_communication import connect_teams

# Connect both teams
bridge = connect_teams(technical_team, analytical_team)

# Technical team asks analytical team for help
result = bridge.delegate_cross_team(
    from_agent="Aleksander Nowak",
    to_agent="Marcus Chen",
    task_title="Financial ROI Analysis",
    task_description="Calculate ROI for new infrastructure investment"
)
```

### **Option 4: Find Expert Across Teams**

```python
# Find financial experts
experts = bridge.find_expert("financial analysis")
# Returns: [{"name": "Marcus Chen", "team": "analytical", ...}]

# Find legal experts
legal = bridge.find_expert("legal")
# Returns: [{"name": "Adrian Kowalski", "team": "analytical", ...}]

# Find data experts (searches both teams!)
data = bridge.find_expert("data")
# Returns: [{"name": "Maya Patel"}, {"name": "Maria Wiśniewska"}, {"name": "Alex Morgan"}]
```

---

## **📋 Common Use Cases**

### **Use Case 1: Market Research Before Feature**

```python
# Before building new feature, research market

# Step 1: Ask Sofia for market research
market_result = team.delegate_to_agent(
    agent_name="Sofia Martinez",
    task_title="AI Feature Market Research",
    task_description="Research market demand for AI-powered code completion",
    priority="high"
)

# Step 2: Ask Marcus for financial viability
financial_result = team.delegate_to_agent(
    agent_name="Marcus Chen",
    task_title="AI Feature ROI Analysis",
    task_description="Estimate ROI and pricing strategy",
    priority="high"
)

# Step 3: Use findings for technical planning
# (Pass to Aleksander/Katarzyna for architecture)
```

### **Use Case 2: Competitive Intelligence**

```python
# Research competitor

result = team.delegate_to_agent(
    agent_name="Elena Volkov",
    task_title="Competitor OSINT",
    task_description="Research Competitor X's technical stack, team size, funding, social media",
    priority="medium"
)

# Elena uses OSINT toolkit to gather intelligence
# Returns: Comprehensive competitor profile
```

### **Use Case 3: Legal Compliance Check**

```python
# Before launching feature, check compliance

result = team.delegate_to_agent(
    agent_name="Adrian Kowalski",
    task_title="GDPR Compliance Check",
    task_description="Assess GDPR compliance for user data processing in new feature",
    priority="high"
)

# Adrian reviews regulations and provides compliance checklist
```

### **Use Case 4: Data Analysis**

```python
# Analyze user behavior data

result = team.delegate_to_agent(
    agent_name="Maya Patel",
    task_title="User Behavior Analysis",
    task_description="Analyze user engagement patterns and identify drop-off points",
    priority="medium"
)

# Maya provides statistical analysis + visualizations
```

### **Use Case 5: Executive Report**

```python
# After investigation, generate executive summary

result = team.delegate_to_agent(
    agent_name="Lucas Rivera",
    task_title="Executive Summary",
    task_description="Synthesize all findings into 2-page executive summary for board",
    priority="high"
)

# Lucas creates professional PDF report
```

---

## **🔒 Privacy & Security**

### **When Analytical Team Uses LOCAL Processing:**

✅ **Always LOCAL (guaranteed):**
- Elena Volkov (OSINT - sensitive investigations)
- Marcus Chen (Financial - confidential data)
- Adrian Kowalski (Legal - attorney-client privilege)
- Viktor Kovalenko (Orchestrator - sees all)
- Damian Rousseau (Devil's Advocate - full context)
- Alex Morgan (Technical Liaison - sensitive docs)

✅ **What "LOCAL" means:**
- All AI processing on your machine (LM Studio)
- gpt-oss-20b model (20B params, 44K context)
- Zero external API calls
- Complete data privacy
- GDPR/HIPAA compliant
- No usage tracking
- No API costs

---

## **🗄️ Where Knowledge is Stored**

| Database | What's Stored | How to Access |
|----------|--------------|---------------|
| **PostgreSQL** | Agent registry, capabilities, routing | SQL queries |
| **Neo4j** | Team relationships, collaboration paths | Cypher queries |
| **Qdrant** | Documentation (semantic search) | Vector search |
| **Redis** | Quick reference, status | Key-value lookup |
| **Elasticsearch** | Documents processed by team | Full-text search |

### **Quick Lookups:**

```python
# Redis: Fast access
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
overview = json.loads(r.get('knowledge:analytical-team:overview'))

# PostgreSQL: Structured queries
cursor.execute("SELECT * FROM analytical_agents WHERE toolkit IS NOT NULL;")

# Neo4j: Relationship queries
MATCH (a:Agent {team: 'analytical'})-[:PROVIDES]->(c:Capability)
RETURN a.name, c.name

# Qdrant: Semantic search
results = qdrant.search("How to use OSINT capabilities?")
```

---

## **❓ FAQ**

**Q: How is analytical team different from technical team?**  
A: Technical = build software. Analytical = research, investigate, analyze. Both can collaborate!

**Q: Can I use both teams on same project?**  
A: Absolutely! Use cross-team bridge to assemble hybrid teams.

**Q: Is analytical team data private?**  
A: Yes! Uses local LLM (gpt-oss-20b) by default. No external API calls.

**Q: How do I find the right agent?**  
A: Use `bridge.find_expert("expertise")` or check the quick reference table above.

**Q: What if I need a capability not listed?**  
A: Ask Viktor (Analytical Orchestrator) - he'll coordinate or suggest alternatives.

**Q: Can analytical agents access our technical databases?**  
A: Yes - they share infrastructure but use separate PROJECT_ID for isolation.

**Q: How fast are analytical team responses?**  
A: 2-60 seconds depending on complexity (local LLM with 44K context).

**Q: What's the 44K context window mean?**  
A: Can analyze ~33,000 words (~66 pages) in ONE request - entire documents!

---

## **📚 Further Reading**

- `ANALYTICAL_TEAM_ANNOUNCEMENT.md` - Official announcement
- `agents/analytical/TEAM_PROFILE.md` - Detailed agent profiles
- `agents/analytical/CROSS_TEAM_INTEGRATION.md` - Collaboration guide
- `agents/analytical/PRIVACY_ARCHITECTURE.md` - Privacy details
- `HELENA_ANALYTICAL_TEAM_DOCUMENTATION_TASK.md` - Helena's documentation task

---

## **🆘 Need Help?**

**Questions about:**
- Analytical capabilities → Viktor Kovalenko (Orchestrator)
- Technical integration → Alex Morgan (Technical Liaison)
- Cross-team collaboration → Aleksander Nowak or Viktor Kovalenko
- Documentation → Helena Kowalczyk (Knowledge Manager)

---

**Welcome to the Analytical Team! 18 agents working together! 🎉**
