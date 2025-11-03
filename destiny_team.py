"""
The Destiny Development Team - Multi-Agent System
A multidisciplinary AI team for non-programmers to build sophisticated projects
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid


class MessageType(Enum):
    REQUEST = "REQUEST"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    DEBATE = "DEBATE"
    APPROVAL = "APPROVAL"
    UPDATE = "UPDATE"
    RESPONSE = "RESPONSE"


class ProjectPhase(Enum):
    DISCOVERY = "DISCOVERY"
    PLANNING = "PLANNING"
    ARCHITECTURE = "ARCHITECTURE"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    DEPLOYMENT = "DEPLOYMENT"
    MAINTENANCE = "MAINTENANCE"


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    recipient: Optional[str] = None  # None = broadcast to all
    message_type: MessageType = MessageType.ANNOUNCEMENT
    content: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    requires_response: bool = False
    response_to: Optional[str] = None  # ID of message this responds to


@dataclass
class ProjectState:
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = ""
    description: str = ""
    current_phase: ProjectPhase = ProjectPhase.DISCOVERY
    requirements: Dict[str, Any] = field(default_factory=dict)
    architecture: Dict[str, Any] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    active_tasks: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    codebase_structure: Dict[str, Any] = field(default_factory=dict)
    test_results: Dict[str, Any] = field(default_factory=dict)
    deployment_status: str = "NOT_STARTED"
    security_checklist: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class AgentPersonality:
    """Defines agent personality traits"""
    def __init__(self, name: str, role: str, traits: List[str], tendencies: List[str], 
                 communication_style: str):
        self.name = name
        self.role = role
        self.traits = traits  # e.g., ["detail-oriented", "pragmatic"]
        self.tendencies = tendencies  # e.g., ["tends to over-engineer"]
        self.communication_style = communication_style


class Agent:
    """Base class for all team agents"""
    
    def __init__(self, name: str, role: str, personality: AgentPersonality, 
                 model_name: str, message_bus, context_window_size: int = 100000):
        self.name = name
        self.role = role
        self.personality = personality
        self.model_name = model_name
        self.message_bus = message_bus
        self.context_window_size = context_window_size  # Token limit for this agent's AI model
        
        # Agent's independent AI model context (conversation history with their model)
        self.ai_conversation_history: List[Dict[str, Any]] = []  # Each agent's own chat history
        self.context_tokens_used: int = 0  # Track tokens used in this agent's context
        
        # Agent's personal knowledge base (facts, decisions, work)
        self.context: Dict[str, Any] = {}  # Structured knowledge
        self.work_queue: List[str] = []  # Assigned tasks
        self.decisions_log: List[Dict[str, Any]] = []
        self.concerns: List[str] = []
        self.recommendations: List[str] = []
        self.message_history: List[Message] = []  # Messages sent/received
        
        # Information received from other agents (for reference, but not in AI context)
        self.shared_knowledge: Dict[str, Any] = {}  # Information from other agents
        
    def send_message(self, recipient: Optional[str], message_type: MessageType, 
                     content: str, context: Optional[Dict] = None, 
                     requires_response: bool = False):
        """Send a message to another agent or broadcast to all"""
        message = Message(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            context=context or {},
            requires_response=requires_response
        )
        self.message_bus.post(message)
        self.message_history.append(message)
        return message
    
    def receive_message(self, message: Message):
        """Process an incoming message"""
        self.message_history.append(message)
        
        # Store information from other agents in shared_knowledge
        # But don't automatically add to AI context (agent decides what to include)
        if message.sender != self.name:
            self.shared_knowledge[message.id] = {
                "from": message.sender,
                "content": message.content,
                "context": message.context,
                "timestamp": message.timestamp.isoformat()
            }
        
        self.process_message(message)
    
    def process_message(self, message: Message):
        """Override in subclasses to handle specific message types"""
        pass
    
    def think(self, prompt: str, project_state: ProjectState, 
               include_shared_knowledge: bool = False) -> str:
        """
        Process a thought/decision using the agent's AI model.
        Uses THIS AGENT'S independent context window.
        
        Each agent maintains their own conversation history with their AI model,
        building up context independently over time.
        """
        # Build context from THIS AGENT'S conversation history
        context_prompt = self._build_ai_context(prompt, project_state, include_shared_knowledge)
        
        # Estimate tokens (simplified - in production use actual tokenizer)
        estimated_tokens = len(context_prompt.split()) * 1.3  # Rough estimate
        
        # Check if we're within context window
        if self.context_tokens_used + estimated_tokens > self.context_window_size:
            # Trim old conversation history if needed
            self._trim_conversation_history()
        
        # Add to this agent's conversation history
        self.ai_conversation_history.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # In production: Call actual AI model API with this agent's conversation history
        # response = call_ai_model(self.model_name, self.ai_conversation_history)
        # For now, simulate response
        response = self._generate_response(prompt, project_state)
        
        # Add response to conversation history
        self.ai_conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        self.context_tokens_used += int(estimated_tokens)
        
        return response
    
    def _build_ai_context(self, prompt: str, project_state: ProjectState, 
                         include_shared: bool) -> str:
        """Build context prompt from this agent's independent context"""
        context_parts = []
        
        # Add agent's role and personality
        context_parts.append(f"You are {self.name}, a {self.role}.")
        context_parts.append(f"Personality: {self.personality.traits}")
        
        # Add this agent's accumulated knowledge
        if self.context:
            context_parts.append(f"\nYour knowledge: {json.dumps(self.context, indent=2)}")
        
        # Add this agent's conversation history (their independent context)
        if self.ai_conversation_history:
            context_parts.append("\nPrevious conversation:")
            for msg in self.ai_conversation_history[-5:]:  # Last 5 messages
                context_parts.append(f"{msg['role']}: {msg['content']}")
        
        # Optionally include shared knowledge from other agents
        if include_shared and self.shared_knowledge:
            context_parts.append("\nInformation from team:")
            for msg_id, info in list(self.shared_knowledge.items())[-3:]:  # Last 3 shared messages
                context_parts.append(f"{info['from']}: {info['content']}")
        
        # Add current prompt
        context_parts.append(f"\nCurrent question: {prompt}")
        
        return "\n".join(context_parts)
    
    def _trim_conversation_history(self):
        """Trim old conversation history if context window is full"""
        # Keep recent conversation, remove oldest
        if len(self.ai_conversation_history) > 20:
            # Remove oldest 5 messages
            self.ai_conversation_history = self.ai_conversation_history[5:]
            # Recalculate tokens
            self.context_tokens_used = sum(
                len(msg['content'].split()) * 1.3 
                for msg in self.ai_conversation_history
            )
    
    def _generate_response(self, prompt: str, project_state: ProjectState) -> str:
        """Generate a response based on personality and role"""
        # This is a placeholder - in production, call actual AI models
        return f"[{self.name} ({self.role}) thinking about: {prompt}]"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.model_name,
            "context_window": f"{self.context_tokens_used}/{self.context_window_size} tokens",
            "conversation_messages": len(self.ai_conversation_history),
            "work_queue": self.work_queue,
            "concerns": self.concerns,
            "recommendations": self.recommendations,
            "context_keys": list(self.context.keys()),
            "shared_knowledge_count": len(self.shared_knowledge)
        }
    
    def add_to_context(self, key: str, value: Any):
        """Add information to this agent's personal context"""
        self.context[key] = value
    
    def get_context_summary(self) -> str:
        """Get a summary of this agent's independent context"""
        return f"""
Agent: {self.name} ({self.role})
Model: {self.model_name}
Context Window: {self.context_tokens_used}/{self.context_window_size} tokens
Conversation History: {len(self.ai_conversation_history)} messages
Personal Knowledge: {len(self.context)} items
Shared Knowledge (from team): {len(self.shared_knowledge)} messages
"""


class MessageBus:
    """Central message routing system"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_queue: List[Message] = []
        self.message_history: List[Message] = []
        
    def register_agent(self, agent: Agent):
        """Register an agent to receive messages"""
        self.agents[agent.name] = agent
        
    def post(self, message: Message):
        """Post a message to the bus"""
        self.message_queue.append(message)
        self.message_history.append(message)
        self._route_message(message)
    
    def _route_message(self, message: Message):
        """Route message to appropriate recipient(s)"""
        if message.recipient:
            # Send to specific agent
            if message.recipient in self.agents:
                self.agents[message.recipient].receive_message(message)
        else:
            # Broadcast to all agents
            for agent in self.agents.values():
                if agent.name != message.sender:  # Don't send to self
                    agent.receive_message(message)
    
    def process_queue(self):
        """Process all pending messages"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            self._route_message(message)


class Orchestrator(Agent):
    """Alex Morgan - The Orchestrator"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Alex Morgan",
            role="Orchestrator",
            traits=["calm", "methodical", "strategic", "coordinator"],
            tendencies=["always has backup plans", "sees big picture"],
            communication_style="Clear, structured, reassuring"
        )
        super().__init__(
            name="Alex Morgan",
            role="Orchestrator",
            personality=personality,
            model_name="claude-sonnet-4.5",
            message_bus=message_bus
        )
        self.project_state: Optional[ProjectState] = None
        
    def initialize_project(self, project_name: str, description: str):
        """Start a new project"""
        self.project_state = ProjectState(
            project_name=project_name,
            description=description
        )
        self.send_message(
            recipient=None,
            message_type=MessageType.ANNOUNCEMENT,
            content=f"?? New project initialized: {project_name}\n\n{description}\n\nTeam, let's begin!"
        )
        return self.project_state
    
    def process_message(self, message: Message):
        """Handle incoming messages as orchestrator"""
        # Orchestrator coordinates responses and manages project state
        if message.message_type == MessageType.UPDATE:
            self._update_project_state(message)
        elif message.message_type == MessageType.APPROVAL:
            self._handle_approval(message)
    
    def _update_project_state(self, message: Message):
        """Update project state based on agent updates"""
        if self.project_state:
            self.project_state.updated_at = datetime.now()
            # Extract updates from message context
    
    def _handle_approval(self, message: Message):
        """Handle approval requests"""
        pass
    
    def assign_task(self, agent_name: str, task: str):
        """Assign a task to an agent"""
        if agent_name in self.message_bus.agents:
            agent = self.message_bus.agents[agent_name]
            agent.work_queue.append(task)
            self.send_message(
                recipient=agent_name,
                message_type=MessageType.REQUEST,
                content=f"Task assigned: {task}",
                context={"task": task}
            )
    
    def move_to_phase(self, phase: ProjectPhase):
        """Transition project to new phase"""
        if self.project_state:
            self.project_state.current_phase = phase
            self.send_message(
                recipient=None,
                message_type=MessageType.ANNOUNCEMENT,
                content=f"?? Project phase transition: {phase.value}"
            )


class ProductManager(Agent):
    """Lisa Anderson - The Product Manager"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Lisa Anderson",
            role="Product Manager",
            traits=["user-focused", "question-asker", "translator"],
            tendencies=["can scope creep", "asks great clarifying questions"],
            communication_style="Questioning, empathetic, business-focused"
        )
        super().__init__(
            name="Lisa Anderson",
            role="Product Manager",
            personality=personality,
            model_name="gpt-5",
            message_bus=message_bus,
            context_window_size=128000  # GPT-5 context window
        )
        self.requirements: Dict[str, Any] = {}
        self.user_stories: List[str] = []
    
    def process_message(self, message: Message):
        """Handle messages as Product Manager"""
        if "requirements" in message.content.lower() or "what" in message.content.lower():
            # PM should gather requirements
            self.gather_requirements(message.content)
    
    def gather_requirements(self, initial_description: str):
        """Gather requirements from user"""
        questions = [
            "Who will use this application?",
            "What problem does it solve?",
            "What's the MVP vs nice-to-have features?",
            "What's the expected user scale?",
            "Any specific constraints or requirements?"
        ]
        
        self.send_message(
            recipient=None,
            message_type=MessageType.REQUEST,
            content=f"?? Requirements gathering needed. Questions:\n" + "\n".join(f"- {q}" for q in questions)
        )
    
    def create_user_stories(self, requirements: Dict[str, Any]):
        """Create user stories from requirements"""
        self.requirements = requirements
        # Generate user stories based on requirements
        self.send_message(
            recipient="Alex Morgan",
            message_type=MessageType.UPDATE,
            content="? User stories created based on requirements",
            context={"user_stories": self.user_stories}
        )


class Architect(Agent):
    """Sarah Chen - The Architect"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Sarah Chen",
            role="Architect",
            traits=["visionary", "pragmatic", "elegant-solutions"],
            tendencies=["can over-engineer", "loves good architecture"],
            communication_style="Technical but clear, enthusiastic about design"
        )
        super().__init__(
            name="Sarah Chen",
            role="Architect",
            personality=personality,
            model_name="gpt-5",
            message_bus=message_bus
        )
        self.architecture_design: Dict[str, Any] = {}
        self.tech_stack: List[str] = []
    
    def process_message(self, message: Message):
        """Handle messages as Architect"""
        if "architecture" in message.content.lower() or "design" in message.content.lower():
            self.design_architecture(message.context)
    
    def design_architecture(self, requirements: Dict[str, Any]):
        """Design system architecture"""
        # Analyze requirements and propose architecture
        self.send_message(
            recipient="Marcus Rodriguez",
            message_type=MessageType.REQUEST,
            content="??? Architecture design ready. Can you review the technical approach?",
            context={"architecture": self.architecture_design}
        )


class Developer(Agent):
    """Marcus Rodriguez - The Developer"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Marcus Rodriguez",
            role="Developer",
            traits=["practical", "code-quality-obsessed", "pragmatic"],
            tendencies=["can get lost in optimization", "prefers working code"],
            communication_style="Direct, technical, solution-focused"
        )
        super().__init__(
            name="Marcus Rodriguez",
            role="Developer",
            personality=personality,
            model_name="claude-codex",
            message_bus=message_bus,
            context_window_size=200000  # Claude Codex has large context
        )
    
    def process_message(self, message: Message):
        """Handle messages as Developer"""
        if "implement" in message.content.lower() or "code" in message.content.lower():
            self.implement_feature(message.context)
    
    def implement_feature(self, spec: Dict[str, Any]):
        """Implement a feature"""
        self.send_message(
            recipient="Priya Patel",
            message_type=MessageType.UPDATE,
            content="? Feature implementation complete. Ready for testing.",
            context={"feature": spec}
        )


class QAEngineer(Agent):
    """Priya Patel - The QA Engineer"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Priya Patel",
            role="QA Engineer",
            traits=["detail-oriented", "skeptical", "constructive"],
            tendencies=["can be overly cautious", "finds bugs others miss"],
            communication_style="Methodical, thorough, evidence-based"
        )
        super().__init__(
            name="Priya Patel",
            role="QA Engineer",
            personality=personality,
            model_name="gemini-pro-2.5",
            message_bus=message_bus,
            context_window_size=1000000  # Gemini Pro 2.5 has very large context
        )
        self.test_cases: List[Dict[str, Any]] = []
        self.bug_reports: List[Dict[str, Any]] = []
    
    def process_message(self, message: Message):
        """Handle messages as QA Engineer"""
        if "test" in message.content.lower() or "bug" in message.content.lower():
            self.create_test_plan(message.context)
    
    def create_test_plan(self, feature_spec: Dict[str, Any]):
        """Create test plan for a feature"""
        self.send_message(
            recipient="Marcus Rodriguez",
            message_type=MessageType.UPDATE,
            content="? Test plan created. Found 2 edge cases to handle.",
            context={"test_cases": self.test_cases}
        )


class DevOpsEngineer(Agent):
    """Jordan Kim - The DevOps Engineer"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Jordan Kim",
            role="DevOps Engineer",
            traits=["automation-enthusiast", "pragmatic", "fast"],
            tendencies=["can automate too much", "gets things running"],
            communication_style="Practical, tool-focused, action-oriented"
        )
        super().__init__(
            name="Jordan Kim",
            role="DevOps Engineer",
            personality=personality,
            model_name="gpt-5",
            message_bus=message_bus
        )
    
    def process_message(self, message: Message):
        """Handle messages as DevOps Engineer"""
        if "deploy" in message.content.lower() or "infrastructure" in message.content.lower():
            self.setup_deployment(message.context)
    
    def setup_deployment(self, project_spec: Dict[str, Any]):
        """Set up deployment pipeline"""
        self.send_message(
            recipient="Mike Torres",
            message_type=MessageType.APPROVAL,
            content="?? Deployment pipeline ready. Security review needed.",
            context={"pipeline": project_spec}
        )


class SecuritySpecialist(Agent):
    """Mike Torres - The Security Specialist"""
    
    def __init__(self, message_bus):
        personality = AgentPersonality(
            name="Mike Torres",
            role="Security Specialist",
            traits=["security-first", "risk-aware", "clear-explainer"],
            tendencies=["can be overly cautious", "explains risks well"],
            communication_style="Security-focused, clear about risks, non-alarmist"
        )
        super().__init__(
            name="Mike Torres",
            role="Security Specialist",
            personality=personality,
            model_name="claude-sonnet-4.5",
            message_bus=message_bus,
            context_window_size=200000  # Claude Sonnet 4.5 has large context
        )
        self.security_checklist: List[str] = []
        self.vulnerabilities: List[str] = []
    
    def process_message(self, message: Message):
        """Handle messages as Security Specialist"""
        if "security" in message.content.lower() or "approval" in message.content.lower():
            self.review_security(message.context)
    
    def review_security(self, component: Dict[str, Any]):
        """Review component for security issues"""
        self.send_message(
            recipient=None,
            message_type=MessageType.ANNOUNCEMENT,
            content="? Security review complete. 3 recommendations: [list]",
            context={"security_checklist": self.security_checklist}
        )


class DestinyTeam:
    """Main team coordinator"""
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.orchestrator = Orchestrator(self.message_bus)
        self.product_manager = ProductManager(self.message_bus)
        self.architect = Architect(self.message_bus)
        self.developer = Developer(self.message_bus)
        self.qa_engineer = QAEngineer(self.message_bus)
        self.devops_engineer = DevOpsEngineer(self.message_bus)
        self.security_specialist = SecuritySpecialist(self.message_bus)
        
        # Register all agents
        self.message_bus.register_agent(self.orchestrator)
        self.message_bus.register_agent(self.product_manager)
        self.message_bus.register_agent(self.architect)
        self.message_bus.register_agent(self.developer)
        self.message_bus.register_agent(self.qa_engineer)
        self.message_bus.register_agent(self.devops_engineer)
        self.message_bus.register_agent(self.security_specialist)
    
    def start_project(self, project_name: str, description: str):
        """Start a new project"""
        project_state = self.orchestrator.initialize_project(project_name, description)
        self.message_bus.process_queue()
        return project_state
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get status of all team members"""
        return {
            agent.name: agent.get_status()
            for agent in self.message_bus.agents.values()
        }
    
    def get_project_state(self) -> Optional[ProjectState]:
        """Get current project state"""
        return self.orchestrator.project_state


if __name__ == "__main__":
    # Example usage
    team = DestinyTeam()
    
    print("?? The Destiny Development Team")
    print("=" * 50)
    
    project_state = team.start_project(
        "Social Media App",
        "A platform for users to share posts and connect"
    )
    
    print(f"\n?? Project: {project_state.project_name}")
    print(f"Phase: {project_state.current_phase.value}")
    
    print("\n?? Team Status:")
    for name, status in team.get_team_status().items():
        print(f"  {name} ({status['role']}) - {len(status['work_queue'])} tasks")
