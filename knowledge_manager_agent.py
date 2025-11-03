"""
Knowledge Manager Agent - Documentation & Memory Optimization

Odpowiedzialny za:
- Sumaryzację długich dyskusji
- Strukturyzację wiedzy projektowej
- Tracking kluczowych decyzji
- Formatowanie dokumentacji
- Optymalizację pamięci agentów
- Cross-project learning

To jest DEDYKOWANY agent do zarządzania wiedzą - nie orchestrator!
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid
from psycopg2.extras import Json


@dataclass
class ProjectSummary:
    """Structured summary of project phase/period"""
    id: str
    project_id: str
    summary_type: str  # daily, weekly, phase, milestone
    period_start: datetime
    period_end: datetime
    
    # Core content
    key_decisions: List[Dict[str, Any]]
    main_discussions: List[str]
    action_items: List[str]
    blockers: List[str]
    
    # Metadata
    message_count: int
    agents_involved: List[str]
    importance: float
    
    # AI-generated
    executive_summary: str  # 2-3 sentences
    detailed_summary: str   # 1-2 paragraphs
    keywords: List[str]


@dataclass  
class DecisionRecord:
    """Structured record of a decision"""
    id: str
    project_id: str
    decision_text: str
    
    # What was decided
    chosen: List[str]
    rejected: List[str]
    
    # Context
    decided_by: List[str]  # Multiple agents can decide together
    date: datetime
    reasoning: List[str]
    alternatives_considered: List[str]
    
    # Impact
    impacts: List[str]  # What areas this affects
    dependencies: List[str]  # What depends on this
    
    # References
    related_messages: List[str]  # Message IDs
    related_documents: List[str]


class KnowledgeManagerAgent:
    """
    Knowledge Manager - Agent dedykowany dokumentacji i organizacji wiedzy.
    
    This agent is NOT the orchestrator - it's a specialist in knowledge management.
    Orchestrator coordinates; Knowledge Manager documents.
    """
    
    def __init__(
        self,
        name: str = "Dr. Helena Kowalczyk",
        postgres_store=None,
        neo4j_graph=None,
        qdrant_store=None
    ):
        self.name = name
        self.role = "Knowledge Manager"
        self.postgres = postgres_store
        self.neo4j = neo4j_graph
        self.qdrant = qdrant_store
        
        # Knowledge Manager's own knowledge base
        self.active_summaries: Dict[str, ProjectSummary] = {}
        self.decision_records: Dict[str, DecisionRecord] = {}
        self.documentation_queue: List[Dict] = []
    
    # ==================== SUMMARIZATION ====================
    
    def create_daily_summary(
        self,
        project_id: str,
        date: datetime
    ) -> Optional[ProjectSummary]:
        """
        Create daily summary of project activity.
        
        Triggered automatically at end of day or manually.
        """
        # Get all messages from that day
        start = date.replace(hour=0, minute=0, second=0)
        end = date.replace(hour=23, minute=59, second=59)
        
        # Query PostgreSQL for messages
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT id, sender, content, message_type, importance
                FROM messages
                WHERE project_id = %s
                  AND timestamp BETWEEN %s AND %s
                ORDER BY timestamp ASC
            """, (project_id, start, end))
            
            messages = cur.fetchall()
        
        if not messages:
            return None
        
        # Extract key information
        key_decisions = self._extract_decisions(messages)
        main_discussions = self._extract_main_topics(messages)
        action_items = self._extract_action_items(messages)
        
        # Generate summaries (would use AI here)
        exec_summary = self._generate_executive_summary(messages, key_decisions)
        detailed_summary = self._generate_detailed_summary(messages)
        
        # Create summary object
        summary = ProjectSummary(
            id=str(uuid.uuid4()),
            project_id=project_id,
            summary_type="daily",
            period_start=start,
            period_end=end,
            key_decisions=key_decisions,
            main_discussions=main_discussions,
            action_items=action_items,
            blockers=[],
            message_count=len(messages),
            agents_involved=list(set(msg[1] for msg in messages)),
            importance=self._calculate_summary_importance(key_decisions),
            executive_summary=exec_summary,
            detailed_summary=detailed_summary,
            keywords=self._extract_keywords([msg[2] for msg in messages])
        )
        
        # Store summary
        self._store_summary(summary)
        
        return summary
    
    def create_phase_summary(
        self,
        project_id: str,
        phase_name: str,
        start_date: datetime,
        end_date: datetime
    ) -> ProjectSummary:
        """
        Create summary for entire project phase.
        
        Example: "Architecture Phase" (weeks 2-4)
        """
        # Get all messages from phase
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT id, sender, content, message_type, importance
                FROM messages
                WHERE project_id = %s
                  AND timestamp BETWEEN %s AND %s
                ORDER BY importance DESC, timestamp ASC
            """, (project_id, start_date, end_date))
            
            messages = cur.fetchall()
        
        # Get daily summaries for this period (if exist)
        daily_summaries = self._get_summaries_for_period(
            project_id, start_date, end_date, "daily"
        )
        
        # Synthesize phase summary
        summary = self._synthesize_phase_summary(
            phase_name,
            messages,
            daily_summaries
        )
        
        return summary
    
    # ==================== DECISION TRACKING ====================
    
    def record_decision(
        self,
        project_id: str,
        decision_text: str,
        chosen: List[str],
        rejected: List[str],
        decided_by: List[str],
        reasoning: List[str],
        message_ids: List[str]
    ) -> DecisionRecord:
        """
        Create structured record of a decision.
        
        This is CRITICAL for long-term projects - you need to know
        not just WHAT was decided, but WHY, by WHOM, and WHAT alternatives
        were considered.
        """
        decision = DecisionRecord(
            id=str(uuid.uuid4()),
            project_id=project_id,
            decision_text=decision_text,
            chosen=chosen,
            rejected=rejected,
            decided_by=decided_by,
            date=datetime.now(),
            reasoning=reasoning,
            alternatives_considered=rejected,
            impacts=self._identify_impacts(chosen, project_id),
            dependencies=self._identify_dependencies(chosen, project_id),
            related_messages=message_ids,
            related_documents=[]
        )
        
        # Store in PostgreSQL
        self._store_decision(decision)
        
        # Store in Neo4j (knowledge graph)
        if self.neo4j:
            self.neo4j.add_decision(
                decision_id=decision.id,
                project_id=project_id,
                decision_text=decision_text,
                decided_by=decided_by[0] if decided_by else "Team",
                chosen=chosen,
                rejected=rejected,
                reasons=reasoning,
                timestamp=decision.date
            )
        
        return decision
    
    # ==================== DOCUMENTATION GENERATION ====================
    
    def generate_project_documentation(
        self,
        project_id: str
    ) -> Dict[str, str]:
        """
        Generate comprehensive project documentation.
        
        Returns multiple documents:
        - README.md (overview)
        - ARCHITECTURE.md (technical design)
        - DECISIONS.md (decision log)
        - ROADMAP.md (plans and timeline)
        """
        docs = {}
        
        # README (project overview)
        docs['README.md'] = self._generate_readme(project_id)
        
        # ARCHITECTURE (technical decisions)
        docs['ARCHITECTURE.md'] = self._generate_architecture_doc(project_id)
        
        # DECISIONS (decision log)
        docs['DECISIONS.md'] = self._generate_decision_log(project_id)
        
        # ROADMAP (plans)
        docs['ROADMAP.md'] = self._generate_roadmap(project_id)
        
        return docs
    
    def _generate_decision_log(self, project_id: str) -> str:
        """Generate decision log document"""
        # Get all decisions from PostgreSQL
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                SELECT decision_text, decision_type, made_by, approved_by, timestamp, context
                FROM decisions
                WHERE project_id = %s
                ORDER BY timestamp DESC
            """, (project_id,))
            
            decisions = cur.fetchall()
        
        # Format as markdown
        doc = f"# Decision Log\n\n"
        doc += f"Project: {project_id}\n"
        doc += f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        doc += "---\n\n"
        
        for decision_text, decision_type, made_by, approved_by, timestamp, context in decisions:
            doc += f"## {timestamp.strftime('%Y-%m-%d')}: {decision_type or 'Decision'}\n\n"
            doc += f"**Decision:** {decision_text}\n\n"
            doc += f"**Made by:** {made_by}\n\n"
            
            if approved_by:
                doc += f"**Approved by:** {', '.join(approved_by)}\n\n"
            
            if context:
                doc += f"**Context:** {context}\n\n"
            
            doc += "---\n\n"
        
        return doc
    
    # ==================== MEMORY OPTIMIZATION ====================
    
    def optimize_agent_memory(
        self,
        agent_name: str,
        project_id: str,
        target_token_count: int = 10000
    ) -> Dict[str, Any]:
        """
        Optimize agent's memory to fit target token count.
        
        Strategy:
        1. Keep most important decisions (facts)
        2. Replace old detailed conversations with summaries
        3. Keep recent context (last week) in full detail
        4. Older context → compressed summaries
        """
        # Get agent's full context
        messages = self.postgres.get_agent_conversation_history(
            agent_name=agent_name,
            project_id=project_id,
            limit=10000
        )
        
        # Categorize by age
        now = datetime.now()
        recent = []  # Last 7 days - keep full
        medium = []  # 7-30 days - summarize weekly
        old = []     # 30+ days - summarize monthly
        
        for msg in messages:
            age = (now - msg.timestamp).days
            if age <= 7:
                recent.append(msg)
            elif age <= 30:
                medium.append(msg)
            else:
                old.append(msg)
        
        # Build optimized context
        optimized = {
            "recent_full": recent,  # Full detail
            "medium_summaries": self._create_weekly_summaries(medium),
            "old_summaries": self._create_monthly_summaries(old),
            "key_facts": self._extract_key_facts(messages)
        }
        
        # Estimate tokens
        estimated_tokens = (
            len(recent) * 150 +  # Recent: ~150 tokens each
            len(optimized['medium_summaries']) * 300 +  # Summaries: ~300 tokens
            len(optimized['old_summaries']) * 500 +
            len(optimized['key_facts']) * 50
        )
        
        return {
            "optimized_context": optimized,
            "original_message_count": len(messages),
            "estimated_tokens": estimated_tokens,
            "compression_ratio": len(messages) / (estimated_tokens / 150),
            "recent_kept": len(recent),
            "summarized": len(medium) + len(old)
        }
    
    # ==================== AGENT BRIEFING ====================
    
    def create_agent_briefing(
        self,
        agent_name: str,
        project_id: str,
        task: str
    ) -> str:
        """
        Create a concise briefing for an agent starting a task.
        
        Instead of giving agent ALL messages, give them:
        - Task description
        - Relevant decisions (from Neo4j)
        - Related context (from Qdrant semantic search)
        - Key facts (from summaries)
        
        This optimizes agent's context window usage.
        """
        briefing = f"# Task Briefing for {agent_name}\n\n"
        briefing += f"## Task\n{task}\n\n"
        
        # Get relevant decisions
        if self.neo4j:
            # Extract concepts from task
            concepts = self._extract_concepts_simple(task)
            
            briefing += "## Relevant Decisions\n\n"
            for concept in concepts[:3]:
                chain = self.neo4j.find_decision_chain(concept, project_id)
                if chain:
                    briefing += f"### {concept}\n"
                    for decision in chain[:2]:  # Top 2
                        briefing += f"- {decision.get('decision', 'N/A')}\n"
                        briefing += f"  Decided by: {decision.get('decided_by', 'Unknown')}\n"
                    briefing += "\n"
        
        # Get recent summaries
        recent_summaries = self._get_recent_summaries(project_id, days=7)
        if recent_summaries:
            briefing += "## Recent Activity\n\n"
            for summary in recent_summaries[:3]:
                briefing += f"**{summary['period']}:** {summary['executive_summary']}\n\n"
        
        # Get key facts
        facts = self._get_key_facts_for_agent(agent_name, project_id)
        if facts:
            briefing += "## Key Facts\n\n"
            for fact in facts[:10]:
                briefing += f"- {fact}\n"
            briefing += "\n"
        
        return briefing
    
    # ==================== HELPERS ====================
    
    def _extract_decisions(self, messages: List) -> List[Dict[str, Any]]:
        """Extract decisions from messages"""
        decisions = []
        
        decision_keywords = [
            'wybraliśmy', 'decided', 'will use', 'going with',
            'wybieramy', 'postanowiliśmy', 'zdecydowaliśmy'
        ]
        
        for msg_id, sender, content, msg_type, importance in messages:
            content_lower = content.lower()
            
            if msg_type == 'DECISION' or any(kw in content_lower for kw in decision_keywords):
                decisions.append({
                    "message_id": msg_id,
                    "sender": sender,
                    "content": content,
                    "importance": importance
                })
        
        return decisions
    
    def _extract_main_topics(self, messages: List) -> List[str]:
        """Extract main discussion topics"""
        # In production: use NLP topic modeling
        # For now: simple keyword frequency
        all_text = " ".join(msg[2] for msg in messages)
        
        # Common tech keywords
        keywords = [
            'architecture', 'database', 'api', 'security', 'testing',
            'deployment', 'performance', 'design', 'implementation'
        ]
        
        topics = []
        for keyword in keywords:
            if keyword in all_text.lower():
                count = all_text.lower().count(keyword)
                if count >= 3:
                    topics.append(f"{keyword} ({count} mentions)")
        
        return topics[:5]
    
    def _extract_action_items(self, messages: List) -> List[str]:
        """Extract action items from messages"""
        action_items = []
        
        action_keywords = [
            'need to', 'should', 'must', 'will implement',
            'todo', 'action item', 'trzeba', 'należy'
        ]
        
        for msg_id, sender, content, msg_type, importance in messages:
            content_lower = content.lower()
            
            if any(kw in content_lower for kw in action_keywords):
                # Extract sentence with action keyword
                sentences = content.split('.')
                for sentence in sentences:
                    if any(kw in sentence.lower() for kw in action_keywords):
                        action_items.append(sentence.strip())
                        break
        
        return action_items[:10]
    
    def _generate_executive_summary(
        self,
        messages: List,
        key_decisions: List[Dict]
    ) -> str:
        """
        Generate 2-3 sentence executive summary.
        
        In production: use AI (Claude Sonnet 4.5 excellent at this)
        """
        message_count = len(messages)
        decision_count = len(key_decisions)
        agents = set(msg[1] for msg in messages)
        
        summary = f"Today: {message_count} messages from {len(agents)} agents. "
        
        if decision_count > 0:
            summary += f"{decision_count} key decisions made. "
        
        if key_decisions:
            first_decision = key_decisions[0]['content'][:80]
            summary += f"Notable: {first_decision}..."
        
        return summary
    
    def _generate_detailed_summary(self, messages: List) -> str:
        """
        Generate 1-2 paragraph detailed summary.
        
        In production: use AI with prompt like:
        "Summarize the following conversation in 1-2 paragraphs,
         focusing on key decisions, main discussions, and action items"
        """
        # Placeholder - would use AI
        return f"Detailed summary of {len(messages)} messages..."
    
    def _calculate_summary_importance(self, key_decisions: List[Dict]) -> float:
        """Calculate how important this summary is"""
        if not key_decisions:
            return 0.3
        
        # More decisions = more important
        importance = min(0.5 + (len(key_decisions) * 0.1), 1.0)
        
        # High-importance decisions boost summary importance
        max_decision_importance = max(
            (d.get('importance', 0.5) for d in key_decisions),
            default=0.5
        )
        
        return (importance + max_decision_importance) / 2
    
    def _extract_keywords(self, texts: List[str]) -> List[str]:
        """Extract keywords from texts"""
        # Simple word frequency
        all_text = " ".join(texts).lower()
        words = all_text.split()
        
        # Filter common words
        common = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'}
        keywords = [w for w in set(words) if len(w) > 4 and w not in common]
        
        # Return top keywords (would use TF-IDF in production)
        return keywords[:20]
    
    def _store_summary(self, summary: ProjectSummary):
        """Store summary in PostgreSQL"""
        with self.postgres.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO agent_contexts (agent_name, project_id, context_key, context_value, importance)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (agent_name, project_id, context_key)
                DO UPDATE SET context_value = EXCLUDED.context_value
            """, (
                self.name,
                summary.project_id,
                f"summary_{summary.summary_type}_{summary.period_start.date()}",
                Json({
                    "executive_summary": summary.executive_summary,
                    "detailed_summary": summary.detailed_summary,
                    "key_decisions": summary.key_decisions,
                    "keywords": summary.keywords,
                    "message_count": summary.message_count
                }),
                summary.importance
            ))
            self.postgres.conn.commit()
    
    def _extract_concepts_simple(self, text: str) -> List[str]:
        """Simple concept extraction"""
        concepts = [
            'postgresql', 'mongodb', 'redis', 'neo4j',
            'microservices', 'api', 'security', 'testing',
            'architecture', 'deployment', 'performance'
        ]
        
        text_lower = text.lower()
        return [c.title() for c in concepts if c in text_lower]
    
    def _get_recent_summaries(
        self,
        project_id: str,
        days: int = 7
    ) -> List[Dict]:
        """Get recent summaries"""
        # Would query from PostgreSQL agent_contexts
        return []
    
    def _get_key_facts_for_agent(
        self,
        agent_name: str,
        project_id: str
    ) -> List[str]:
        """Get key facts relevant for agent"""
        # Would query from agent's context
        return []
    
    def _create_weekly_summaries(self, messages: List) -> List[Dict]:
        """Create weekly summaries from messages"""
        # Group by week and summarize
        return []
    
    def _create_monthly_summaries(self, messages: List) -> List[Dict]:
        """Create monthly summaries from messages"""
        # Group by month and summarize
        return []
    
    def _extract_key_facts(self, messages: List) -> List[Dict]:
        """Extract atomic facts from messages"""
        return []
    
    def _synthesize_phase_summary(
        self,
        phase_name: str,
        messages: List,
        daily_summaries: List
    ) -> ProjectSummary:
        """Synthesize phase summary from daily summaries + messages"""
        # Would use AI to synthesize
        return None
    
    def _get_summaries_for_period(
        self,
        project_id: str,
        start: datetime,
        end: datetime,
        summary_type: str
    ) -> List[Dict]:
        """Get summaries for a time period"""
        return []
    
    def _identify_impacts(self, chosen: List[str], project_id: str) -> List[str]:
        """Identify what areas are impacted by choices"""
        return []
    
    def _identify_dependencies(self, chosen: List[str], project_id: str) -> List[str]:
        """Identify dependencies"""
        return []
    
    def _store_decision(self, decision: DecisionRecord):
        """Store decision in PostgreSQL"""
        pass
    
    def _generate_readme(self, project_id: str) -> str:
        """Generate README"""
        return "# Project README\n\nGenerated by Knowledge Manager"
    
    def _generate_architecture_doc(self, project_id: str) -> str:
        """Generate architecture document"""
        return "# Architecture\n\nGenerated by Knowledge Manager"
    
    def _generate_roadmap(self, project_id: str) -> str:
        """Generate roadmap"""
        return "# Roadmap\n\nGenerated by Knowledge Manager"


# ==================== ORCHESTRATOR EXTENSION ====================

class DocumentationOrchestrator:
    """
    Extension to Master Orchestrator for documentation management.
    
    This shows how Knowledge Manager works WITH orchestrator,
    not INSTEAD of orchestrator.
    """
    
    def __init__(self, master_orchestrator):
        self.orchestrator = master_orchestrator
        self.knowledge_manager = KnowledgeManagerAgent(
            postgres_store=master_orchestrator.postgres,
            neo4j_graph=master_orchestrator.neo4j,
            qdrant_store=master_orchestrator.qdrant
        )
    
    def end_of_day_workflow(self, project_id: str):
        """
        Run at end of each day.
        
        Knowledge Manager creates daily summary, optimizes memory.
        """
        today = datetime.now()
        
        # Create daily summary
        summary = self.knowledge_manager.create_daily_summary(
            project_id=project_id,
            date=today
        )
        
        if summary:
            print(f"📝 Daily summary created: {summary.message_count} messages")
            print(f"   Key decisions: {len(summary.key_decisions)}")
            print(f"   {summary.executive_summary}")
    
    def end_of_phase_workflow(
        self,
        project_id: str,
        phase_name: str,
        start_date: datetime,
        end_date: datetime
    ):
        """
        Run at end of project phase.
        
        Knowledge Manager creates phase summary, generates docs.
        """
        # Phase summary
        summary = self.knowledge_manager.create_phase_summary(
            project_id=project_id,
            phase_name=phase_name,
            start_date=start_date,
            end_date=end_date
        )
        
        # Generate documentation
        docs = self.knowledge_manager.generate_project_documentation(project_id)
        
        print(f"📚 Phase '{phase_name}' documentation complete:")
        for doc_name in docs.keys():
            print(f"   - {doc_name}")
    
    def optimize_all_agents(self, project_id: str):
        """
        Optimize memory for all agents.
        
        Useful before major milestone or when project is getting large.
        """
        agents = [
            "Magdalena Kowalska",
            "Katarzyna Wiśniewska",
            "Tomasz Zieliński",
            "Anna Nowakowska"
        ]
        
        print(f"\n🧠 Optimizing agent memories for project {project_id}...")
        
        for agent in agents:
            result = self.knowledge_manager.optimize_agent_memory(
                agent_name=agent,
                project_id=project_id,
                target_token_count=10000
            )
            
            print(f"\n  {agent}:")
            print(f"    Messages: {result['original_message_count']}")
            print(f"    Tokens: {result['estimated_tokens']}")
            print(f"    Compression: {result['compression_ratio']:.1f}x")


if __name__ == "__main__":
    print("Knowledge Manager Agent - Documentation Specialist")
    print("=" * 60)
    print("\nThis agent handles:")
    print("  ✅ Daily/weekly/phase summaries")
    print("  ✅ Decision tracking and documentation")
    print("  ✅ Agent memory optimization")
    print("  ✅ Project documentation generation")
    print("  ✅ Knowledge base maintenance")
    print("\n✨ Works WITH orchestrator, not INSTEAD of!")
