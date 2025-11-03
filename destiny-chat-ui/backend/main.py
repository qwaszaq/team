"""
Destiny Chat UI - Backend API
FastAPI server with WebSocket support for real-time chat

Author: Tomasz Zieliński (Senior Developer)
Orchestrated by: Aleksander Nowak
Date: 2025-11-03
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os
import json

# Add parent directory to path to import agents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.specialized.aleksander_agent import AleksanderAgent
from agents.specialized.tomasz_agent import TomaszAgent
from agents.specialized.anna_agent import AnnaAgent
from agents.specialized.joanna_agent import JoannaAgent
from agents.specialized.magdalena_agent import MagdalenaAgent
from agents.specialized.katarzyna_agent import KatarzynaAgent
from agents.specialized.piotr_agent import PiotrAgent
from agents.specialized.michal_agent import MichalAgent
from agents.specialized.dr_joanna_agent import DrJoannaAgent

# Import LM Studio chat client
from lmstudio_chat import LMStudioChat

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ID = "destiny-chat-ui"  # Separate from main project!

# Initialize LM Studio chat client
lm_chat = LMStudioChat()

# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="Destiny Chat UI API",
    description="Backend API for Destiny Team chat interface",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Data Models
# ============================================================================

class ChatMessage(BaseModel):
    """Chat message model"""
    content: str
    to_agent: str = "@All"  # @Aleksander, @Tomasz, @All, etc.
    from_user: str = "User"

class AgentStatus(BaseModel):
    """Agent status model"""
    name: str
    role: str
    status: str  # available, busy, offline
    specialization: str

class ChatResponse(BaseModel):
    """Response from agent"""
    agent: str
    content: str
    timestamp: str
    type: str = "message"  # message, status, error

# ============================================================================
# Agent Management
# ============================================================================

class AgentManager:
    """Manages all 9 Destiny Team agents"""
    
    def __init__(self):
        print(f"🚀 Initializing Destiny Team agents for project: {PROJECT_ID}")
        self.project_id = PROJECT_ID
        self.agents = {}
        self._init_agents()
        
    def _init_agents(self):
        """Initialize all 9 agents"""
        try:
            self.agents = {
                "Aleksander Nowak": AleksanderAgent(self.project_id),
                "Tomasz Zieliński": TomaszAgent(self.project_id),
                "Anna Nowakowska": AnnaAgent(self.project_id),
                "Joanna Mazur": JoannaAgent(self.project_id),
                "Magdalena Kowalska": MagdalenaAgent(self.project_id),
                "Katarzyna Wiśniewska": KatarzynaAgent(self.project_id),
                "Piotr Szymański": PiotrAgent(self.project_id),
                "Michał Dąbrowski": MichalAgent(self.project_id),
                "Dr. Joanna Wójcik": DrJoannaAgent(self.project_id),
            }
            print(f"✅ Initialized {len(self.agents)} agents")
        except Exception as e:
            print(f"❌ Error initializing agents: {e}")
            # Continue with empty agents dict
            self.agents = {}
    
    def get_agent(self, name: str):
        """Get agent by name"""
        return self.agents.get(name)
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents status"""
        return [
            {
                "name": agent.name,
                "role": agent.role,
                "status": agent.status.value if hasattr(agent, 'status') else "available",
                "specialization": agent.specialization
            }
            for agent in self.agents.values()
        ]
    
    def send_message(self, message: str, to_agent: str) -> str:
        """Send message to agent and get REAL AI response"""
        
        # Parse @mention
        agent_name = to_agent.replace("@", "").strip()
        
        # If @All, send to Aleksander (orchestrator)
        if agent_name.lower() == "all":
            agent_name = "Aleksander Nowak"
        
        agent = self.get_agent(agent_name)
        if not agent:
            return f"❌ Agent '{agent_name}' not found"
        
        # Generate REAL AI response using LM Studio
        try:
            messages = lm_chat.create_agent_prompt(
                agent_name=agent.name,
                agent_role=agent.role,
                specialization=agent.specialization,
                user_message=message
            )
            
            ai_response = lm_chat.chat(
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            # Format response
            response = f"""👋 **{agent.name}** ({agent.role})

{ai_response}

---
💡 _Możesz zadać kolejne pytanie lub wybrać innego agenta z listy._"""
            
            return response
            
        except Exception as e:
            # Fallback to mock if LM Studio fails
            print(f"Error with LM Studio: {e}")
            return self._generate_mock_response(agent, message)
    
    def _generate_mock_response(self, agent, message: str) -> str:
        """Generate agent-specific response (POC version)"""
        
        msg_lower = message.lower()
        
        # Aleksander (Orchestrator)
        if agent.role == "Orchestrator":
            return """Rozumiem Twoją prośbę. Koordynuję pracę zespołu:
- Analizuję wymagania
- Deleguję zadania do właściwych agentów
- Monitoruję postęp

Czy mogę przekazać to zadanie konkretnym specjalistom?"""
        
        # Tomasz (Developer)
        elif agent.role == "Senior Developer":
            if "build" in msg_lower or "implement" in msg_lower:
                return """Jako developer, mogę pomóc w implementacji:
- Kod backend (Python/FastAPI)
- Frontend (React/TypeScript)
- Integracje z bazami danych
- API endpoints

Potrzebuję więcej szczegółów o tym, co chcesz zbudować."""
            else:
                return "Jestem gotowy do implementacji. Powiedz mi więcej o technical requirements."
        
        # Anna (QA)
        elif agent.role == "QA Engineer":
            return """Jako QA Engineer, mogę pomóc w:
- Testowaniu aplikacji
- Tworzeniu test cases
- Automatyzacji testów
- Quality assurance

Czy mam przetestować coś konkretnego?"""
        
        # Joanna (UX Designer)
        elif agent.role == "UX/UI Designer":
            return """Jako UX Designer, mogę zaprojektować:
- Interfejs użytkownika
- User flow
- Wireframes i mockups
- Design system

Jaka jest Twoja wizja UI?"""
        
        # Magdalena (Product Manager)
        elif agent.role == "Product Manager":
            return """Jako Product Manager, mogę pomóc:
- Zdefiniować requirements
- Ustalić priorytety
- Stworzyć roadmap
- Zarządzać backlogi

Co chcesz osiągnąć z tym produktem?"""
        
        # Default
        else:
            return f"Jako {agent.role}, jestem gotowy pomóc. Powiedz mi więcej o Twoich potrzebach."

# Initialize agent manager
agent_manager = AgentManager()

# ============================================================================
# WebSocket Connection Manager
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting: {e}")

manager = ConnectionManager()

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Destiny Chat UI API",
        "status": "operational",
        "version": "0.1.0",
        "project_id": PROJECT_ID,
        "agents": len(agent_manager.agents)
    }

@app.get("/agents", response_model=List[AgentStatus])
async def get_agents():
    """Get all agents status"""
    agents = agent_manager.get_all_agents()
    return agents

@app.post("/chat/send")
async def send_message(message: ChatMessage):
    """Send message to agent"""
    try:
        response_text = agent_manager.send_message(
            message.content,
            message.to_agent
        )
        
        response = ChatResponse(
            agent=message.to_agent,
            content=response_text,
            timestamp=datetime.now().isoformat(),
            type="message"
        )
        
        # Broadcast to WebSocket clients
        await manager.broadcast({
            "type": "message",
            "data": response.dict()
        })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            if message_data.get("type") == "chat":
                content = message_data.get("content")
                to_agent = message_data.get("to_agent", "@All")
                
                # Get response from agent
                response_text = agent_manager.send_message(content, to_agent)
                
                # Send response back
                response = {
                    "type": "message",
                    "data": {
                        "agent": to_agent,
                        "content": response_text,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                await manager.broadcast(response)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("="*80)
    print("🚀 Starting Destiny Chat UI Backend")
    print("="*80)
    print(f"Project ID: {PROJECT_ID}")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"Health: http://localhost:8000/")
    print("="*80)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
