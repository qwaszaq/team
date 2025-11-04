# 🏗️ Deep Research System - Technical Architecture

**Document Type:** Technical Implementation Specification  
**Date:** 2025-11-04  
**Lead:** Maria Wiśniewska (Software Architect)  
**Contributors:** Tomasz, Piotr, Michał (Core Team)

---

## 📋 Technical Overview

This document provides detailed technical specifications for implementing the Deep Research Agent system.

---

## 🎯 System Requirements

### **Functional Requirements:**
- FR1: Process 1M+ tokens of input data
- FR2: Generate 50k token reports
- FR3: Multi-agent coordination
- FR4: Real-time progress tracking
- FR5: Quality assurance gates
- FR6: Source attribution

### **Non-Functional Requirements:**
- NFR1: Performance: Complete research in 5-8 hours
- NFR2: Cost: < $70 per report
- NFR3: Accuracy: 95%+ fact accuracy
- NFR4: Scalability: Support 10 concurrent research tasks
- NFR5: Reliability: 99% uptime
- NFR6: Security: Enterprise-grade data protection

---

## 🏗️ Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│  (CLI / Web / API)                                             │
└───────────────────────────┬────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                          │
│  ┌─────────────────┐  ┌───────────────┐  ┌────────────────┐ │
│  │  Task Scheduler │  │ Agent Manager │  │ State Machine  │ │
│  └─────────────────┘  └───────────────┘  └────────────────┘ │
└───────────────────────────┬───────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌──────────────────────┐          ┌──────────────────────────┐
│    Agent Layer       │          │    Data Layer            │
│                      │          │                          │
│ ┌────────────────┐  │          │ ┌──────────────────────┐ │
│ │ Document Agent │  │◄─────────┤ │ Vector Store (Qdrant)│ │
│ └────────────────┘  │          │ └──────────────────────┘ │
│ ┌────────────────┐  │          │ ┌──────────────────────┐ │
│ │ OSINT Agent    │  │◄─────────┤ │ PostgreSQL           │ │
│ └────────────────┘  │          │ └──────────────────────┘ │
│ ┌────────────────┐  │          │ ┌──────────────────────┐ │
│ │ Financial      │  │◄─────────┤ │ Redis Cache          │ │
│ │ Analyst        │  │          │ └──────────────────────┘ │
│ └────────────────┘  │          │ ┌──────────────────────┐ │
│ ┌────────────────┐  │          │ │ S3 / File Storage    │ │
│ │ Market Analyst │  │◄─────────┤ └──────────────────────┘ │
│ └────────────────┘  │          └──────────────────────────┘
│ ┌────────────────┐  │
│ │ Strategic      │  │                  ┌──────────────┐
│ │ Analyst        │  │◄─────────────────┤ LLM Provider │
│ └────────────────┘  │                  │  (Claude)    │
│ ┌────────────────┐  │                  └──────────────┘
│ │ QC Agent       │  │
│ └────────────────┘  │                  ┌──────────────┐
│ ┌────────────────┐  │◄─────────────────┤ External APIs│
│ │ Synthesis      │  │                  │ (Finance)    │
│ │ Agent          │  │                  └──────────────┘
│ └────────────────┘  │
└──────────────────────┘
```

---

## 💾 Data Architecture

### **Storage Strategy:**

#### **1. Vector Store (Qdrant)**
```python
# Use case: Semantic search over documents
collection_config = {
    "vectors": {
        "size": 3072,  # text-embedding-3-large
        "distance": "Cosine"
    },
    "payload_schema": {
        "text": "text",
        "source": "keyword",
        "date": "datetime",
        "chunk_id": "integer",
        "doc_type": "keyword"
    }
}

# Example: Store document chunks
qdrant.upsert(
    collection_name="research_documents",
    points=[
        {
            "id": chunk_id,
            "vector": embedding,
            "payload": {
                "text": chunk_text,
                "source": "Tesla_10K_2023.pdf",
                "date": "2023-02-01",
                "chunk_id": i,
                "doc_type": "financial_report"
            }
        }
    ]
)

# Example: Semantic search
results = qdrant.search(
    collection_name="research_documents",
    query_vector=query_embedding,
    limit=50,
    query_filter={
        "must": [
            {"key": "date", "range": {"gte": "2020-01-01"}},
            {"key": "doc_type", "match": {"value": "financial_report"}}
        ]
    }
)
```

#### **2. PostgreSQL (Structured Data)**
```sql
-- Schema design
CREATE TABLE research_tasks (
    task_id UUID PRIMARY KEY,
    user_query TEXT NOT NULL,
    status VARCHAR(50),  -- planning, collecting, analyzing, complete
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    cost_usd DECIMAL(10,2),
    token_count INTEGER
);

CREATE TABLE agent_runs (
    run_id UUID PRIMARY KEY,
    task_id UUID REFERENCES research_tasks(task_id),
    agent_type VARCHAR(50),  -- document, osint, financial, etc
    status VARCHAR(50),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10,2),
    result_summary TEXT
);

CREATE TABLE data_sources (
    source_id UUID PRIMARY KEY,
    task_id UUID REFERENCES research_tasks(task_id),
    source_type VARCHAR(50),  -- pdf, api, web
    source_url TEXT,
    collected_at TIMESTAMP,
    token_count INTEGER,
    credibility_score DECIMAL(3,2)  -- 0.0 to 1.0
);

CREATE TABLE findings (
    finding_id UUID PRIMARY KEY,
    task_id UUID REFERENCES research_tasks(task_id),
    agent_type VARCHAR(50),
    finding_type VARCHAR(50),  -- metric, trend, red_flag, insight
    content TEXT,
    confidence_score DECIMAL(3,2),
    sources TEXT[],  -- Array of source_ids
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE quality_checks (
    check_id UUID PRIMARY KEY,
    task_id UUID REFERENCES research_tasks(task_id),
    check_type VARCHAR(50),  -- fact_check, consistency, bias
    passed BOOLEAN,
    issues TEXT,
    checked_at TIMESTAMP
);
```

#### **3. Redis Cache**
```python
# Use case: Cache expensive API calls and intermediate results
cache_strategy = {
    "stock_prices": ttl=86400,  # 24 hours
    "news_articles": ttl=3600,  # 1 hour
    "financial_statements": ttl=2592000,  # 30 days
    "embeddings": ttl=604800,  # 7 days
    "agent_outputs": ttl=3600  # 1 hour
}

# Example: Cache stock data
def get_stock_data(ticker, start_date, end_date):
    cache_key = f"stock:{ticker}:{start_date}:{end_date}"
    
    # Check cache
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from API
    data = yahoo_finance_api.get_history(ticker, start_date, end_date)
    
    # Cache for 24 hours
    redis.setex(cache_key, 86400, json.dumps(data))
    
    return data
```

---

## 🔧 Agent Implementation

### **Base Agent Class:**

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import anthropic

class BaseResearchAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.vector_store = QdrantClient(...)
        self.db = PostgreSQLConnection(...)
        self.cache = RedisClient(...)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return agent-specific system prompt"""
        pass
    
    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        pass
    
    def call_llm(
        self, 
        context: str, 
        query: str, 
        max_tokens: int = 4000
    ) -> str:
        """Make LLM call with context management"""
        
        # Token count check
        context_tokens = self.count_tokens(context)
        
        if context_tokens > 150000:
            # Use RAG to reduce context
            context = self.retrieve_relevant_context(query, max_tokens=100000)
        
        response = self.llm.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=self.get_system_prompt(),
            messages=[{
                "role": "user",
                "content": f"Context:\n{context}\n\nQuery:\n{query}"
            }]
        )
        
        return response.content[0].text
    
    def retrieve_relevant_context(self, query: str, max_tokens: int) -> str:
        """RAG: Retrieve relevant chunks from vector store"""
        
        # Embed query
        query_embedding = self.get_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(
            collection_name="research_documents",
            query_vector=query_embedding,
            limit=100
        )
        
        # Collect chunks until token limit
        context_chunks = []
        total_tokens = 0
        
        for result in results:
            chunk = result.payload["text"]
            chunk_tokens = self.count_tokens(chunk)
            
            if total_tokens + chunk_tokens <= max_tokens:
                context_chunks.append(chunk)
                total_tokens += chunk_tokens
            else:
                break
        
        return "\n\n---\n\n".join(context_chunks)
    
    def log_run(self, task_id: str, status: str, result: Dict):
        """Log agent run to database"""
        self.db.execute("""
            INSERT INTO agent_runs (
                task_id, agent_type, status, result_summary,
                input_tokens, output_tokens, cost_usd
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            task_id, self.role, status, json.dumps(result),
            result.get("input_tokens", 0),
            result.get("output_tokens", 0),
            result.get("cost", 0)
        ))
```

### **Example: Financial Analyst Agent:**

```python
class FinancialAnalystAgent(BaseResearchAgent):
    def __init__(self):
        super().__init__(name="FinancialAnalyst", role="financial_analyst")
    
    def get_system_prompt(self) -> str:
        return """You are an expert financial analyst with CFA certification.
        
Your role:
- Analyze financial statements in depth
- Calculate and interpret financial ratios
- Identify trends, patterns, and anomalies
- Detect red flags (accounting irregularities, unsustainable practices)
- Provide evidence-based insights

Guidelines:
- Be precise with numbers
- Cite specific financial statements
- Show calculations
- Consider industry context
- Identify both strengths and weaknesses
- Support conclusions with data
"""
    
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial data"""
        
        task_id = task["task_id"]
        company = task["company"]
        ticker = task["ticker"]
        years = task.get("years", 10)
        
        # 1. Retrieve financial data
        financial_data = self.retrieve_financial_data(ticker, years)
        
        # 2. Calculate metrics
        metrics = self.calculate_metrics(financial_data)
        
        # 3. LLM analysis
        analysis_prompt = f"""
Analyze the following financial data for {company} ({ticker}) 
over {years} years:

{json.dumps(metrics, indent=2)}

Provide comprehensive analysis covering:
1. Profitability trends
2. Liquidity position
3. Solvency concerns
4. Operational efficiency
5. Growth trajectory
6. Red flags or concerns
7. Key insights

Format: Structured analysis with clear sections.
Length: 8,000-10,000 tokens
"""
        
        analysis = self.call_llm(
            context=json.dumps(financial_data, indent=2),
            query=analysis_prompt,
            max_tokens=10000
        )
        
        # 4. Store findings
        self.store_findings(task_id, analysis, metrics)
        
        # 5. Log run
        self.log_run(task_id, "completed", {
            "metrics_calculated": len(metrics),
            "analysis_length": len(analysis)
        })
        
        return {
            "status": "completed",
            "metrics": metrics,
            "analysis": analysis
        }
    
    def calculate_metrics(self, financial_data: Dict) -> Dict:
        """Calculate financial ratios"""
        metrics = {}
        
        for year, data in financial_data.items():
            income = data["income_statement"]
            balance = data["balance_sheet"]
            cash_flow = data["cash_flow"]
            
            metrics[year] = {
                # Profitability
                "gross_margin": income["gross_profit"] / income["revenue"],
                "operating_margin": income["operating_income"] / income["revenue"],
                "net_margin": income["net_income"] / income["revenue"],
                "roe": income["net_income"] / balance["shareholders_equity"],
                "roa": income["net_income"] / balance["total_assets"],
                
                # Liquidity
                "current_ratio": balance["current_assets"] / balance["current_liabilities"],
                "quick_ratio": (balance["current_assets"] - balance["inventory"]) / balance["current_liabilities"],
                
                # Solvency
                "debt_to_equity": balance["total_debt"] / balance["shareholders_equity"],
                "interest_coverage": income["ebit"] / income["interest_expense"],
                
                # Efficiency
                "asset_turnover": income["revenue"] / balance["total_assets"],
                "inventory_turnover": income["cogs"] / balance["inventory"],
                
                # Cash flow
                "operating_cash_flow": cash_flow["operating_cf"],
                "free_cash_flow": cash_flow["operating_cf"] - cash_flow["capex"]
            }
        
        return metrics
```

---

## 🔄 Workflow Engine

### **State Machine:**

```python
from enum import Enum
from typing import Dict, List, Callable

class ResearchState(Enum):
    CREATED = "created"
    PLANNING = "planning"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    VERIFYING = "verifying"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchWorkflow:
    def __init__(self, task_id: str, user_query: str):
        self.task_id = task_id
        self.user_query = user_query
        self.state = ResearchState.CREATED
        self.agents = self.initialize_agents()
        self.results = {}
    
    def initialize_agents(self) -> Dict:
        return {
            "orchestrator": OrchestratorAgent(),
            "document": DocumentIngestionAgent(),
            "osint": OSINTAgent(),
            "financial": FinancialAnalystAgent(),
            "market": MarketAnalystAgent(),
            "strategic": StrategicAnalystAgent(),
            "qc": QualityControlAgent(),
            "synthesis": SynthesisAgent()
        }
    
    async def execute(self):
        """Execute research workflow"""
        
        try:
            # Phase 1: Planning
            self.transition_to(ResearchState.PLANNING)
            plan = await self.agents["orchestrator"].create_plan(self.user_query)
            
            # Phase 2: Data Collection
            self.transition_to(ResearchState.COLLECTING)
            await self.collect_data(plan)
            
            # Phase 3: Analysis (parallel)
            self.transition_to(ResearchState.ANALYZING)
            await self.run_analyses(plan)
            
            # Phase 4: Quality Control
            self.transition_to(ResearchState.VERIFYING)
            qc_result = await self.agents["qc"].verify(self.results)
            
            if not qc_result["approved"]:
                # Re-run failed analyses
                await self.rerun_failed_analyses(qc_result["issues"])
            
            # Phase 5: Synthesis
            self.transition_to(ResearchState.SYNTHESIZING)
            report = await self.agents["synthesis"].generate_report(self.results)
            
            # Complete
            self.transition_to(ResearchState.COMPLETED)
            return report
            
        except Exception as e:
            self.transition_to(ResearchState.FAILED)
            raise
    
    async def collect_data(self, plan: Dict):
        """Run data collection agents in parallel"""
        tasks = [
            self.agents["document"].process(plan),
            self.agents["osint"].process(plan)
        ]
        results = await asyncio.gather(*tasks)
        self.results["data_collection"] = results
    
    async def run_analyses(self, plan: Dict):
        """Run analyst agents in parallel"""
        tasks = [
            self.agents["financial"].process(plan),
            self.agents["market"].process(plan),
            self.agents["strategic"].process(plan)
        ]
        results = await asyncio.gather(*tasks)
        self.results["analyses"] = results
    
    def transition_to(self, new_state: ResearchState):
        """Transition to new state"""
        print(f"[{self.task_id}] {self.state.value} → {new_state.value}")
        self.state = new_state
        
        # Update database
        self.db.execute("""
            UPDATE research_tasks 
            SET status = %s, updated_at = NOW()
            WHERE task_id = %s
        """, (new_state.value, self.task_id))
```

---

## 🚦 Rate Limiting & Throttling

```python
class RateLimiter:
    def __init__(self):
        self.limits = {
            "anthropic": {
                "requests_per_minute": 50,
                "tokens_per_minute": 40000
            },
            "openai": {
                "requests_per_minute": 500,
                "tokens_per_minute": 200000
            },
            "alpha_vantage": {
                "requests_per_minute": 5
            }
        }
        self.counters = {}
    
    async def acquire(self, service: str, tokens: int = 0):
        """Acquire rate limit token"""
        if service not in self.counters:
            self.counters[service] = {"requests": 0, "tokens": 0, "reset_at": time.time() + 60}
        
        counter = self.counters[service]
        
        # Reset if minute passed
        if time.time() > counter["reset_at"]:
            counter["requests"] = 0
            counter["tokens"] = 0
            counter["reset_at"] = time.time() + 60
        
        # Check limits
        limits = self.limits[service]
        if counter["requests"] >= limits["requests_per_minute"]:
            wait_time = counter["reset_at"] - time.time()
            await asyncio.sleep(wait_time)
            return await self.acquire(service, tokens)
        
        if tokens > 0 and counter["tokens"] + tokens > limits.get("tokens_per_minute", float("inf")):
            wait_time = counter["reset_at"] - time.time()
            await asyncio.sleep(wait_time)
            return await self.acquire(service, tokens)
        
        # Acquire
        counter["requests"] += 1
        counter["tokens"] += tokens
```

---

## 💰 Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.pricing = {
            "claude-3.5-sonnet": {
                "input": 0.003 / 1000,  # $0.003 per 1k tokens
                "output": 0.015 / 1000
            },
            "gpt-4-turbo": {
                "input": 0.01 / 1000,
                "output": 0.03 / 1000
            },
            "text-embedding-3-large": {
                "input": 0.00013 / 1000
            }
        }
    
    def calculate_llm_cost(
        self, 
        model: str, 
        input_tokens: int, 
        output_tokens: int
    ) -> float:
        """Calculate LLM API cost"""
        pricing = self.pricing[model]
        cost = (
            input_tokens * pricing["input"] +
            output_tokens * pricing["output"]
        )
        return cost
    
    def track_task_cost(self, task_id: str):
        """Get total cost for research task"""
        result = self.db.execute("""
            SELECT 
                SUM(cost_usd) as total_cost,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens
            FROM agent_runs
            WHERE task_id = %s
        """, (task_id,))
        
        return result.fetchone()
```

---

## 📊 Monitoring & Observability

```python
import prometheus_client as prom

# Metrics
research_duration = prom.Histogram(
    "research_duration_seconds",
    "Time to complete research",
    ["phase"]
)

agent_duration = prom.Histogram(
    "agent_duration_seconds",
    "Time per agent",
    ["agent_type"]
)

llm_tokens = prom.Counter(
    "llm_tokens_total",
    "Total LLM tokens used",
    ["model", "direction"]  # direction: input/output
)

research_cost = prom.Counter(
    "research_cost_usd",
    "Total cost in USD",
    ["task_id"]
)

quality_score = prom.Histogram(
    "quality_score",
    "Research quality score",
    ["task_id"]
)

# Example usage in agent
@research_duration.time()
def run_analysis_phase(self):
    with agent_duration.labels(agent_type="financial").time():
        result = self.financial_agent.process()
    
    llm_tokens.labels(
        model="claude-3.5-sonnet",
        direction="input"
    ).inc(result["input_tokens"])
    
    llm_tokens.labels(
        model="claude-3.5-sonnet",
        direction="output"
    ).inc(result["output_tokens"])
    
    return result
```

---

## 🔒 Security Implementation

### **API Key Management:**

```python
import boto3
from cryptography.fernet import Fernet

class SecretManager:
    def __init__(self):
        # Use AWS Secrets Manager or similar
        self.client = boto3.client("secretsmanager")
        self.cache = {}
    
    def get_secret(self, secret_name: str) -> str:
        """Retrieve API key from secure vault"""
        if secret_name in self.cache:
            return self.cache[secret_name]
        
        response = self.client.get_secret_value(SecretId=secret_name)
        secret = response["SecretString"]
        
        # Cache for session
        self.cache[secret_name] = secret
        return secret

# Usage
secrets = SecretManager()
anthropic_key = secrets.get_secret("anthropic_api_key")
```

### **Data Encryption:**

```python
class DataEncryption:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt_findings(self, findings: Dict) -> bytes:
        """Encrypt sensitive research findings"""
        json_data = json.dumps(findings)
        encrypted = self.cipher.encrypt(json_data.encode())
        return encrypted
    
    def decrypt_findings(self, encrypted_data: bytes) -> Dict:
        """Decrypt findings"""
        decrypted = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
```

---

## 🚀 Deployment Architecture

### **Option 1: Local Development**
```yaml
# docker-compose.yml
version: "3.8"

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: research_db
      POSTGRES_USER: research_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  research_api:
    build: .
    depends_on:
      - qdrant
      - postgres
      - redis
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    ports:
      - "8000:8000"

volumes:
  qdrant_data:
  postgres_data:
```

### **Option 2: Production (AWS)**
```
┌────────────────────────────────────────┐
│           Route 53 (DNS)               │
└──────────────┬─────────────────────────┘
               │
┌──────────────▼─────────────────────────┐
│      CloudFront (CDN)                  │
└──────────────┬─────────────────────────┘
               │
┌──────────────▼─────────────────────────┐
│   Application Load Balancer            │
└────────┬──────────────┬────────────────┘
         │              │
    ┌────▼────┐    ┌───▼─────┐
    │ ECS     │    │ ECS     │
    │ Task 1  │    │ Task 2  │
    └────┬────┘    └───┬─────┘
         │              │
    ┌────▼──────────────▼────┐
    │     RDS PostgreSQL      │
    └─────────────────────────┘
    
    ┌─────────────────────────┐
    │   ElastiCache Redis     │
    └─────────────────────────┘
    
    ┌─────────────────────────┐
    │   Qdrant Cloud          │
    └─────────────────────────┘
    
    ┌─────────────────────────┐
    │   S3 (Documents)        │
    └─────────────────────────┘
```

---

## ✅ Implementation Checklist

### **Phase 1: MVP (Weeks 1-4)**
- [ ] Set up infrastructure (Docker Compose)
- [ ] Implement base agent class
- [ ] Build document ingestion agent
- [ ] Build financial analyst agent
- [ ] Build synthesis agent
- [ ] Create basic workflow
- [ ] Test on sample company

### **Phase 2: Core Agents (Weeks 5-8)**
- [ ] Build OSINT agent
- [ ] Build market analyst agent
- [ ] Build strategic analyst agent
- [ ] Build quality control agent
- [ ] Integrate all agents
- [ ] Add parallel processing

### **Phase 3: Production (Weeks 9-12)**
- [ ] Web UI development
- [ ] API endpoints
- [ ] Authentication & authorization
- [ ] Cost optimization
- [ ] Performance tuning
- [ ] Documentation
- [ ] Deployment to production

---

## 📈 Success Metrics

**Target KPIs:**
- Research completion time: < 8 hours
- Cost per report: < $70
- Fact accuracy: > 95%
- User satisfaction: > 4.5/5
- System uptime: > 99%

---

## 🎯 Conclusion

This architecture provides:
- ✅ Scalable multi-agent system
- ✅ Efficient token management
- ✅ Cost-effective processing
- ✅ High-quality outputs
- ✅ Production-ready design

**Status:** Ready for implementation

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-04  
**Next Review:** After MVP completion
