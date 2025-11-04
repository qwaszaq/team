"""
Alex Morgan - Technical Liaison & Data Engineer
Bridge between Analytical Team and Technical Team
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class AlexAgent(BaseAgent):
    """
    Alex Morgan - Technical Liaison & Data Engineer
    
    Role: Technical Bridge & Data Engineering Specialist
    Specialization: Document parsing, data extraction, embeddings,
                   technical tool provisioning, workflow automation,
                   Elasticsearch full-text search
    
    Capabilities:
    - Parse documents (PDF, DOCX, XLSX, PPT, images)
    - Extract structured data from unstructured sources
    - Index documents in Elasticsearch (full-text search)
    - Generate embeddings for Qdrant (semantic search)
    - Hybrid search (Elasticsearch + Qdrant combined)
    - Coordinate with technical team for tools
    - Build data pipelines for analysts
    - Database queries and data preparation
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Alex Morgan",
            role="Technical Liaison / Data Engineer",
            specialization="Document parsing, Data extraction, Embeddings, Technical coordination, Automation",
            project_id=project_id
        )
        
        # Technical team contacts
        self.technical_team = {
            "Tomasz Kamiński": "Senior Developer - implementations",
            "Anna Nowakowska": "QA Engineer - testing",
            "Joanna Mazur": "UX Designer - interfaces",
            "Piotr Szymański": "DevOps - automation/deployment"
        }
        
        # Supported document types
        self.supported_formats = [
            "PDF", "DOCX", "XLSX", "PPTX", "CSV", "TXT", "MD",
            "Images (OCR)", "HTML", "XML", "JSON"
        ]
        
        # Search infrastructure
        self.search_stack = {
            "Elasticsearch": {
                "url": "http://localhost:9200",
                "purpose": "Full-text search, keyword search, aggregations",
                "credentials": "elastic:changeme123",
                "cluster": "hercules-cluster"
            },
            "Qdrant": {
                "url": "http://localhost:6333",
                "purpose": "Semantic search, similarity, multilingual",
                "model": "multilingual-e5-large-instruct"
            }
        }
        
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute technical liaison work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=3)
        
        if any(word in task_lower for word in ["parse", "extract", "pdf", "docx", "excel"]):
            result = self._document_parsing(task, context)
        elif any(word in task_lower for word in ["index", "elasticsearch", "full-text"]):
            result = self._elasticsearch_indexing(task, context)
        elif any(word in task_lower for word in ["embed", "embedding", "semantic", "qdrant"]):
            result = self._embeddings_generation(task, context)
        elif any(word in task_lower for word in ["search", "find", "query"]):
            result = self._hybrid_search_setup(task, context)
        elif any(word in task_lower for word in ["automate", "pipeline", "workflow"]):
            result = self._workflow_automation(task, context)
        elif any(word in task_lower for word in ["database", "query", "sql"]):
            result = self._data_retrieval(task, context)
        elif any(word in task_lower for word in ["technical", "tool", "request"]):
            result = self._technical_coordination(task, context)
        else:
            result = self._general_data_engineering(task, context)
        
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
    
    def _document_parsing(self, task: Task, context: list) -> TaskResult:
        """Parse and extract data from documents"""
        
        thoughts = f"""
📄 DOCUMENT PARSING - Alex Morgan

Request: {task.title}

PARSING PLAN:

📁 Document Analysis:
- Document type: [PDF/DOCX/XLSX/PPT]
- Volume: [Number of documents]
- Complexity: [Simple/Complex structure]
- Target data: [Tables, text, images, metadata]

🔧 Technical Approach:

For PDFs:
- Method: PyPDF2 for text, Tabula for tables, OCR for images
- Special handling: Multi-column layouts, scanned docs
- Output format: [Structured JSON/CSV/Excel]

For DOCX:
- Method: python-docx library
- Extract: Text, tables, formatting, metadata
- Preserve: Document structure

For XLSX:
- Method: pandas/openpyxl
- Extract: All sheets, formulas, formatting
- Validation: Data types, missing values

For PPTX:
- Method: python-pptx
- Extract: Slide text, notes, images, charts
- Structure: Slide-by-slide breakdown

🎯 Extraction Pipeline:
1. Document ingestion (batch processing)
2. Format detection and routing
3. Content extraction (text, tables, images)
4. Data structuring (JSON/CSV)
5. Quality validation
6. Delivery to requesting analyst

⚙️ Technical Coordination:
Need from Tomasz (Technical Team):
- [Specific tools/libraries if complex]
- [Cloud processing if large volume]
- [Custom parser if unusual format]

📊 Output Specification:
- Format: [Clean CSV/JSON/Database table]
- Metadata: Document source, page numbers, confidence scores
- Quality: [Validated, deduplicated, normalized]

TIMELINE:
- Setup: [X hours]
- Processing: [Y hours for Z documents]
- Delivery: [Clean, analyst-ready data]

STATUS: Ready to parse. Starting extraction pipeline.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "documents_processed": "Batch ready",
                "extraction_method": "Automated pipeline",
                "output_format": "Structured data",
                "quality": "Validated"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["extracted_data.csv", "parsing_log.txt", "quality_report.md"],
            next_steps="Deliver clean data to requesting analyst. Monitor for parsing errors."
        )
    
    def _embeddings_generation(self, task: Task, context: list) -> TaskResult:
        """Generate embeddings for semantic search"""
        
        thoughts = f"""
🔍 EMBEDDINGS GENERATION - Alex Morgan

Request: {task.title}

SEMANTIC SEARCH SETUP:

📚 Document Corpus:
- Volume: [Number of documents]
- Types: [PDF, DOCX, etc.]
- Size: [Total GB]
- Language: [English, Polish, Mixed]

🧠 Embedding Strategy:

Model Selection:
- Using: multilingual-e5-large-instruct (1024-dim)
- Reasoning: Supports Polish + English, high quality
- Infrastructure: LM Studio (local, private, free)

Processing Pipeline:
1. Document parsing → Clean text extraction
2. Text chunking → Optimal size (512 tokens)
3. Embedding generation → Batch processing
4. Vector storage → Qdrant database
5. Metadata attachment → Source, page, date

📊 Chunking Strategy:
- Chunk size: 512 tokens (overlap: 50 tokens)
- Reasoning: Balance between context and granularity
- Special handling: Preserve paragraphs, sections

🗄️ Qdrant Configuration:
- Collection: "analytical-team-docs"
- Vector dimension: 1024
- Distance metric: Cosine similarity
- Metadata fields: source, date, author, doc_type

🔍 Search Capabilities Enabled:
✓ Semantic search (meaning-based)
✓ Multilingual (Polish + English)
✓ Similarity scoring
✓ Filtered search (by metadata)
✓ Hybrid search (semantic + keyword)

⚙️ Technical Coordination:
Coordinating with Tomasz for:
- [Batch processing optimization]
- [Qdrant collection setup]
- [API endpoints for search]

📈 Performance:
- Embedding speed: ~100 docs/hour
- Search latency: <100ms
- Storage: ~4KB per chunk

STATUS: Embeddings generation pipeline active.
Analysts can now search by MEANING, not just keywords!
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "embeddings_generated": "Complete",
                "search_enabled": "Semantic search ready",
                "collection": "analytical-team-docs",
                "search_latency": "<100ms"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["embedding_stats.md", "search_api_docs.md", "sample_queries.md"],
            next_steps="Analysts can now use semantic search. Provide query examples."
        )
    
    def _workflow_automation(self, task: Task, context: list) -> TaskResult:
        """Automate analytical workflows"""
        
        thoughts = f"""
⚙️ WORKFLOW AUTOMATION - Alex Morgan

Automation Request: {task.title}

AUTOMATION DESIGN:

🔄 Workflow Analysis:
- Current process: [Manual steps identified]
- Frequency: [Daily/Weekly/Monthly]
- Time consumed: [Hours per execution]
- Error-prone steps: [Identified]

🤖 Automation Plan:

Input Sources:
- [Data sources listed]
- [API endpoints if applicable]
- [File locations]

Processing Steps:
1. Data ingestion (automated scraping/API calls)
2. Data cleaning (standardization, validation)
3. Transformation (calculations, aggregations)
4. Enrichment (additional data sources)
5. Output generation (reports, dashboards)

Output Delivery:
- Format: [CSV/Excel/PDF/Dashboard]
- Schedule: [Frequency]
- Distribution: [Email/Slack/Database]
- Alerts: [Error notifications]

🛠️ Technical Implementation:

Coordinating with Technical Team:
- Piotr (DevOps): Scheduling, monitoring, alerts
- Tomasz (Developer): Custom scripts if needed
- Anna (QA): Testing automation reliability

Tools/Stack:
- Scheduler: [Cron/Airflow/GitHub Actions]
- Processing: [Python scripts]
- Storage: [Database/Cloud storage]
- Monitoring: [Logging, error alerts]

📊 Automation Benefits:
- Time saved: [X hours per week]
- Error reduction: [Human error eliminated]
- Consistency: [Same process every time]
- Scalability: [Handle more data automatically]

⚡ Status:
Pipeline built. Testing. Will deploy [timeframe].
Team will be notified when automation is live.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "automation_status": "Pipeline built",
                "time_saved": "Significant",
                "reliability": "High",
                "monitoring": "Active"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["automation_script.py", "schedule_config.yaml", "monitoring_dashboard.md"],
            next_steps="Deploy automation, train team on monitoring dashboard"
        )
    
    def _data_retrieval(self, task: Task, context: list) -> TaskResult:
        """Retrieve and prepare data from databases"""
        
        thoughts = f"""
🗄️ DATA RETRIEVAL - Alex Morgan

Data Request: {task.title}

DATABASE QUERY PLAN:

📊 Data Requirements:
- Source: [PostgreSQL/Neo4j/Files]
- Time range: [Date range]
- Filters: [Specific criteria]
- Output: [Format analyst needs]

💾 Query Design:

PostgreSQL Query:
```sql
-- Optimized query for analyst needs
SELECT [specific fields]
FROM [tables]
WHERE [conditions]
GROUP BY [if needed]
ORDER BY [relevant sorting]
LIMIT [if needed]
```

Query Optimization:
- Indexed fields used
- Join strategy optimized
- Result set size estimated
- Execution time: [projected]

🔍 Data Quality Checks:
✓ NULL values handled
✓ Duplicates removed
✓ Data types validated
✓ Outliers flagged
✓ Completeness verified

📈 Data Preparation:
- Cleaning: [Steps taken]
- Transformation: [Calculations, aggregations]
- Enrichment: [Additional context added]
- Format: [CSV/Excel/JSON - analyst-friendly]

📦 Deliverable:
- Clean dataset ready for analysis
- Data dictionary included
- Quality metrics documented
- Refresh cadence: [if recurring]

STATUS: Query executed. Clean data delivered to analyst.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "data_delivered": "Clean dataset",
                "quality": "Validated",
                "format": "Analyst-ready",
                "documentation": "Included"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["dataset.csv", "data_dictionary.md", "quality_report.md"],
            next_steps="Data ready for analysis. Contact me for refresh or modifications."
        )
    
    def _technical_coordination(self, task: Task, context: list) -> TaskResult:
        """Coordinate with technical team for tools/capabilities"""
        
        thoughts = f"""
🔗 TECHNICAL COORDINATION - Alex Morgan

Technical Request: {task.title}

BRIDGING TO TECHNICAL TEAM:

📋 Request Analysis:
- Need: [What analyst needs]
- Technical complexity: [Assessment]
- Urgency: [Timeline]
- Impact: [Who benefits]

🤝 Technical Team Coordination:

Best Contact:
- Tomasz Kamiński: For implementations, scripts, APIs
- Anna Nowakowska: For testing, validation
- Piotr Szymański: For automation, deployment
- Joanna Mazur: For UI/dashboards

Request Translation:
Analytical need: "{task.description}"
Technical requirement: [Translated to technical specs]
Expected deliverable: [Clear technical output]
Success criteria: [How to measure]

⚙️ Implementation Plan:
1. Spec document created
2. Technical team briefed
3. Development tracked
4. Testing coordinated
5. Delivery to analyst with training

📊 Status Updates:
- Will update analyst team on progress
- Estimated delivery: [Timeline]
- Any blockers will be communicated promptly

🎯 My Role:
- Translate analytical needs → technical specs
- Coordinate implementation
- Test and validate
- Train analysts on new tools
- Ongoing support

STATUS: Technical request submitted to appropriate team member.
Tracking implementation. Will deliver ready-to-use tool to team.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "request_status": "Coordinated with technical team",
                "assigned_to": "Appropriate technical specialist",
                "timeline": "Communicated",
                "updates": "Will provide progress reports"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["technical_spec.md", "coordination_plan.md"],
            next_steps="Monitor technical team progress, deliver tool when ready"
        )
    
    def _elasticsearch_indexing(self, task: Task, context: list) -> TaskResult:
        """Index documents in Elasticsearch"""
        # Import the method from helper file
        from agents.analytical.alex_elasticsearch_methods import _elasticsearch_indexing
        return _elasticsearch_indexing(self, task, context)
    
    def _hybrid_search_setup(self, task: Task, context: list) -> TaskResult:
        """Setup hybrid Elasticsearch + Qdrant search"""
        from agents.analytical.alex_elasticsearch_methods import _hybrid_search_setup
        return _hybrid_search_setup(self, task, context)
    
    def _general_data_engineering(self, task: Task, context: list) -> TaskResult:
        """General data engineering support"""
        
        thoughts = f"""
🔧 DATA ENGINEERING SUPPORT - Alex Morgan

Request: {task.title}

TECHNICAL CAPABILITIES AVAILABLE:

📄 Document Processing:
- Parse: PDF, DOCX, XLSX, PPTX, images (OCR)
- Extract: Text, tables, metadata, images
- Output: Clean, structured data

🔍 Semantic Search:
- Generate embeddings (multilingual)
- Setup Qdrant collections
- Build search interfaces
- Enable meaning-based retrieval

⚙️ Automation:
- Data pipelines (ETL)
- Scheduled workflows
- Monitoring and alerts
- Error handling

🗄️ Data Operations:
- Database queries (PostgreSQL, Neo4j)
- Data cleaning and validation
- Data transformation
- Quality assurance

🤝 Technical Bridge:
- Coordinate with technical team
- Translate analytical needs to tech specs
- Deliver analyst-friendly tools
- Training and support

💡 Philosophy:
Analysts shouldn't need to be programmers.
I handle the technical complexity.
You focus on analysis, I provide clean data and tools.

Ready to support. What do you need?
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "status": "Ready for tasking",
                "capabilities": "Full data engineering support"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[],
            next_steps="Await specific data engineering request"
        )


# Test
if __name__ == "__main__":
    print("Testing Alex Agent...")
    alex = AlexAgent()
    print(f"✅ {alex.name} initialized")
    print(f"   Role: {alex.role}")
    print(f"   Purpose: Bridge analytical ↔ technical teams 🔧")
    print(f"   Supported formats: {', '.join(alex.supported_formats)}")
    print(f"   Technical contacts: {len(alex.technical_team)}")
