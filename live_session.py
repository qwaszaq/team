"""
Live Interactive Team Session - Real-time communication
Artur communicates with the Destiny Development Team through Alex (Orchestrator)
"""

from destiny_team import DestinyTeam, MessageType, ProjectPhase
from typing import Dict, List
import json


class LiveTeamSession:
    """Live session where user interacts with team through orchestrator"""
    
    def __init__(self):
        self.team = DestinyTeam()
        self.project_state = None
        self.conversation_log: List[Dict] = []
        
    def start_session(self):
        """Initialize a new project session"""
        print("\n" + "=" * 70)
        print("🎯 ALEX MORGAN (Orchestrator)")
        print("=" * 70)
        print("\n   'Hello Artur! I'm Alex Morgan, your Orchestrator.'")
        print("   'I'll coordinate our team of experts to help you build your project.'")
        print("\n   'Our team is ready:'")
        print("   • 👩 Lisa Anderson - Product Manager")
        print("   • 🏗️ Sarah Chen - Architect")
        print("   • 💻 Marcus Rodriguez - Developer")
        print("   • 🔬 Priya Patel - QA Engineer")
        print("   • ⚙️ Jordan Kim - DevOps Engineer")
        print("   • 🔒 Mike Torres - Security Specialist")
        print("\n   'What would you like to build? Describe your project idea.'")
        print("\n" + "=" * 70 + "\n")
        
    def process_user_message(self, user_message: str) -> str:
        """Process user message and coordinate team response"""
        if not user_message.strip():
            return ""
        
        # Log conversation
        self.conversation_log.append({"user": user_message, "timestamp": "now"})
        
        message_lower = user_message.lower()
        
        # Check if it's a project description
        if any(word in message_lower for word in ['build', 'create', 'make', 'want', 'need', 'project']) and not self.project_state:
            return self._initialize_project(user_message)
        
        # Route to appropriate team member based on content
        if any(word in message_lower for word in ['user', 'who', 'what', 'problem', 'feature', 'requirements']):
            return self._route_to_product_manager(user_message)
        
        elif any(word in message_lower for word in ['architecture', 'tech', 'stack', 'database', 'framework', 'design']):
            return self._route_to_architect(user_message)
        
        elif any(word in message_lower for word in ['code', 'implement', 'build', 'create', 'write', 'develop']):
            return self._route_to_developer(user_message)
        
        elif any(word in message_lower for word in ['test', 'bug', 'quality', 'check', 'qa']):
            return self._route_to_qa(user_message)
        
        elif any(word in message_lower for word in ['deploy', 'host', 'server', 'infrastructure', 'devops']):
            return self._route_to_devops(user_message)
        
        elif any(word in message_lower for word in ['security', 'safe', 'secure', 'protection']):
            return self._route_to_security(user_message)
        
        elif any(word in message_lower for word in ['status', 'progress', 'phase', 'where']):
            return self._get_project_status()
        
        elif any(word in message_lower for word in ['team', 'members', 'who']):
            return self._show_team_status()
        
        else:
            return self._general_response(user_message)
    
    def _initialize_project(self, message: str) -> str:
        """Initialize a new project"""
        project_name = self._extract_project_name(message)
        self.project_state = self.team.start_project(project_name, message)
        self.team.message_bus.process_queue()
        
        response = f"""
✅ PROJECT INITIALIZED: '{project_name}'

🎯 ALEX MORGAN (Orchestrator):
   'Excellent! I've initialized the project. Let me coordinate with the team...'

👩 LISA ANDERSON (Product Manager):
   'Great idea! I have some questions to make sure we build exactly what you need:'
   
   • Who will use this application?
   • What problem does it solve?
   • What are the key features you envision?
   • What's your expected user scale?
   
   'The more details you share, the better we can design it!'

📊 Project Phase: {self.project_state.current_phase.value}
"""
        return response
    
    def _route_to_product_manager(self, message: str) -> str:
        """Route message to Product Manager"""
        # Build Lisa's context
        if not self.team.product_manager.context.get('user_info'):
            self.team.product_manager.add_to_context('user_info', {})
        
        # Lisa thinks about this (builds her independent context)
        lisa_response = self.team.product_manager.think(
            f"User said: {message}. What should I ask next?",
            self.project_state if self.project_state else ProjectState()
        )
        
        response = f"""
👩 LISA ANDERSON (Product Manager):
   'Thanks for that information! Let me update our requirements...'
   
   {message}
   
   'I'm noting this down. A few more questions:'
   • Can you tell me more about the primary use case?
   • Are there any specific constraints or preferences?
   • What's the timeline for this project?

🎯 ALEX MORGAN (Orchestrator):
   'Lisa is gathering requirements. Once we have enough info, I'll have Sarah
   start thinking about the architecture.'

📊 Lisa's Context: {len(self.team.product_manager.ai_conversation_history)} conversation messages
   Shared Knowledge: {len(self.team.product_manager.shared_knowledge)} messages from team
"""
        return response
    
    def _route_to_architect(self, message: str) -> str:
        """Route message to Architect"""
        # Sarah thinks about architecture (builds her independent context)
        sarah_response = self.team.architect.think(
            f"User asked about: {message}. What architecture should I recommend?",
            self.project_state if self.project_state else ProjectState()
        )
        
        response = f"""
🏗️ SARAH CHEN (Architect):
   'Excellent question about architecture! Let me think about this...'
   
   {message}
   
   'Based on what I know so far, I'm considering:'
   • Modern web framework (React/Next.js for frontend)
   • Robust backend (Node.js or Python)
   • Scalable database (PostgreSQL for relational data)
   • Cloud hosting (AWS/Vercel for deployment)
   
   'However, I'd like to know more about:'
   • Expected user scale?
   • Performance requirements?
   • Budget constraints?

💻 MARCUS RODRIGUEZ (Developer):
   'Sarah, I agree with React + Node. That's a solid stack for most projects.
   Let me know when you finalize the architecture and I'll start implementing.'

📊 Sarah's Context: {len(self.team.architect.ai_conversation_history)} conversation messages
   Marcus's Context: {len(self.team.developer.ai_conversation_history)} conversation messages
"""
        return response
    
    def _route_to_developer(self, message: str) -> str:
        """Route message to Developer"""
        marcus_response = self.team.developer.think(
            f"User asked: {message}. How should I approach implementation?",
            self.project_state if self.project_state else ProjectState()
        )
        
        response = f"""
💻 MARCUS RODRIGUEZ (Developer):
   'Got it! I'm ready to start coding. Let me break down what needs to be done:'
   
   {message}
   
   'I'll focus on:'
   • Clean, maintainable code structure
   • Proper error handling
   • Following best practices
   • Code that's easy to test

🔬 PRIYA PATEL (QA Engineer):
   'Marcus, I'll prepare test cases as you develop. Let me know when features
   are ready and I'll test them thoroughly.'

📊 Marcus's Context: {len(self.team.developer.ai_conversation_history)} conversation messages
   Priya's Context: {len(self.team.qa_engineer.ai_conversation_history)} conversation messages
"""
        return response
    
    def _route_to_qa(self, message: str) -> str:
        """Route message to QA Engineer"""
        priya_response = self.team.qa_engineer.think(
            f"User asked: {message}. What should I test?",
            self.project_state if self.project_state else ProjectState()
        )
        
        response = f"""
🔬 PRIYA PATEL (QA Engineer):
   'Testing is crucial! I'll create comprehensive test coverage:'
   
   {message}
   
   'My test plan includes:'
   • Unit tests for individual components
   • Integration tests for workflows
   • Edge case testing
   • Performance testing
   • Security testing

💻 MARCUS RODRIGUEZ (Developer):
   'Thanks Priya! I'll make sure the code is testable from the start.'

📊 Priya's Context: {len(self.team.qa_engineer.ai_conversation_history)} conversation messages
"""
        return response
    
    def _route_to_devops(self, message: str) -> str:
        """Route message to DevOps Engineer"""
        response = f"""
⚙️ JORDAN KIM (DevOps Engineer):
   'Deployment is my specialty! Here's what I'll set up:'
   
   {message}
   
   'I'll configure:'
   • Docker containers for consistent environments
   • CI/CD pipeline (automated testing and deployment)
   • Cloud hosting setup
   • Monitoring and logging
   • Automated backups

🔒 MIKE TORRES (Security Specialist):
   'Jordan, I'll review the deployment configuration for security before
   we go live. Security is critical!'

📊 Jordan's Context: {len(self.team.devops_engineer.ai_conversation_history)} conversation messages
"""
        return response
    
    def _route_to_security(self, message: str) -> str:
        """Route message to Security Specialist"""
        response = f"""
🔒 MIKE TORRES (Security Specialist):
   'Security is paramount! I'll ensure we have:'
   
   {message}
   
   'Security checklist:'
   • Secure authentication (JWT, OAuth)
   • Input validation and sanitization
   • SQL injection prevention
   • XSS protection
   • Rate limiting
   • HTTPS in production
   • Regular security audits

🎯 ALEX MORGAN (Orchestrator):
   'Mike's security review is essential. We'll make sure everything is secure
   before deployment.'

📊 Mike's Context: {len(self.team.security_specialist.ai_conversation_history)} conversation messages
"""
        return response
    
    def _get_project_status(self) -> str:
        """Get current project status"""
        if not self.project_state:
            return "\n⚠️ No active project. Start by describing what you want to build.\n"
        
        status = self.team.get_team_status()
        
        response = f"""
📊 PROJECT STATUS
{'=' * 70}

Project: {self.project_state.project_name}
Phase: {self.project_state.current_phase.value}
Description: {self.project_state.description[:100]}...

Team Status:
"""
        for name, info in status.items():
            response += f"""
  {name} ({info['role']})
    Context Window: {info['context_window']}
    Conversation Messages: {info['conversation_messages']}
    Tasks: {len(info['work_queue'])}
    Shared Knowledge: {info['shared_knowledge_count']} messages
"""
        return response
    
    def _show_team_status(self) -> str:
        """Show team member status"""
        status = self.team.get_team_status()
        response = "\n👥 TEAM STATUS\n" + "=" * 70 + "\n"
        for name, info in status.items():
            response += f"""
{name} ({info['role']})
  Model: {info['model']}
  Context: {info['context_window']}
  Conversations: {info['conversation_messages']} messages
  Shared Knowledge: {info['shared_knowledge_count']} messages from team
"""
        return response
    
    def _general_response(self, message: str) -> str:
        """General team response"""
        response = f"""
🎯 ALEX MORGAN (Orchestrator):
   'Got it, Artur! Let me coordinate with the team...'

👩 LISA ANDERSON (Product Manager):
   'That's helpful context! I'm updating our requirements.'

🏗️ SARAH CHEN (Architect):
   'I'll factor that into the architecture design.'

💻 MARCUS RODRIGUEZ (Developer):
   'Noted. I'll keep that in mind during implementation.'

📊 Independent Contexts Being Built:
"""
        for name, agent in self.team.message_bus.agents.items():
            response += f"   • {name}: {len(agent.ai_conversation_history)} conversation messages\n"
        
        return response
    
    def _extract_project_name(self, message: str) -> str:
        """Extract project name from message"""
        words = message.split()
        if len(words) > 1:
            return " ".join(words[:3])[:50]
        return "My Project"


if __name__ == "__main__":
    session = LiveTeamSession()
    session.start_session()
    
    print("Type your messages (or 'exit' to quit):\n")
    
    while True:
        user_input = input("👤 Artur: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n🎯 ALEX MORGAN (Orchestrator):")
            print("   'Thanks for working with us, Artur! The team is here whenever you need us.'")
            print("   'Goodbye! 👋'\n")
            break
        
        if not user_input:
            continue
        
        response = session.process_user_message(user_input)
        print(response)
