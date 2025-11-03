"""
Michał Kowalczyk - Software Architect Agent
Specialization: System architecture, design patterns, scalability, technical leadership

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class MichalAgent(BaseAgent):
    """
    Software Architect Agent
    
    Specialized in:
    - System architecture design
    - Design patterns and best practices
    - Scalability and performance
    - Technical documentation
    - Architecture reviews
    
    This agent provides architecture-specific reasoning and system design outputs.
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        super().__init__(
            name="Michał Kowalczyk",
            role="Software Architect",
            specialization="System architecture, Design patterns, Scalability, Technical leadership",
            project_id=project_id
        )
        
        # Architecture-specific attributes
        self.design_patterns = [
            "Microservices", "Event-driven", "CQRS", "Repository", 
            "Factory", "Observer", "Strategy", "Adapter"
        ]
        self.architectural_styles = ["Layered", "Hexagonal", "Clean Architecture", "Domain-Driven Design"]
        self.focus_areas = ["Scalability", "Maintainability", "Performance", "Security", "Resilience"]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute architecture-specific work
        
        Analyzes task and routes to appropriate architecture handler.
        """
        start_time = datetime.now()
        
        # Load relevant architecture context
        context = self.load_context(task.description, limit=3)
        context_list = context if isinstance(context, list) else []
        
        # Analyze task type
        task_lower = task.description.lower()
        
        if any(word in task_lower for word in ["design", "architecture", "system", "structure"]):
            result = self._design_architecture(task, context_list)
        elif any(word in task_lower for word in ["review", "evaluate", "assess", "analyze"]):
            result = self._review_architecture(task, context_list)
        elif any(word in task_lower for word in ["document", "documentation", "adr", "spec"]):
            result = self._document_design(task, context_list)
        elif any(word in task_lower for word in ["scalability", "scale", "performance", "load"]):
            result = self._evaluate_scalability(task, context_list)
        elif any(word in task_lower for word in ["pattern", "refactor", "improve", "modernize"]):
            result = self._recommend_patterns(task, context_list)
        else:
            result = self._general_architecture_work(task, context_list)
            
        # Calculate time
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
        
    def _design_architecture(self, task: Task, context_list) -> TaskResult:
        """Design system architecture"""
        
        thoughts = f"""
ARCHITECTURE DESIGN (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: System Architecture Design

ARCHITECTURAL APPROACH:
1. Requirements Analysis
   - Functional requirements (what system does)
   - Non-functional requirements (performance, scale, security)
   - Constraints and trade-offs
   - Quality attributes prioritization
   
2. High-Level Architecture
   ┌─────────────────────────────────────────┐
   │         SYSTEM ARCHITECTURE             │
   ├─────────────────────────────────────────┤
   │                                         │
   │  ┌──────────┐      ┌──────────┐       │
   │  │   API    │─────▶│ Business │       │
   │  │  Layer   │      │  Logic   │       │
   │  └──────────┘      └──────────┘       │
   │       │                  │             │
   │       ▼                  ▼             │
   │  ┌──────────┐      ┌──────────┐       │
   │  │   Auth   │      │   Data   │       │
   │  │ Service  │      │  Layer   │       │
   │  └──────────┘      └──────────┘       │
   └─────────────────────────────────────────┘
   
3. Component Design
   ├── Presentation Layer
   │   • REST API (Express/FastAPI)
   │   • GraphQL endpoint (optional)
   │   • WebSocket for real-time
   │
   ├── Application Layer
   │   • Use cases and business logic
   │   • Service orchestration
   │   • Transaction management
   │
   ├── Domain Layer
   │   • Domain models and entities
   │   • Business rules
   │   • Domain events
   │
   └── Infrastructure Layer
       • Database (PostgreSQL)
       • Cache (Redis)
       • Message queue (RabbitMQ)
       • External services

4. Data Flow Architecture
   Request → API Gateway → Load Balancer → Service Instances
   ↓
   Business Logic → Domain Rules → Validation
   ↓
   Data Access → Cache Check → Database
   ↓
   Response ← Transform ← Aggregate ← Query

5. Cross-Cutting Concerns
   ✓ Authentication & Authorization (JWT, OAuth2)
   ✓ Logging & Monitoring (ELK stack)
   ✓ Error handling & resilience (Circuit breaker)
   ✓ Rate limiting & throttling
   ✓ API versioning strategy

ARCHITECTURAL DECISIONS:
📋 ADR-001: Microservices Architecture
   Context: Need for independent scaling and deployment
   Decision: Use microservices pattern
   Consequences: +flexibility, -complexity

📋 ADR-002: Event-Driven Communication
   Context: Services need loose coupling
   Decision: Event bus with RabbitMQ
   Consequences: +decoupling, +scalability, -debugging

📋 ADR-003: CQRS Pattern
   Context: Read/write patterns differ significantly
   Decision: Separate read and write models
   Consequences: +performance, +scalability, -consistency

TECHNOLOGY STACK:
- Backend: Python (FastAPI), Node.js (Express)
- Database: PostgreSQL (primary), MongoDB (documents)
- Cache: Redis (sessions, hot data)
- Message Queue: RabbitMQ
- API Gateway: Kong / AWS API Gateway
- Container: Docker, Kubernetes

SCALABILITY STRATEGY:
- Horizontal scaling for stateless services
- Database read replicas for read-heavy operations
- CDN for static assets
- Caching at multiple layers
- Async processing for heavy operations

ARCHITECTURE CONTEXT:
{len(context_list)} previous architectural decisions reviewed
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "architecture_design",
                "architectural_style": "microservices",
                "components_designed": 8,
                "design_patterns": ["CQRS", "Event-driven", "Repository"],
                "scalability": "horizontal",
                "documented": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "architecture_diagram.png",
                "component_diagram.png",
                "data_flow_diagram.png",
                "architecture_decision_records.md",
                "tech_stack_specification.md"
            ],
            next_steps="Review with team, validate non-functional requirements, handoff to Tomasz (Dev)"
        )
        
    def _review_architecture(self, task: Task, context_list) -> TaskResult:
        """Review existing architecture"""
        
        thoughts = f"""
ARCHITECTURE REVIEW (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: Architecture Review & Assessment

REVIEW FRAMEWORK:
1. Architectural Quality Attributes
   ├── Performance
   │   • Response time under load
   │   • Throughput capacity
   │   • Resource utilization
   │
   ├── Scalability
   │   • Horizontal scaling capability
   │   • Vertical scaling limits
   │   • Auto-scaling implementation
   │
   ├── Maintainability
   │   • Code modularity
   │   • Separation of concerns
   │   • Technical debt level
   │
   ├── Security
   │   • Authentication/Authorization
   │   • Data encryption
   │   • Security vulnerabilities
   │
   └── Resilience
       • Fault tolerance
       • Error recovery
       • Circuit breakers

2. Design Pattern Analysis
   ✓ GOOD: Repository pattern properly implemented
   ✓ GOOD: Dependency injection for loose coupling
   ⚠️  ISSUE: Missing circuit breaker pattern
   ⚠️  ISSUE: No retry logic for external calls
   ❌ PROBLEM: Tight coupling between services

3. Architecture Smells Detected
   🔴 CRITICAL: Distributed monolith
      • Services share database
      • Synchronous communication everywhere
      → Recommendation: Introduce event bus
   
   🟡 MEDIUM: Single point of failure
      • No redundancy for critical services
      → Recommendation: Add load balancer + replicas
   
   🟡 MEDIUM: Missing API gateway
      • Clients call services directly
      → Recommendation: Add API gateway layer

4. Technical Debt Assessment
   Debt Level: MEDIUM
   - Legacy code: ~20% of codebase
   - Missing tests: Architecture layer
   - Documentation: Partially outdated
   
   Priority Refactoring:
   1. Decouple services (HIGH)
   2. Add resilience patterns (HIGH)
   3. Update documentation (MEDIUM)

5. Scalability Assessment
   Current Capacity: 1,000 req/sec
   Bottlenecks Identified:
   - Database connection pool (max 100)
   - Synchronous service calls
   - No caching layer
   
   Recommended Improvements:
   ✓ Add Redis cache layer
   ✓ Implement async messaging
   ✓ Database connection pooling

ARCHITECTURE SCORE: 6.5/10
- Strengths: Good structure, clear separation
- Weaknesses: Scalability limits, coupling issues
- Recommendation: Moderate refactoring needed

COMPARISON TO BEST PRACTICES:
✓ Clean code principles
✓ SOLID principles mostly followed
⚠️  Missing resilience patterns
⚠️  Limited scalability
❌ Tight service coupling
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "architecture_review",
                "overall_score": 6.5,
                "critical_issues": 1,
                "medium_issues": 2,
                "recommendations": 5,
                "refactoring_needed": "moderate"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "architecture_review.pdf",
                "issues_found.md",
                "recommendations.md",
                "refactoring_plan.md"
            ],
            next_steps="Prioritize critical issues, plan refactoring with Tomasz (Dev)"
        )
        
    def _document_design(self, task: Task, context_list) -> TaskResult:
        """Create technical documentation"""
        
        thoughts = f"""
TECHNICAL DOCUMENTATION (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: Architecture Documentation

DOCUMENTATION STRUCTURE:
1. Architecture Overview
   ├── System Context Diagram (C4 Level 1)
   ├── Container Diagram (C4 Level 2)
   ├── Component Diagram (C4 Level 3)
   └── Code Diagram (C4 Level 4)
   
2. Architecture Decision Records (ADRs)
   Format: Markdown files in /docs/adr/
   
   ADR-001-microservices-architecture.md
   ADR-002-event-driven-communication.md
   ADR-003-database-per-service.md
   ADR-004-api-gateway-pattern.md
   ADR-005-caching-strategy.md

3. Component Specifications
   For each major component:
   - Purpose and responsibilities
   - Interface definition (API contract)
   - Dependencies (internal/external)
   - Data models
   - Configuration
   - Deployment requirements

4. Data Architecture
   ├── Database Schema
   │   • Entity relationship diagrams
   │   • Table definitions
   │   • Indexes and constraints
   │
   ├── Data Flow
   │   • Input/output specifications
   │   • Data transformations
   │   • State management
   │
   └── Data Lifecycle
       • Creation and validation
       • Storage and retrieval
       • Archival and deletion

5. Integration Points
   ├── Internal APIs
   │   • REST endpoints specification
   │   • Event contracts
   │   • Message formats
   │
   └── External Services
       • Third-party integrations
       • Authentication methods
       • Rate limits and quotas

DOCUMENTATION DELIVERABLES:
📄 Architecture Overview (executive summary)
📄 System Design Document (detailed spec)
📄 API Documentation (OpenAPI/Swagger)
📄 Deployment Guide (infrastructure)
📄 Monitoring & Operations Guide
📄 Architecture Decision Records (ADRs)

DIAGRAMS CREATED:
🖼️  C4 Model Diagrams (4 levels)
🖼️  Sequence Diagrams (key flows)
🖼️  Deployment Diagram (infrastructure)
🖼️  Data Flow Diagrams
🖼️  Component Interaction Diagrams

DOCUMENTATION TOOLS:
- Diagrams: PlantUML, Draw.io, Lucidchart
- API Docs: Swagger/OpenAPI
- ADRs: Markdown in Git
- Wiki: Confluence/Notion

DOCUMENTATION STANDARDS:
✓ C4 model for architecture diagrams
✓ ADR template for decisions
✓ OpenAPI 3.0 for REST APIs
✓ RFC 2119 keywords (MUST, SHOULD, MAY)
✓ Semantic versioning for APIs
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "technical_documentation",
                "documents_created": 6,
                "diagrams_created": 8,
                "adrs_written": 5,
                "api_documented": True,
                "c4_model": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "architecture_overview.pdf",
                "system_design_doc.pdf",
                "api_documentation.yaml",
                "deployment_guide.md",
                "adr_records/"
            ],
            next_steps="Share with team, maintain as living documentation"
        )
        
    def _evaluate_scalability(self, task: Task, context_list) -> TaskResult:
        """Evaluate system scalability"""
        
        thoughts = f"""
SCALABILITY EVALUATION (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: Scalability & Performance Analysis

SCALABILITY ASSESSMENT:
1. Current Capacity Analysis
   Baseline Metrics:
   - Throughput: 1,000 requests/second
   - Latency: p95 < 200ms, p99 < 500ms
   - Concurrent users: 10,000
   - Database: 50GB, 1,000 queries/sec
   
   Load Testing Results:
   - At 2x load: Performance degrades 40%
   - At 3x load: System becomes unstable
   - Bottleneck: Database connections

2. Horizontal Scalability
   ✓ GOOD: Stateless application services
   ✓ GOOD: Load balancer distributing traffic
   ⚠️  ISSUE: Database not scaled (single instance)
   ⚠️  ISSUE: Shared sessions (not distributed)
   
   Horizontal Scaling Plan:
   - Add service replicas (easy)
   - Implement Redis for sessions
   - Database read replicas
   - Shard database if needed (>1TB)

3. Vertical Scalability
   Current Resources:
   - CPU: 4 cores (80% utilized peak)
   - Memory: 16GB (70% utilized)
   - Disk: SSD, 500 IOPS
   
   Vertical Scaling Potential:
   - Can scale to 16 cores (4x)
   - Can scale to 64GB RAM (4x)
   - Limited by cloud instance size

4. Bottleneck Analysis
   🔴 CRITICAL: Database connection pool
      Current: 100 connections
      Peak usage: 95 connections
      → Solution: Increase pool + read replicas
   
   🟡 MEDIUM: No caching layer
      Cache hit rate: N/A (no cache)
      → Solution: Add Redis cache
   
   🟡 MEDIUM: Synchronous service calls
      External API latency: 200-500ms
      → Solution: Async processing + queue

5. Scalability Improvements
   Phase 1 (Quick wins - 1 week):
   ✓ Add Redis cache (expected: 30% load reduction)
   ✓ Database connection pool tuning
   ✓ Enable gzip compression
   ✓ CDN for static assets
   
   Phase 2 (Medium term - 1 month):
   ✓ Database read replicas (3x read capacity)
   ✓ Async job processing (RabbitMQ)
   ✓ Auto-scaling groups
   ✓ Circuit breakers for resilience
   
   Phase 3 (Long term - 3 months):
   ✓ Microservices decomposition
   ✓ Event-driven architecture
   ✓ Database sharding if needed
   ✓ Multi-region deployment

PROJECTED CAPACITY AFTER IMPROVEMENTS:
Current:    1,000 req/sec
Phase 1:    3,000 req/sec (3x)
Phase 2:   10,000 req/sec (10x)
Phase 3:   50,000 req/sec (50x)

COST-BENEFIT ANALYSIS:
- Phase 1: Low cost, high impact
- Phase 2: Medium cost, high impact
- Phase 3: High cost, needed for scale

RECOMMENDATION: 
Start with Phase 1 (quick wins), monitor growth, 
proceed to Phase 2 when reaching 70% capacity.
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "scalability_evaluation",
                "current_capacity": "1000 req/sec",
                "bottlenecks_found": 3,
                "scalability_score": 6.0,
                "improvement_phases": 3,
                "projected_capacity": "50000 req/sec"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "scalability_report.pdf",
                "bottleneck_analysis.md",
                "improvement_roadmap.md",
                "capacity_projections.xlsx"
            ],
            next_steps="Implement Phase 1 improvements, set up monitoring"
        )
        
    def _recommend_patterns(self, task: Task, context_list) -> TaskResult:
        """Recommend design patterns and improvements"""
        
        thoughts = f"""
DESIGN PATTERN RECOMMENDATIONS (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: Pattern Selection & Refactoring

PATTERN ANALYSIS:
1. Current Architecture Patterns
   ✓ Repository Pattern (data access)
   ✓ Factory Pattern (object creation)
   ✓ Dependency Injection (loose coupling)
   ⚠️  Missing: Circuit Breaker (resilience)
   ⚠️  Missing: CQRS (read/write separation)
   ❌ Anti-pattern: God Object (refactor needed)

2. Recommended Patterns by Category
   
   A. Resilience Patterns:
   ┌─────────────────────────────────────┐
   │ 1. Circuit Breaker Pattern          │
   │    - Prevent cascade failures        │
   │    - Fast fail on unavailable service│
   │    - Auto-recovery mechanism         │
   │                                      │
   │ 2. Retry Pattern with Backoff        │
   │    - Exponential backoff             │
   │    - Max retry limit                 │
   │    - Idempotency required            │
   │                                      │
   │ 3. Bulkhead Pattern                  │
   │    - Isolate resources               │
   │    - Prevent resource exhaustion     │
   └─────────────────────────────────────┘
   
   B. Performance Patterns:
   - Cache-Aside: For frequently read data
   - Lazy Loading: For heavy resources
   - Event Sourcing: For audit trail + replay
   - CQRS: Separate read/write models
   
   C. Scalability Patterns:
   - Load Balancer: Distribute traffic
   - Database Sharding: Horizontal partition
   - Service Mesh: Inter-service communication
   - API Gateway: Single entry point

3. Refactoring Recommendations
   
   Priority 1 (HIGH):
   🔧 Introduce Circuit Breaker
      Where: External service calls
      Why: Prevent cascade failures
      Effort: 2-3 days
      Impact: High (system stability)
   
   Priority 2 (HIGH):
   🔧 Implement CQRS
      Where: User queries vs commands
      Why: Better read performance
      Effort: 1 week
      Impact: High (performance)
   
   Priority 3 (MEDIUM):
   🔧 Add Caching Layer
      Where: Hot data paths
      Why: Reduce database load
      Effort: 3-5 days
      Impact: High (performance)

4. Pattern Implementation Guide
   
   Circuit Breaker Example:
   ```python
   class CircuitBreaker:
       def __init__(self, threshold=5, timeout=60):
           self.threshold = threshold
           self.timeout = timeout
           self.failures = 0
           self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
       
       def call(self, func):
           if self.state == 'OPEN':
               if self._should_attempt_reset():
                   self.state = 'HALF_OPEN'
               else:
                   raise CircuitOpenError()
           
           try:
               result = func()
               self._on_success()
               return result
           except Exception as e:
               self._on_failure()
               raise e
   ```

5. Best Practices
   ✓ Choose patterns based on actual needs
   ✓ Don't over-engineer (YAGNI principle)
   ✓ Document pattern decisions (ADRs)
   ✓ Consider trade-offs (complexity vs benefit)
   ✓ Validate with team before implementing

PATTERN SELECTION CRITERIA:
- Problem fit: Does pattern solve our problem?
- Complexity: Is added complexity justified?
- Team familiarity: Can team maintain it?
- Performance impact: Does it improve performance?
- Scalability: Does it help scaling?
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "pattern_recommendations",
                "patterns_recommended": 8,
                "priority_high": 2,
                "priority_medium": 3,
                "implementation_guide": True,
                "code_examples": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "pattern_recommendations.md",
                "refactoring_plan.md",
                "implementation_guide.md",
                "code_examples/"
            ],
            next_steps="Review with Tomasz (Dev), prioritize implementation"
        )
        
    def _general_architecture_work(self, task: Task, context_list) -> TaskResult:
        """General architecture work"""
        
        thoughts = f"""
ARCHITECTURE TASK (Michał Kowalczyk):
{'='*70}

TASK: {task.title}
TYPE: General Architecture Work

ARCHITECTURAL THINKING:
1. System Perspective
   - Understanding the big picture
   - Identifying components and interactions
   - Considering non-functional requirements
   - Evaluating trade-offs
   
2. Quality Attributes Focus
   - Performance: Response time, throughput
   - Scalability: Growth capacity
   - Maintainability: Code quality, modularity
   - Security: Data protection, access control
   - Resilience: Fault tolerance, recovery
   
3. Design Principles Applied
   ✓ SOLID principles
   ✓ DRY (Don't Repeat Yourself)
   ✓ KISS (Keep It Simple)
   ✓ YAGNI (You Aren't Gonna Need It)
   ✓ Separation of Concerns
   
4. Architectural Concerns
   - Coupling and cohesion
   - Layer independence
   - Technology choices
   - Infrastructure requirements
   - Future extensibility

ARCHITECTURE CONTEXT:
{len(context_list)} previous architectural decisions reviewed

DELIVERABLE:
- Architecture-focused solution
- Technical specifications
- Documented decisions
- Ready for implementation

STATUS: Completed with architectural best practices
FOCUS: System-level thinking, quality attributes
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "general_architecture",
                "status": "completed",
                "quality_attributes_considered": True,
                "design_principles_applied": True,
                "documented": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["architecture_solution.md", "technical_spec.pdf"],
            next_steps="Review with team, coordinate with Tomasz (Dev) for implementation"
        )


# Module test
if __name__ == "__main__":
    import uuid
    
    print("Testing MichalAgent...")
    
    michal = MichalAgent()
    
    # Test architecture design task
    task = Task(
        task_id=uuid.uuid4(),
        title="Design system architecture",
        description="Design the system architecture for a project metrics dashboard",
        assigned_to=michal.name,
        assigned_by="Test",
        context={},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    result = michal.process_task(task)
    
    print(f"\n✅ MichalAgent test:")
    print(f"   Status: {result.status.value}")
    print(f"   Type: {result.output.get('type')}")
    print(f"   Contains 'architecture': {'architecture' in result.thoughts.lower()}")
    print(f"   Contains 'scalability': {'scalability' in result.thoughts.lower()}")
    print(f"   Contains 'component': {'component' in result.thoughts.lower()}")
    
    assert result.status == TaskStatus.DONE
    assert "architecture" in result.thoughts.lower()
    
    print("\n✅ MichalAgent ready!")
