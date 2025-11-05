"""
Multi-Agent Orchestrator - Sequential Processing
Aleksander Nowak & Katarzyna Wiśniewska
2025-11-05
"""

import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import time

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.base_agent import (
    BaseAgent, Task, TaskResult, TaskStatus,
    FinancialAnalystAgent, LegalAnalystAgent, RiskAnalystAgent
)
from src.data.embedding_pipeline import DocumentEmbeddingPipeline, DualEmbeddingSystem
from src.data.postgres_client import PostgresClient


@dataclass
class CaseAnalysis:
    """Complete case analysis result"""
    case_id: str
    title: str
    agents_used: List[str]
    results: List[TaskResult]
    embeddings_count: int
    total_time: float
    total_tokens: int
    average_confidence: float
    synthesis: str


class MultiAgentOrchestrator:
    """
    Orchestrator for multi-agent sequential processing
    
    Workflow:
    1. Receive documents
    2. Generate embeddings
    3. Create tasks
    4. Execute agents sequentially
    5. Pass context between agents
    6. Aggregate results
    7. Store in database
    """
    
    def __init__(self, postgres_host: str = "localhost"):
        """
        Initialize orchestrator
        
        Args:
            postgres_host: PostgreSQL host
        """
        # Agents registry
        self.agents: Dict[str, BaseAgent] = {
            "financial": FinancialAnalystAgent(),
            "legal": LegalAnalystAgent(),
            "risk": RiskAnalystAgent()
        }
        
        # Data pipeline
        self.embedding_pipeline = DocumentEmbeddingPipeline()
        self.embeddings = DualEmbeddingSystem()
        
        # Database
        try:
            self.db = PostgresClient(host=postgres_host)
            self.db_available = True
        except:
            print("⚠️  PostgreSQL not available - running in test mode")
            self.db = None
            self.db_available = False
        
        # Performance tracking
        self.cases_processed = 0
        self.total_processing_time = 0
    
    def process_case(
        self,
        case_id: str,
        title: str,
        documents: List[Dict[str, str]],
        analysis_types: List[str],
        description: Optional[str] = None
    ) -> CaseAnalysis:
        """
        Process complete case with multiple documents and agents
        
        Args:
            case_id: Case identifier
            title: Case title
            documents: List of documents with 'id', 'content', 'type'
            analysis_types: List of analysis types (financial, legal, risk)
            description: Optional case description
            
        Returns:
            CaseAnalysis with complete results
        """
        start_time = time.time()
        print(f"\n{'='*70}")
        print(f"🚀 PROCESSING CASE: {case_id}")
        print(f"{'='*70}")
        
        # Step 1: Create case in database
        if self.db_available:
            print("\n📊 Creating case in database...")
            self.db.create_case(
                case_id=case_id,
                title=title,
                description=description or f"Analysis of {len(documents)} documents",
                case_type="analytical",
                metadata={
                    "document_count": len(documents),
                    "analysis_types": analysis_types,
                    "started_at": datetime.now().isoformat()
                }
            )
            print(f"   ✅ Case created: {case_id}")
        
        # Step 2: Process documents and generate embeddings
        print(f"\n📄 Processing {len(documents)} documents...")
        all_embeddings = []
        embeddings_count = 0
        
        for doc in documents:
            doc_id = doc['id']
            content = doc['content']
            doc_type = doc.get('type', 'general')
            
            print(f"   Processing: {doc_id}...")
            
            # Generate embeddings
            records = self.embedding_pipeline.process_document(
                document=content,
                document_id=doc_id,
                document_type=doc_type
            )
            
            # Add case_id to records
            for record in records:
                record['case_id'] = case_id
            
            all_embeddings.extend(records)
            embeddings_count += len(records)
            print(f"   ✅ {doc_id}: {len(records)} chunks embedded")
        
        # Step 3: Store embeddings in database
        if self.db_available and all_embeddings:
            print(f"\n💾 Storing {embeddings_count} embeddings...")
            stored = self.db.batch_store_embeddings(all_embeddings)
            print(f"   ✅ Stored {stored} embeddings")
        
        # Step 4: Prepare analysis tasks
        print(f"\n🤖 Preparing {len(analysis_types)} agent tasks...")
        tasks = []
        
        for analysis_type in analysis_types:
            task = Task(
                task_id=f"{case_id}_task_{analysis_type}_{int(time.time())}",
                title=f"{analysis_type.title()} Analysis",
                description=f"Perform {analysis_type} analysis on case documents",
                task_type=analysis_type,
                data={
                    "case_id": case_id,
                    "document_count": len(documents),
                    "documents_summary": [
                        {"id": doc['id'], "length": len(doc['content'])}
                        for doc in documents
                    ]
                },
                created_at=datetime.now()
            )
            tasks.append((analysis_type, task))
            print(f"   ✅ Task created: {analysis_type}")
        
        # Step 5: Execute agents sequentially with context
        print(f"\n🔄 Executing {len(tasks)} agents sequentially...")
        results = []
        context = []
        
        for i, (analysis_type, task) in enumerate(tasks):
            agent = self.agents.get(analysis_type)
            if not agent:
                print(f"   ⚠️  No agent for: {analysis_type}")
                continue
            
            print(f"\n   Agent {i+1}/{len(tasks)}: {agent.name}")
            print(f"   Role: {agent.role}")
            
            # Execute with context from previous agents
            result = agent.execute(task, context if i > 0 else None)
            results.append(result)
            
            # Add to context for next agent
            context.append({
                "agent_name": result.agent_name,
                "agent_role": result.agent_role,
                "output": result.output,
                "confidence": result.confidence
            })
            
            print(f"   ✅ Completed in {result.time_taken:.2f}s")
            print(f"   Confidence: {result.confidence:.2f}")
            print(f"   Tokens: {result.tokens_used['total']}")
            
            # Store task in database
            if self.db_available:
                self.db.store_agent_task(
                    case_id=case_id,
                    task_id=task.task_id,
                    agent_name=result.agent_name,
                    agent_role=result.agent_role,
                    status=result.status.value,
                    task_data=task.data,
                    result_data=result.output,
                    confidence_score=result.confidence,
                    tokens_used=result.tokens_used['total'],
                    time_taken=result.time_taken
                )
        
        # Step 6: Synthesize results
        print(f"\n📊 Synthesizing results...")
        synthesis = self._synthesize_results(results, case_id, title)
        
        # Calculate metrics
        elapsed = time.time() - start_time
        total_tokens = sum(r.tokens_used['total'] for r in results)
        avg_confidence = sum(r.confidence for r in results) / len(results) if results else 0
        
        # Update stats
        self.cases_processed += 1
        self.total_processing_time += elapsed
        
        print(f"\n{'='*70}")
        print(f"✅ CASE COMPLETE: {case_id}")
        print(f"{'='*70}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Agents: {len(results)}")
        print(f"Embeddings: {embeddings_count}")
        print(f"Tokens: {total_tokens}")
        print(f"Avg Confidence: {avg_confidence:.2f}")
        print(f"{'='*70}\n")
        
        return CaseAnalysis(
            case_id=case_id,
            title=title,
            agents_used=[r.agent_name for r in results],
            results=results,
            embeddings_count=embeddings_count,
            total_time=elapsed,
            total_tokens=total_tokens,
            average_confidence=avg_confidence,
            synthesis=synthesis
        )
    
    def _synthesize_results(
        self,
        results: List[TaskResult],
        case_id: str,
        title: str
    ) -> str:
        """
        Synthesize results from multiple agents
        
        Args:
            results: List of agent results
            case_id: Case identifier
            title: Case title
            
        Returns:
            Synthesis text
        """
        synthesis = f"# Case Analysis Synthesis: {title}\n\n"
        synthesis += f"**Case ID:** {case_id}\n"
        synthesis += f"**Agents:** {len(results)}\n"
        synthesis += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        synthesis += "## Agent Findings\n\n"
        
        for i, result in enumerate(results, 1):
            synthesis += f"### {i}. {result.agent_name} ({result.agent_role})\n\n"
            synthesis += f"**Confidence:** {result.confidence:.2f}\n\n"
            synthesis += f"**Summary:** {result.output.get('summary', 'N/A')}\n\n"
            
            findings = result.output.get('key_findings', [])
            if findings:
                synthesis += "**Key Findings:**\n"
                for finding in findings[:3]:
                    synthesis += f"- {finding}\n"
                synthesis += "\n"
            
            recommendations = result.output.get('recommendations', [])
            if recommendations:
                synthesis += "**Recommendations:**\n"
                for rec in recommendations[:3]:
                    synthesis += f"- {rec}\n"
                synthesis += "\n"
        
        synthesis += "## Overall Assessment\n\n"
        avg_conf = sum(r.confidence for r in results) / len(results)
        synthesis += f"Average Confidence: {avg_conf:.2f}\n"
        synthesis += f"Total Findings: {sum(len(r.output.get('key_findings', [])) for r in results)}\n"
        
        return synthesis
    
    def semantic_search(
        self,
        query: str,
        case_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Semantic search across documents
        
        Args:
            query: Search query
            case_id: Optional case filter
            limit: Max results
            
        Returns:
            List of search results
        """
        if not self.db_available:
            print("⚠️  Database not available for search")
            return []
        
        # Generate query embedding
        query_embedding = self.embeddings.embed(query).embedding
        
        # Search
        results = self.db.semantic_search(
            query_embedding=query_embedding,
            case_id=case_id,
            limit=limit
        )
        
        return [
            {
                "document_id": r.document_id,
                "chunk_id": r.chunk_id,
                "content": r.content,
                "similarity": r.similarity,
                "metadata": r.metadata
            }
            for r in results
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get orchestrator statistics
        
        Returns:
            Stats dictionary
        """
        return {
            "cases_processed": self.cases_processed,
            "total_time": self.total_processing_time,
            "avg_time_per_case": self.total_processing_time / self.cases_processed if self.cases_processed > 0 else 0,
            "agents_available": list(self.agents.keys()),
            "database_available": self.db_available
        }


def test_orchestrator():
    """Test orchestrator"""
    print("🧪 Testing Multi-Agent Orchestrator...\n")
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Test documents
    documents = [
        {
            "id": "doc_001",
            "content": """
            Q4 2024 Financial Report
            
            Revenue Performance: Company achieved $4.2M in revenue for Q4 2024,
            representing a 23% year-over-year increase. This strong growth was
            driven by enterprise segment expansion and improved customer retention.
            
            Profitability: EBITDA margin improved to 32%, up from 28% in Q3.
            Operating expenses were well-controlled at 18% of revenue, down from
            21% in the previous quarter.
            
            Cash Position: Company ended Q4 with $8.5M in cash and equivalents,
            providing strong runway for planned expansion initiatives.
            """,
            "type": "financial"
        },
        {
            "id": "doc_002",
            "content": """
            Legal Compliance Review Q4 2024
            
            Regulatory Compliance: All required quarterly filings were submitted
            on time. No material compliance issues identified.
            
            Contract Review: Three major customer contracts were renewed during
            Q4. All contracts include standard liability limitations and IP
            protection clauses.
            
            Risk Areas: Identified need to update data privacy policies to align
            with new state regulations effective Q1 2025.
            """,
            "type": "legal"
        }
    ]
    
    # Process case
    analysis = orchestrator.process_case(
        case_id=f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Q4 2024 Comprehensive Analysis",
        documents=documents,
        analysis_types=["financial", "legal", "risk"],
        description="End-to-end test of orchestration pipeline"
    )
    
    # Display results
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    print(f"\nCase: {analysis.case_id}")
    print(f"Agents: {', '.join(analysis.agents_used)}")
    print(f"Embeddings: {analysis.embeddings_count}")
    print(f"Total Time: {analysis.total_time:.2f}s")
    print(f"Total Tokens: {analysis.total_tokens}")
    print(f"Avg Confidence: {analysis.average_confidence:.2f}")
    
    print("\n" + "-"*70)
    print("SYNTHESIS")
    print("-"*70)
    print(analysis.synthesis)
    
    # Test semantic search
    if orchestrator.db_available:
        print("\n" + "="*70)
        print("SEMANTIC SEARCH TEST")
        print("="*70)
        
        query = "What was the revenue performance?"
        print(f"\nQuery: {query}")
        results = orchestrator.semantic_search(query, case_id=analysis.case_id, limit=3)
        
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Document: {result['document_id']}")
            print(f"   Similarity: {result['similarity']:.3f}")
            print(f"   Content: {result['content'][:150]}...")
    
    # Get stats
    stats = orchestrator.get_stats()
    print("\n" + "="*70)
    print("ORCHESTRATOR STATS")
    print("="*70)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n✅ Orchestrator test complete!")


if __name__ == "__main__":
    test_orchestrator()
