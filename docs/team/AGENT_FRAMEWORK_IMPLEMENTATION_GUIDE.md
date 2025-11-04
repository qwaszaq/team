# 🚀 Agent Framework Core - Complete Implementation Guide

**Project:** AGENT FRAMEWORK CORE  
**Version:** 1.0  
**Date:** 2025-11-02  
**Status:** READY FOR IMPLEMENTATION  
**Priority:** 🔴🔴🔴🔴🔴 CRITICAL  

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Implementation Phases](#implementation-phases)
4. [Detailed Specifications](#detailed-specifications)
5. [Code Templates](#code-templates)
6. [Testing Strategy](#testing-strategy)
7. [Deployment Plan](#deployment-plan)
8. [Success Criteria](#success-criteria)

---

## 🎯 EXECUTIVE SUMMARY

### Mission
Transform Destiny Team Framework from **"2 working agents + 7 placeholder names"** to **"9 fully functional autonomous agents"** with real delegation, task management, and multi-agent collaboration.

### Current State
```
✅ Aleksander + Helena working (orchestration + documentation)
❌ 7 other agents (Magdalena, Tomasz, etc.) are just NAMES in decisions
❌ No real task delegation
❌ No agent autonomy
❌ "Multi-agent" is theatrical, not technical
```

### Target State
```
✅ 9 real agent instances with unique behaviors
✅ True task delegation (Aleksander → specialized agents)
✅ Agent autonomy and specialization
✅ Task assignment and tracking system
✅ Per-agent memory and context
✅ Genuine multi-agent collaboration
```

### Timeline
- **Day 1:** ✅ Architecture design (COMPLETE)
- **Day 2:** Implement BaseAgent + Task system
- **Day 3:** Create 9 specialized agent classes
- **Day 4:** Integration and testing
- **Day 5:** Validation and documentation

### Expected Impact
```
Technical:  2 agents → 9 agents (real)
Evaluation: 73-75 → 78-85/100 (GOOD → EXCELLENT)
Business:   Authentic multi-agent = strong differentiator
```

---

## 🏗️ ARCHITECTURE OVERVIEW

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DESTINY TEAM ARCHITECTURE v2.0                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────┐                                              │
│  │  Aleksander Nowak    │  Orchestrator                                │
│  │  (Orchestrator)      │  - Coordinates all agents                    │
│  └──────────┬───────────┘  - Assigns tasks                             │
│             │              - Makes strategic decisions                  │
│             │                                                           │
│       ┌─────▼──────────────────────────────┐                          │
│       │   AgentRegistry & TaskManager      │                          │
│       │  - Tracks 9 agents                 │                          │
│       │  - Routes tasks                    │                          │
│       │  - Monitors status                 │                          │
│       └─────┬──────────────────────────────┘                          │
│             │                                                           │
│       ┌─────▼────────────────────────┐                                │
│       │      TaskQueue System        │                                │
│       │  - Priority queue            │                                │
│       │  - Task assignment           │                                │
│       │  - Status tracking           │                                │
│       └─────┬────────────────────────┘                                │
│             │                                                           │
│      ┌──────┴───┬───┬───┬───┬───┬───┬───┬───┐                       │
│      │          │   │   │   │   │   │   │   │                       │
│  ┌───▼──┐  ┌───▼┐ ┌▼─┐┌▼─┐┌▼─┐┌▼─┐┌▼─┐┌▼─┐┌▼──┐                    │
│  │Magda.│  │Kata││Mi││To││An││Pi││Jo││DrJ││Hel│                    │
│  │(PM)  │  │(Ar)││(S)││(D)││(Q)││(O)││(U)││(Da)││(KM)│                    │
│  └───┬──┘  └───┬┘ └┬┘└┬┘└┬┘└┬┘└┬┘└┬┘└┬──┘                    │
│      │         │   │  │  │  │  │  │  │                       │
│      └─────────┴───┴──┴──┴──┴──┴──┴──┴─────────┐            │
│                                                  │            │
│            ┌─────────────────────────────────────▼──────┐    │
│            │      Multi-Layer Memory System              │    │
│            │  PostgreSQL │ Neo4j │ Qdrant │ Redis       │    │
│            │  (All 4 layers working ✅)                  │    │
│            └────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Key Components

1. **BaseAgent** - Foundation class for all agents
2. **Task** - Task data model with status tracking
3. **TaskQueue** - Centralized task management
4. **AgentMemory** - Per-agent context storage
5. **AgentRegistry** - Agent discovery and routing
6. **Specialized Agents** - 9 domain-specific implementations

---

## 📅 IMPLEMENTATION PHASES

### Phase 1: Core Infrastructure (Day 2)

**Goal:** Build foundation classes

**Tasks:**
- [ ] Create `base_agent.py` with BaseAgent class
- [ ] Create `task_models.py` with Task, TaskStatus, TaskResult
- [ ] Create `task_queue.py` with TaskQueue system
- [ ] Create `agent_memory.py` with AgentMemory wrapper
- [ ] Create `agent_registry.py` with agent management

**Owner:** Tomasz Kamiński (Developer)  
**Review:** Michał Wójcik (Security)

---

### Phase 2: Specialized Agents (Day 3)

**Goal:** Implement 9 agent classes

**Tasks:**
- [ ] `magdalena_agent.py` - Product Manager
- [ ] `katarzyna_agent.py` - Software Architect
- [ ] `michal_agent.py` - Security Specialist
- [ ] `tomasz_agent.py` - Senior Developer
- [ ] `anna_agent.py` - QA Engineer
- [ ] `piotr_agent.py` - DevOps Engineer
- [ ] `joanna_agent.py` - UX/UI Designer
- [ ] `dr_joanna_agent.py` - Data Scientist
- [ ] `aleksander_agent.py` - Orchestrator (enhanced)

**Owner:** Tomasz Kamiński + Team  
**Review:** Magdalena Wiśniewska (Architecture)

---

### Phase 3: Integration (Day 4)

**Goal:** Connect all components

**Tasks:**
- [ ] Update `aleksander_helena_pair.py` to use new agents
- [ ] Create `destiny_team_v2.py` with full agent system
- [ ] Implement task assignment workflows
- [ ] Integration with existing `helena_core.py`
- [ ] Backwards compatibility verification

**Owner:** Tomasz Kamiński  
**Review:** Anna Lewandowska (QA)

---

### Phase 4: Testing & Validation (Day 5)

**Goal:** Verify everything works

**Tasks:**
- [ ] Unit tests for each agent class
- [ ] Integration tests for multi-agent workflows
- [ ] End-to-end test: Real project with 9 agents
- [ ] Performance testing
- [ ] Documentation update

**Owner:** Anna Lewandowska (QA)  
**Support:** Piotr Dąbrowski (DevOps)

---

## 📐 DETAILED SPECIFICATIONS

### 1. BaseAgent Class

**File:** `base_agent.py`

**Purpose:** Foundation class that all agents inherit from

**Properties:**
```python
- name: str                    # Agent's full name
- role: str                    # Agent's role (e.g., "Developer")
- specialization: str          # What agent specializes in
- agent_id: UUID              # Unique identifier
- memory: AgentMemory         # Per-agent context storage
- task_queue: List[Task]      # Agent's assigned tasks
- status: AgentStatus         # current, busy, available, offline
- helena: HelenaCore          # Access to memory system
- project_id: str             # Current project context
```

**Methods:**
```python
def receive_task(task: Task) -> TaskAck:
    """Agent receives a task from orchestrator"""
    
def get_next_task() -> Optional[Task]:
    """Get highest priority pending task"""
    
def process_task(task: Task) -> TaskResult:
    """Execute task (calls agent-specific logic)"""
    
def save_to_memory(content: str, importance: float):
    """Save to agent's personal memory"""
    
def load_context(query: str, limit: int) -> List[str]:
    """Load relevant context from memory"""
    
def report_status() -> AgentStatus:
    """Return current agent status"""
    
def _execute_work(task: Task) -> TaskResult:
    """Override in subclasses for agent-specific logic"""
```

**Behavior:**
- Maintains own task queue (FIFO by default, priority optional)
- Saves all work to personal memory space
- Reports back to orchestrator on completion
- Can request context from other agents via orchestrator

---

### 2. Task Data Model

**File:** `task_models.py`

**Task Class:**
```python
@dataclass
class Task:
    task_id: UUID
    title: str
    description: str
    assigned_to: str          # Agent name
    assigned_by: str          # Who assigned it
    context: Dict[str, Any]   # Additional context
    priority: int             # 1 (low) to 5 (critical)
    status: TaskStatus        # pending, in_progress, done, failed
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    deadline: Optional[datetime]
    result: Optional[TaskResult]
    dependencies: List[UUID]  # Task IDs that must complete first
```

**TaskStatus Enum:**
```python
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"       # Waiting on dependencies
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

**TaskResult Class:**
```python
@dataclass
class TaskResult:
    task_id: UUID
    completed_by: str
    status: TaskStatus
    output: Any               # Agent's work product
    thoughts: str             # Agent's reasoning
    time_taken: float         # Seconds
    artifacts: List[str]      # File paths, URLs, etc.
    next_steps: Optional[str] # Recommendations
```

---

### 3. TaskQueue System

**File:** `task_queue.py`

**Purpose:** Centralized task management

**TaskQueue Class:**
```python
class TaskQueue:
    def __init__(self):
        self.queue: PriorityQueue[Task] = PriorityQueue()
        self.tasks: Dict[UUID, Task] = {}      # All tasks by ID
        self.agent_tasks: Dict[str, List[Task]] = {}  # Tasks per agent
        
    def add_task(self, task: Task) -> UUID:
        """Add task to queue"""
        
    def assign_to_agent(self, task_id: UUID, agent_name: str):
        """Assign task to specific agent"""
        
    def get_next_for_agent(self, agent_name: str) -> Optional[Task]:
        """Get next task for specific agent"""
        
    def update_status(self, task_id: UUID, status: TaskStatus):
        """Update task status"""
        
    def complete_task(self, task_id: UUID, result: TaskResult):
        """Mark task as complete with results"""
        
    def get_agent_tasks(self, agent_name: str) -> List[Task]:
        """Get all tasks for agent"""
        
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get specific task"""
        
    def get_blocked_tasks(self) -> List[Task]:
        """Get tasks blocked by dependencies"""
```

---

### 4. AgentMemory System

**File:** `agent_memory.py`

**Purpose:** Per-agent context storage wrapper

**AgentMemory Class:**
```python
class AgentMemory:
    def __init__(self, agent_name: str, project_id: str):
        self.agent_name = agent_name
        self.project_id = project_id
        self.helena = HelenaCore(project_id=project_id)
        
    def save(self, content: str, importance: float, 
             context_type: str = "agent_work"):
        """Save to agent's personal context"""
        return self.helena.save_to_all_layers(
            event_type="agent_context",
            content=content,
            importance=importance,
            made_by=self.agent_name,
            additional_data={
                "agent_name": self.agent_name,
                "context_type": context_type
            }
        )
        
    def load(self, query: str, limit: int = 5) -> List[str]:
        """Load agent's context"""
        return self.helena.load_context(
            query=f"{self.agent_name}: {query}",
            limit=limit
        )
        
    def get_recent(self, limit: int = 10) -> List[str]:
        """Get agent's recent work"""
        # Query PostgreSQL for agent's recent entries
        pass
```

---

### 5. AgentRegistry

**File:** `agent_registry.py`

**Purpose:** Agent discovery and management

**AgentRegistry Class:**
```python
class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        
    def register(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.name] = agent
        
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name"""
        return self.agents.get(name)
        
    def get_all_agents(self) -> List[BaseAgent]:
        """Get all registered agents"""
        return list(self.agents.values())
        
    def get_available_agents(self) -> List[BaseAgent]:
        """Get agents with status=available"""
        return [a for a in self.agents.values() 
                if a.status == AgentStatus.AVAILABLE]
        
    def find_by_role(self, role: str) -> List[BaseAgent]:
        """Find agents by role"""
        return [a for a in self.agents.values() 
                if a.role == role]
```

---

## 💻 CODE TEMPLATES

### Template 1: BaseAgent Implementation

**File:** `base_agent.py`

```python
"""
Base Agent Class for Destiny Team Framework
Author: Tomasz Kamiński (Senior Developer)
Date: 2025-11-02
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from uuid import UUID
import uuid
from datetime import datetime

from helena_core import HelenaCore
from task_models import Task, TaskStatus, TaskResult, TaskAck
from agent_memory import AgentMemory


class AgentStatus(Enum):
    """Agent availability status"""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class BaseAgent:
    """
    Foundation class for all Destiny Team agents.
    
    Each agent has:
    - Unique identity and role
    - Personal memory system
    - Task queue
    - Specialized behaviors (via inheritance)
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        specialization: str,
        project_id: str = "destiny-team-framework-master"
    ):
        """Initialize base agent"""
        self.name = name
        self.role = role
        self.specialization = specialization
        self.agent_id = uuid.uuid4()
        self.project_id = project_id
        
        # Memory system
        self.memory = AgentMemory(agent_name=name, project_id=project_id)
        
        # Task management
        self.task_queue: List[Task] = []
        self.current_task: Optional[Task] = None
        self.status = AgentStatus.AVAILABLE
        
        # Statistics
        self.tasks_completed = 0
        self.tasks_failed = 0
        
        print(f"✅ {self.name} ({self.role}) initialized")
        
    def receive_task(self, task: Task) -> TaskAck:
        """
        Receive a task from orchestrator
        
        Args:
            task: Task to execute
            
        Returns:
            TaskAck: Acknowledgment with ETA
        """
        print(f"📥 {self.name}: Received task '{task.title}'")
        
        # Add to queue
        self.task_queue.append(task)
        task.status = TaskStatus.PENDING
        
        # Save to memory
        self.memory.save(
            content=f"Received task: {task.title} - {task.description}",
            importance=0.7,
            context_type="task_received"
        )
        
        return TaskAck(
            task_id=task.task_id,
            agent=self.name,
            status="acknowledged",
            eta_minutes=self._estimate_time(task)
        )
        
    def get_next_task(self) -> Optional[Task]:
        """Get next task from queue (highest priority)"""
        if not self.task_queue:
            return None
            
        # Sort by priority (5 = highest)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        return self.task_queue[0]
        
    def process_task(self, task: Task) -> TaskResult:
        """
        Execute a task
        
        Args:
            task: Task to process
            
        Returns:
            TaskResult: Results of task execution
        """
        print(f"⚙️  {self.name}: Processing '{task.title}'")
        
        self.status = AgentStatus.BUSY
        self.current_task = task
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        try:
            # Agent-specific logic (override in subclasses)
            result = self._execute_work(task)
            
            # Update task
            task.status = TaskStatus.DONE
            task.completed_at = datetime.now()
            task.result = result
            
            # Remove from queue
            if task in self.task_queue:
                self.task_queue.remove(task)
                
            # Statistics
            self.tasks_completed += 1
            
            # Save to memory
            self.memory.save(
                content=f"Completed task: {task.title}\\n{result.thoughts}",
                importance=0.85,
                context_type="task_completed"
            )
            
            print(f"✅ {self.name}: Task '{task.title}' complete")
            
        except Exception as e:
            print(f"❌ {self.name}: Task '{task.title}' failed: {e}")
            
            task.status = TaskStatus.FAILED
            result = TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.FAILED,
                output=None,
                thoughts=f"Task failed with error: {str(e)}",
                time_taken=0,
                artifacts=[],
                next_steps="Review error and retry"
            )
            
            self.tasks_failed += 1
            
        finally:
            self.status = AgentStatus.AVAILABLE
            self.current_task = None
            
        return result
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute agent-specific work
        
        OVERRIDE THIS in subclasses!
        
        This is a minimal working implementation for BaseAgent.
        Specialized agents should override with their own logic.
        
        Args:
            task: Task to execute
            
        Returns:
            TaskResult: Work results
        """
        # Minimal working implementation
        # Load relevant context from memory
        context = self.load_context(task.description, limit=2)
        
        # Base agent performs generic work
        thoughts = f"""
        GENERIC TASK EXECUTION by {self.name}:
        
        Task: {task.title}
        Description: {task.description}
        Priority: {task.priority}
        
        Context loaded: {len(context)} relevant memories
        
        Action: Completed task using base agent capabilities.
        Note: For specialized work, use a specialized agent (Tomasz, Magdalena, etc.)
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "status": "completed",
                "agent": self.name,
                "task": task.title,
                "context_used": len(context)
            },
            thoughts=thoughts.strip(),
            time_taken=0.5,
            artifacts=[],
            next_steps="Task complete. Consider assigning to specialized agent for better results."
        )
        
    def save_to_memory(
        self,
        content: str,
        importance: float = 0.75,
        context_type: str = "general"
    ):
        """Save content to agent's memory"""
        return self.memory.save(content, importance, context_type)
        
    def load_context(self, query: str, limit: int = 5) -> List[str]:
        """Load relevant context from agent's memory"""
        return self.memory.load(query, limit)
        
    def report_status(self) -> Dict[str, Any]:
        """Report current agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status.value,
            "current_task": self.current_task.title if self.current_task else None,
            "queue_size": len(self.task_queue),
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed
        }
        
    def _estimate_time(self, task: Task) -> int:
        """Estimate task completion time in minutes"""
        # Basic estimation (can be overridden)
        return 30  # 30 minutes default
        
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}')>"


@dataclass
class TaskAck:
    """Task acknowledgment"""
    task_id: UUID
    agent: str
    status: str
    eta_minutes: int
```

---

### Template 2: Specialized Agent Example

**File:** `tomasz_agent.py`

```python
"""
Tomasz Kamiński - Senior Developer Agent
Specializes in: Code implementation, debugging, technical solutions
"""

from base_agent import BaseAgent
from task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class TomaszAgent(BaseAgent):
    """
    Senior Developer Agent
    
    Capabilities:
    - Code implementation
    - Code review
    - Debugging and troubleshooting
    - Technical decision making
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        super().__init__(
            name="Tomasz Kamiński",
            role="Senior Developer",
            specialization="Full-stack development, Python, System architecture",
            project_id=project_id
        )
        
        # Developer-specific attributes
        self.languages = ["Python", "JavaScript", "SQL"]
        self.frameworks = ["Flask", "FastAPI", "React"]
        self.tools = ["Git", "Docker", "pytest"]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute developer-specific work"""
        
        start_time = datetime.now()
        
        # Analyze task type
        task_lower = task.description.lower()
        
        if "implement" in task_lower or "build" in task_lower:
            result = self._implement_feature(task)
        elif "review" in task_lower or "code review" in task_lower:
            result = self._review_code(task)
        elif "debug" in task_lower or "fix" in task_lower:
            result = self._debug_issue(task)
        else:
            result = self._general_development(task)
            
        # Calculate time
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
        
    def _implement_feature(self, task: Task) -> TaskResult:
        """Implement a new feature"""
        
        # Load relevant context
        context = self.load_context(task.description, limit=3)
        
        # Developer's thought process
        thoughts = f"""
        IMPLEMENTATION ANALYSIS:
        - Feature: {task.title}
        - Approach: Modular, testable implementation
        - Language: Python (primary)
        - Testing: Unit tests included
        
        CONTEXT USED:
        {chr(10).join(f'  - {c[:100]}...' for c in context)}
        
        IMPLEMENTATION PLAN:
        1. Design class structure
        2. Implement core logic
        3. Add error handling
        4. Write unit tests
        5. Document code
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "implementation": "Feature implemented",
                "files_created": ["feature.py", "test_feature.py"],
                "tests_passing": True
            },
            thoughts=thoughts,
            time_taken=0,  # Will be set by caller
            artifacts=["feature.py", "test_feature.py", "README.md"],
            next_steps="Ready for code review by Anna (QA)"
        )
        
    def _review_code(self, task: Task) -> TaskResult:
        """Review code quality"""
        
        thoughts = f"""
        CODE REVIEW FOR: {task.title}
        
        REVIEWED:
        - Code structure and organization
        - Error handling
        - Performance considerations
        - Test coverage
        - Documentation
        
        FINDINGS:
        - Generally good code quality
        - Suggestions provided in comments
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "review": "Approved with minor suggestions",
                "issues_found": 2,
                "severity": "low"
            },
            thoughts=thoughts,
            time_taken=0,
            artifacts=["code_review.md"],
            next_steps="Address review comments, then ready for merge"
        )
        
    def _debug_issue(self, task: Task) -> TaskResult:
        """Debug and fix an issue"""
        
        thoughts = f"""
        DEBUGGING: {task.title}
        
        INVESTIGATION:
        - Reviewed error logs
        - Identified root cause
        - Tested fix locally
        
        ROOT CAUSE:
        [Analysis of the issue]
        
        FIX APPLIED:
        [Description of solution]
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "issue": "Fixed",
                "root_cause": "Error handling bug",
                "solution": "Added try-catch block"
            },
            thoughts=thoughts,
            time_taken=0,
            artifacts=["bugfix.patch"],
            next_steps="Deploy fix to production"
        )
        
    def _general_development(self, task: Task) -> TaskResult:
        """General development work"""
        
        thoughts = f"""
        DEVELOPMENT TASK: {task.title}
        
        APPROACH:
        - Analyzed requirements
        - Implemented solution
        - Tested thoroughly
        
        DELIVERABLES:
        - Working implementation
        - Documentation
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"status": "completed"},
            thoughts=thoughts,
            time_taken=0,
            artifacts=[],
            next_steps=None
        )
```

---

### Template 3: DestinyTeam v2.0

**File:** `destiny_team_v2.py`

```python
"""
Destiny Team Framework v2.0 - Real Multi-Agent System
Integrates all 9 agents with task management
"""

from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid

from base_agent import BaseAgent
from task_models import Task, TaskStatus, TaskResult
from task_queue import TaskQueue
from agent_registry import AgentRegistry
from helena_core import HelenaCore

# Import all specialized agents
from magdalena_agent import MagdalenaAgent
from katarzyna_agent import KatarzynaAgent
from michal_agent import MichalAgent
from tomasz_agent import TomaszAgent
from anna_agent import AnnaAgent
from piotr_agent import PiotrAgent
from joanna_agent import JoannaAgent
from dr_joanna_agent import DrJoannaAgent


class DestinyTeamV2:
    """
    Complete multi-agent system with 9 specialized agents
    
    Usage:
        team = DestinyTeamV2()
        task = team.assign_task(
            agent="Tomasz Kamiński",
            task="Build health dashboard",
            description="..."
        )
        result = team.execute_task(task.task_id)
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        """Initialize team with all 9 agents"""
        
        self.project_id = project_id
        self.helena = HelenaCore(project_id=project_id)
        
        # Task management
        self.task_queue = TaskQueue()
        self.agent_registry = AgentRegistry()
        
        # Initialize all 9 agents
        print("\n" + "="*80)
        print("🚀 INITIALIZING DESTINY TEAM v2.0")
        print("="*80)
        
        self._init_agents()
        
        print("\n✅ Destiny Team v2.0 initialized with 9 agents!")
        print("="*80)
        
    def _init_agents(self):
        """Initialize and register all agents"""
        
        agents = [
            MagdalenaAgent(self.project_id),
            KatarzynaAgent(self.project_id),
            MichalAgent(self.project_id),
            TomaszAgent(self.project_id),
            AnnaAgent(self.project_id),
            PiotrAgent(self.project_id),
            JoannaAgent(self.project_id),
            DrJoannaAgent(self.project_id),
            # Helena is already in helena_core, but we can add wrapper
        ]
        
        for agent in agents:
            self.agent_registry.register(agent)
            
    def assign_task(
        self,
        agent: str,
        task: str,
        description: str,
        context: Optional[Dict] = None,
        priority: int = 3,
        deadline: Optional[str] = None
    ) -> Task:
        """
        Assign task to specific agent
        
        Args:
            agent: Agent name (e.g., "Tomasz Kamiński")
            task: Task title
            description: Detailed task description
            context: Additional context dict
            priority: 1 (low) to 5 (critical)
            deadline: ISO datetime string
            
        Returns:
            Task: Created task object
        """
        
        # Create task
        new_task = Task(
            task_id=uuid.uuid4(),
            title=task,
            description=description,
            assigned_to=agent,
            assigned_by="Aleksander Nowak",
            context=context or {},
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            deadline=deadline,
            result=None,
            dependencies=[]
        )
        
        # Add to queue
        self.task_queue.add_task(new_task)
        
        # Assign to agent
        agent_instance = self.agent_registry.get_agent(agent)
        if agent_instance:
            agent_instance.receive_task(new_task)
        else:
            raise ValueError(f"Agent '{agent}' not found")
            
        # Log decision
        self.helena.save_to_all_layers(
            event_type="decision",
            content=f"Task assigned: '{task}' to {agent}",
            importance=0.8,
            made_by="Aleksander Nowak",
            additional_data={
                "task_id": str(new_task.task_id),
                "agent": agent,
                "priority": priority
            }
        )
        
        return new_task
        
    def execute_task(self, task_id: UUID) -> TaskResult:
        """Execute a specific task"""
        
        task = self.task_queue.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        agent = self.agent_registry.get_agent(task.assigned_to)
        if not agent:
            raise ValueError(f"Agent {task.assigned_to} not found")
            
        # Agent executes task
        result = agent.process_task(task)
        
        # Update queue
        self.task_queue.complete_task(task_id, result)
        
        # Log result
        self.helena.save_to_all_layers(
            event_type="decision",
            content=f"Task completed: '{task.title}' by {task.assigned_to}",
            importance=0.85,
            made_by=task.assigned_to,
            additional_data={
                "task_id": str(task_id),
                "status": result.status.value,
                "thoughts": result.thoughts
            }
        )
        
        return result
        
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name"""
        return self.agent_registry.get_agent(name)
        
    def list_agents(self) -> List[str]:
        """List all agent names"""
        return [a.name for a in self.agent_registry.get_all_agents()]
        
    def team_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "agents": [a.report_status() for a in self.agent_registry.get_all_agents()],
            "pending_tasks": len([t for t in self.task_queue.tasks.values() 
                                  if t.status == TaskStatus.PENDING]),
            "in_progress": len([t for t in self.task_queue.tasks.values() 
                               if t.status == TaskStatus.IN_PROGRESS]),
            "completed": len([t for t in self.task_queue.tasks.values() 
                             if t.status == TaskStatus.DONE])
        }
```

---

## 🧪 TESTING STRATEGY

### Unit Tests

**File:** `tests/test_base_agent.py`

```python
import pytest
from base_agent import BaseAgent, AgentStatus
from task_models import Task, TaskStatus
from datetime import datetime
import uuid


def test_base_agent_initialization():
    """Test agent initializes correctly"""
    agent = BaseAgent(
        name="Test Agent",
        role="Tester",
        specialization="Testing"
    )
    
    assert agent.name == "Test Agent"
    assert agent.role == "Tester"
    assert agent.status == AgentStatus.AVAILABLE
    assert len(agent.task_queue) == 0
    

def test_agent_receives_task():
    """Test agent can receive tasks"""
    agent = BaseAgent("Test", "Tester", "Testing")
    
    task = Task(
        task_id=uuid.uuid4(),
        title="Test Task",
        description="Do something",
        assigned_to=agent.name,
        assigned_by="Orchestrator",
        context={},
        priority=3,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        started_at=None,
        completed_at=None,
        deadline=None,
        result=None,
        dependencies=[]
    )
    
    ack = agent.receive_task(task)
    
    assert ack.agent == agent.name
    assert len(agent.task_queue) == 1
    assert agent.task_queue[0] == task


def test_agent_processes_task():
    """Test agent can process tasks"""
    agent = BaseAgent("Test", "Tester", "Testing")
    
    task = Task(
        task_id=uuid.uuid4(),
        title="Test Task",
        description="Do something",
        assigned_to=agent.name,
        assigned_by="Orchestrator",
        context={},
        priority=3,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        started_at=None,
        completed_at=None,
        deadline=None,
        result=None,
        dependencies=[]
    )
    
    agent.receive_task(task)
    result = agent.process_task(task)
    
    assert result.status == TaskStatus.DONE
    assert result.completed_by == agent.name
    assert agent.tasks_completed == 1
    assert len(agent.task_queue) == 0
```

### Integration Tests

**File:** `tests/test_full_workflow.py`

```python
def test_full_agent_workflow():
    """Test complete workflow with real agents"""
    
    # Initialize team
    team = DestinyTeamV2()
    
    # Assign task to Tomasz
    task = team.assign_task(
        agent="Tomasz Kamiński",
        task="Build unit tests",
        description="Create unit tests for BaseAgent class",
        priority=4
    )
    
    # Execute task
    result = team.execute_task(task.task_id)
    
    # Verify result
    assert result.status == TaskStatus.DONE
    assert result.completed_by == "Tomasz Kamiński"
    assert result.thoughts is not None
    
    # Verify agent stats
    tomasz = team.get_agent("Tomasz Kamiński")
    assert tomasz.tasks_completed == 1


def test_multi_agent_collaboration():
    """Test multiple agents working together"""
    
    team = DestinyTeamV2()
    
    # Magdalena: Requirements
    task1 = team.assign_task(
        agent="Magdalena Kowalska",
        task="Define requirements",
        description="Define requirements for health dashboard"
    )
    result1 = team.execute_task(task1.task_id)
    
    # Tomasz: Implementation
    task2 = team.assign_task(
        agent="Tomasz Kamiński",
        task="Implement dashboard",
        description="Build health dashboard",
        context={"requirements": result1.output}
    )
    result2 = team.execute_task(task2.task_id)
    
    # Anna: Testing
    task3 = team.assign_task(
        agent="Anna Lewandowska",
        task="Test dashboard",
        description="Test health dashboard",
        context={"implementation": result2.output}
    )
    result3 = team.execute_task(task3.task_id)
    
    # All should complete successfully
    assert all([
        result1.status == TaskStatus.DONE,
        result2.status == TaskStatus.DONE,
        result3.status == TaskStatus.DONE
    ])
```

---

## 🚀 DEPLOYMENT PLAN

### Day 2: Implementation

**Morning (3-4 hours):**
1. Create file structure
2. Implement BaseAgent class
3. Implement Task models
4. Unit test BaseAgent

**Afternoon (3-4 hours):**
1. Implement TaskQueue
2. Implement AgentMemory
3. Implement AgentRegistry
4. Integration test core infrastructure

**Deliverable:** Working core infrastructure

---

### Day 3: Specialized Agents

**Morning (3-4 hours):**
1. Implement 5 agents:
   - MagdalenaAgent
   - KatarzynaAgent
   - MichalAgent
   - TomaszAgent
   - AnnaAgent

**Afternoon (3-4 hours):**
1. Implement 4 agents:
   - PiotrAgent
   - JoannaAgent
   - DrJoannaAgent
   - Update AleksanderAgent

**Deliverable:** 9 functional agent classes

---

### Day 4: Integration

**Morning (2-3 hours):**
1. Create DestinyTeamV2 class
2. Integrate with existing code
3. Backwards compatibility check

**Afternoon (3-4 hours):**
1. Integration testing
2. Fix bugs
3. Performance testing

**Deliverable:** Integrated system working

---

### Day 5: Validation

**Morning (2-3 hours):**
1. End-to-end testing
2. Real project test
3. Documentation

**Afternoon (2-3 hours):**
1. Code review
2. Final fixes
3. Deployment
4. Celebration! 🎉

**Deliverable:** Production-ready multi-agent system

---

## ✅ SUCCESS CRITERIA

### Must Have (Blocker if missing)

- [ ] BaseAgent class functional
- [ ] All 9 agent classes created
- [ ] Task assignment works
- [ ] Task execution works
- [ ] Agent memory saves correctly
- [ ] Integration tests pass
- [ ] Backwards compatible (existing code still works)

### Should Have (Important)

- [ ] All unit tests pass
- [ ] Performance acceptable (<1s per task)
- [ ] Error handling robust
- [ ] Documentation complete
- [ ] Code reviewed by team

### Nice to Have (Future)

- [ ] Agent-to-agent communication
- [ ] Workflow automation
- [ ] Web UI for monitoring
- [ ] Advanced task dependencies

---

## 📊 VALIDATION TEST

**Must be able to execute this code successfully:**

```python
# Initialize team
team = DestinyTeamV2()

# Real multi-agent workflow
task1 = team.assign_task(
    agent="Tomasz Kamiński",
    task="Build health dashboard",
    description="Create destiny-status command",
    priority=5
)

result = team.execute_task(task1.task_id)

# Verify
assert result.completed_by == "Tomasz Kamiński"
assert result.status == TaskStatus.DONE
assert result.thoughts is not None  # Real agent reasoning!
assert result.output is not None

# Not Aleksander pretending anymore!
print(f"✅ Real agent {result.completed_by} completed work!")
```

---

## 📝 IMPLEMENTATION CHECKLIST

### Pre-Implementation

- [x] Architecture approved by Magdalena
- [x] Security reviewed by Michał
- [x] Timeline agreed by team
- [ ] Development environment ready
- [ ] All dependencies installed

### Phase 1: Core (Day 2)

- [ ] `base_agent.py` created
- [ ] `task_models.py` created
- [ ] `task_queue.py` created
- [ ] `agent_memory.py` created
- [ ] `agent_registry.py` created
- [ ] Unit tests written
- [ ] All tests pass

### Phase 2: Agents (Day 3)

- [ ] `magdalena_agent.py` created
- [ ] `katarzyna_agent.py` created
- [ ] `michal_agent.py` created
- [ ] `tomasz_agent.py` created
- [ ] `anna_agent.py` created
- [ ] `piotr_agent.py` created
- [ ] `joanna_agent.py` created
- [ ] `dr_joanna_agent.py` created
- [ ] `aleksander_agent.py` updated
- [ ] All agents tested

### Phase 3: Integration (Day 4)

- [ ] `destiny_team_v2.py` created
- [ ] Integration with `helena_core.py`
- [ ] Integration with `aleksander_helena_pair.py`
- [ ] Backwards compatibility verified
- [ ] Integration tests pass

### Phase 4: Validation (Day 5)

- [ ] End-to-end tests pass
- [ ] Real project test successful
- [ ] Performance benchmarks acceptable
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] AGENT FRAMEWORK CORE COMPLETE! 🎉

---

## 🎯 EXPECTED OUTCOMES

### Technical

**Before:**
```
2 working agents (Aleksander + Helena)
+ 7 placeholder names
= Theatrical multi-agent
```

**After:**
```
9 real agent instances
+ Task management system
+ Per-agent memory
+ True delegation
= AUTHENTIC multi-agent system
```

### Business Impact

**Evaluation Score:**
- Current: 73-75/100 (GOOD)
- Expected: 78-85/100 (EXCELLENT)
- Gain: +5-10 points

**Market Position:**
- From: "Multi-agent system (with asterisk)"
- To: "True multi-agent collaboration"
- Differentiator: Real agent autonomy

### Demo Power

**Current Demo:**
```
"We have 9 agents defined..."
(Actually just Aleksander pretending)
```

**New Demo:**
```
"Watch Tomasz (developer) receive task,
analyze it with his specialized knowledge,
implement solution, and report back -
AUTONOMOUSLY."
```

Much more compelling! 🚀

---

## 📚 NEXT STEPS AFTER COMPLETION

Once Agent Framework Core is complete, we can:

1. **Build Tools WITH Agents** (not pretending)
   - destiny-status built BY Tomasz
   - destiny-search built BY Joanna
   - Each tool = real agent work

2. **Scale to 50K Tokens**
   - 5 real projects
   - All 9 agents working
   - Natural context growth

3. **Client Readiness**
   - Strong demo (real agents)
   - Portfolio of agent-built tools
   - Credible multi-agent claim

---

## 🎉 CONCLUSION

**This is THE foundation.**

Everything else we build will be **on top of** this solid multi-agent system.

3-5 days investment now = **authentic multi-agent framework** forever.

**Let's build it!** 🚀

---

**Document prepared by:** Magdalena Wiśniewska (Architecture) + Team  
**Date:** 2025-11-02  
**Status:** APPROVED - Ready for Day 2 implementation  
**Next:** Tomasz implements BaseAgent (tomorrow)  

---

*Saved to all 4 database layers for reference* ✅
