# 💬 DESTINY CHAT UI - Hybrid System Integration
## Browser Interface dla On-Prem Intelligence System

**Date:** 2025-11-04  
**Status:** Concept (To Be Implemented Later)  
**Priority:** High (User Requested)  
**Reminder:** Artur poprosił o przypomnienie tego zadania  

---

## 🎯 KONCEPCJA

**Pomysł Artura:**
> "Wykorzystać destiny-chat-ui jako interfejs do hybrydowego systemu - podpiąć lokalny LLM, 
> Aleksander widziałby wszystko przez logi LMStudio"

**Dlaczego to ŚWIETNY pomysł:**

1. ✅ **User-Friendly Interface** - Przeglądarkowy chat zamiast command line
2. ✅ **Visual Progress** - Real-time widzisz co robi local LLM
3. ✅ **Supervision Built-In** - Aleksander ma dostęp do logów
4. ✅ **Existing Codebase** - destiny-chat-ui już istnieje (TSX/React)
5. ✅ **LMStudio Compatible** - OpenAI-compatible API, łatwa integracja

---

## 🏗️ ARCHITEKTURA

### **Current destiny-chat-ui Structure:**

```
destiny-chat-ui/
├── src/
│   ├── components/
│   │   ├── Chat.tsx           # Main chat interface
│   │   ├── MessageList.tsx    # Message display
│   │   └── InputBar.tsx       # User input
│   ├── lib/
│   │   └── api.ts             # API calls (currently to cloud?)
│   └── App.tsx
├── package.json
└── tsconfig.json
```

### **Proposed Integration:**

```
┌─────────────────────────────────────────────────────────────┐
│  BROWSER (User Interface)                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  destiny-chat-ui (React/TSX)                         │  │
│  │                                                       │  │
│  │  [Chat Interface]                                    │  │
│  │  User: "Zbadaj Telusa i CPK"                        │  │
│  │  Bot: "✓ Rozpoczynam investigation..."              │  │
│  │  Bot: "🔧 Scraping wyborcza.pl..."                  │  │
│  │  Bot: "📊 Analyzing price data..."                  │  │
│  │  Bot: "✅ Found 12 sources, archived"               │  │
│  │                                                       │  │
│  │  [Progress Bar] ████████░░ 80%                       │  │
│  │  [Sources Counter] 12/15                            │  │
│  │  [Quality Indicator] Grade: B                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│  BACKEND (Investigation Orchestrator)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  local_orchestrator.py (Enhanced with WebSocket)     │  │
│  │                                                       │  │
│  │  Receives: "Zbadaj Telusa"                          │  │
│  │  ↓                                                    │  │
│  │  Creates: investigation task                         │  │
│  │  ↓                                                    │  │
│  │  Streams progress to UI:                            │  │
│  │    • Tool calls                                      │  │
│  │    • Sources found                                   │  │
│  │    • Analysis status                                 │  │
│  │    • Quality metrics                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    ↕ OpenAI-compatible API
┌─────────────────────────────────────────────────────────────┐
│  LOCAL LLM (LMStudio)                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  gpt-oss-20b (44k context)                          │  │
│  │  Endpoint: http://localhost:1234/v1                 │  │
│  │                                                       │  │
│  │  Logs → logs/lmstudio/                              │  │
│  │         (Aleksander reads these)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    ↕ Direct access
┌─────────────────────────────────────────────────────────────┐
│  SUPERVISOR (Aleksander - Cursor)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Reads:                                              │  │
│  │    • logs/lmstudio/ (what LLM did)                  │  │
│  │    • logs/investigations/ (tool usage)              │  │
│  │    • shared_workspace/results/ (output)             │  │
│  │                                                       │  │
│  │  Provides:                                           │  │
│  │    • Quality reports                                 │  │
│  │    • Guidance for improvements                       │  │
│  │    • Final synthesis                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 TECHNICAL IMPLEMENTATION

### **Phase 1: Connect destiny-chat-ui to LMStudio**

**Update `src/lib/api.ts`:**

```typescript
// Current (example - probably cloud API)
const API_ENDPOINT = "https://api.openai.com/v1/chat/completions";

// New: Local LMStudio
const API_ENDPOINT = "http://localhost:1234/v1/chat/completions";

export async function sendMessage(
  messages: Message[],
  tools?: Tool[]
): Promise<Response> {
  const response = await fetch(API_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-oss-20b",
      messages: messages,
      tools: tools,           // Function calling
      stream: true,           // Streaming for real-time updates
      temperature: 0.7,
      max_tokens: 2048
    })
  });
  
  return response;
}
```

### **Phase 2: Add Investigation Mode**

**New Component: `src/components/InvestigationPanel.tsx`:**

```typescript
interface InvestigationState {
  id: string;
  status: "planning" | "active" | "review" | "complete";
  sourcesCollected: number;
  sourcesRequired: number;
  qualityGrade: string;
  currentAction: string;
}

export const InvestigationPanel: React.FC = () => {
  const [investigation, setInvestigation] = useState<InvestigationState | null>(null);
  
  // Subscribe to investigation updates via WebSocket
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080/investigations");
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setInvestigation(update);
    };
    
    return () => ws.close();
  }, []);
  
  if (!investigation) return null;
  
  return (
    <div className="investigation-panel">
      <h3>Investigation: {investigation.id}</h3>
      
      {/* Status Badge */}
      <Badge status={investigation.status}>
        {investigation.status.toUpperCase()}
      </Badge>
      
      {/* Progress Bar */}
      <ProgressBar 
        current={investigation.sourcesCollected}
        total={investigation.sourcesRequired}
      />
      
      {/* Quality Indicator */}
      <div className="quality">
        Grade: <span className={`grade-${investigation.qualityGrade}`}>
          {investigation.qualityGrade}
        </span>
      </div>
      
      {/* Current Action */}
      <div className="current-action">
        🔧 {investigation.currentAction}
      </div>
      
      {/* Supervisor Status */}
      {investigation.status === "review" && (
        <div className="supervisor-review">
          👔 Aleksander reviewing quality...
        </div>
      )}
    </div>
  );
};
```

### **Phase 3: Real-Time Updates via WebSocket**

**Backend Enhancement: `local_orchestrator.py`:**

```python
import asyncio
import websockets
import json

class LocalLLMOrchestrator:
    def __init__(self, ...):
        # ... existing code ...
        self.websocket_clients = set()
    
    async def broadcast_update(self, update: dict):
        """
        Broadcast investigation update to all connected clients
        """
        if self.websocket_clients:
            message = json.dumps(update)
            await asyncio.gather(
                *[client.send(message) for client in self.websocket_clients]
            )
    
    async def handle_websocket(self, websocket, path):
        """
        Handle WebSocket connections from destiny-chat-ui
        """
        self.websocket_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.websocket_clients.remove(websocket)
    
    def run_investigation(self, task: str, ...):
        # ... existing code ...
        
        # After each significant action, broadcast update
        await self.broadcast_update({
            "investigation_id": investigation_id,
            "status": "active",
            "sourcesCollected": len(sources),
            "sourcesRequired": min_sources,
            "currentAction": f"Scraping {url}...",
            "qualityGrade": "B"
        })


# Start WebSocket server
async def start_websocket_server():
    orchestrator = LocalLLMOrchestrator()
    
    async with websockets.serve(
        orchestrator.handle_websocket,
        "localhost",
        8080
    ):
        await asyncio.Future()  # Run forever

# Run both HTTP (for LLM) and WebSocket (for UI)
asyncio.run(start_websocket_server())
```

### **Phase 4: Supervisor Visibility Dashboard**

**New Page: `src/pages/SupervisorDashboard.tsx`:**

```typescript
interface LogEntry {
  timestamp: string;
  type: "llm_call" | "tool_execution" | "tool_error";
  details: any;
}

export const SupervisorDashboard: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  
  // Poll logs (or use WebSocket)
  useEffect(() => {
    const interval = setInterval(async () => {
      // Read LMStudio logs
      const response = await fetch("/api/logs/lmstudio/latest");
      const newLogs = await response.json();
      setLogs(prev => [...prev, ...newLogs]);
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="supervisor-dashboard">
      <h1>👔 Aleksander's Supervision Dashboard</h1>
      
      {/* Active Investigations */}
      <section className="active-investigations">
        <h2>Active Investigations</h2>
        {investigations.map(inv => (
          <InvestigationCard key={inv.id} investigation={inv} />
        ))}
      </section>
      
      {/* Live Log Stream */}
      <section className="log-stream">
        <h2>🔍 Live LMStudio Logs</h2>
        <div className="log-container">
          {logs.map((log, i) => (
            <LogEntry key={i} log={log} />
          ))}
        </div>
      </section>
      
      {/* Quality Metrics */}
      <section className="quality-metrics">
        <h2>📊 Quality Metrics</h2>
        <MetricsGrid investigations={investigations} />
      </section>
      
      {/* Pending Reviews */}
      <section className="pending-reviews">
        <h2>⏳ Pending Supervisor Review</h2>
        <ReviewQueue />
      </section>
    </div>
  );
};
```

---

## 🎨 UI/UX FEATURES

### **Investigation Chat Mode**

```
┌─────────────────────────────────────────────────────┐
│  Destiny Intelligence System                        │
│  [Normal Chat] [Investigation Mode] ← Toggle        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  User: "Zbadaj transakcję ziemi Telusa związaną    │
│         z CPK"                                       │
│                                                      │
│  Assistant: 🔍 Investigation started               │
│             ID: telus_cpk_001                       │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ Status: Active                             │    │
│  │ Sources: 8/15 ████████░░░░░░░ 53%        │    │
│  │ Grade: B (needs improvement)              │    │
│  │                                            │    │
│  │ 🔧 Currently: Scraping onet.pl...        │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Assistant: ✅ Archived source #8                  │
│             https://onet.pl/article/telus           │
│             Credibility: HIGH                       │
│                                                      │
│  Assistant: 📊 Statistical analysis complete       │
│             Property price: 87,000 PLN/ha          │
│             Market average: 51,500 PLN/ha          │
│             Z-score: 2.96 (outlier!)               │
│                                                      │
│  👔 Aleksander: Reviewing quality...               │
│                                                      │
│  👔 Aleksander: ⚠️ Need 7 more sources            │
│                 Guidance provided                   │
│                                                      │
│  Assistant: 🔄 Continuing investigation...         │
│                                                      │
│  [User input box]                                   │
└─────────────────────────────────────────────────────┘
```

### **Supervisor View (Aleksander's Dashboard)**

```
┌─────────────────────────────────────────────────────┐
│  👔 Aleksander's Supervision Dashboard              │
├─────────────────────────────────────────────────────┤
│                                                      │
│  🔥 Active Investigations (2)                       │
│  ┌────────────────────────────────────────────┐    │
│  │ telus_cpk_001          Grade: B  [Review] │    │
│  │ cpk_research_002       Grade: A  [Done]   │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  🔍 Live LMStudio Logs                             │
│  ┌────────────────────────────────────────────┐    │
│  │ 16:45:23 LLM Call: investigation task      │    │
│  │ 16:45:25 Tool: scrape_webpage              │    │
│  │ 16:45:27 Tool: archive_source ✓            │    │
│  │ 16:45:29 Tool: calculate_statistics        │    │
│  │ 16:45:30 LLM Response: 245 tokens          │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  📊 Quality Metrics                                 │
│  ┌──────────────┬──────────────┬──────────────┐    │
│  │ Tool Usage   │ A (excellent)│ ✅           │    │
│  │ Source Qual. │ A+ (100%)    │ ✅           │    │
│  │ Completeness │ B (8/15)     │ ⚠️           │    │
│  └──────────────┴──────────────┴──────────────┘    │
│                                                      │
│  ⏳ Pending Review (1)                              │
│  ┌────────────────────────────────────────────┐    │
│  │ telus_cpk_001: Ready for review           │    │
│  │ [Review Now]  [Generate Guidance]          │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 💡 KORZYŚCI

### **Dla Artura (User):**
1. ✅ **Easy to Use** - Chat interface zamiast command line
2. ✅ **Visual Progress** - Real-time status investigation
3. ✅ **Transparency** - Widzisz co się dzieje
4. ✅ **Interactive** - Możesz zadawać pytania w trakcie
5. ✅ **Professional UI** - Modern, intuitive interface

### **Dla Aleksandra (Supervisor):**
1. ✅ **Full Visibility** - Dashboard z wszystkimi investigations
2. ✅ **Live Logs** - Real-time LMStudio activity
3. ✅ **Quality Metrics** - At-a-glance assessment
4. ✅ **Easy Review** - Click to review any investigation
5. ✅ **Guidance Interface** - Easy to provide feedback

### **Dla Local LLM:**
1. ✅ **Clear Instructions** - GUI makes task clearer
2. ✅ **Feedback Loop** - Sees Aleksander's guidance in UI
3. ✅ **Progress Tracking** - Knows where it stands
4. ✅ **Tool Visibility** - UI shows which tools available

---

## 🚀 IMPLEMENTATION PLAN

### **Priority 1: Basic Connection (2-3 days)**

1. ✅ Update destiny-chat-ui API endpoint → localhost:1234
2. ✅ Test basic chat with local LLM
3. ✅ Verify function calling works in UI
4. ✅ Add investigation mode toggle

### **Priority 2: Investigation Panel (2-3 days)**

1. ✅ Create InvestigationPanel component
2. ✅ Add WebSocket support to local_orchestrator.py
3. ✅ Implement real-time progress updates
4. ✅ Add source counter, quality indicator

### **Priority 3: Supervisor Dashboard (3-4 days)**

1. ✅ Create SupervisorDashboard page
2. ✅ Implement log streaming from LMStudio
3. ✅ Add quality metrics display
4. ✅ Create review interface

### **Priority 4: Polish & Testing (2-3 days)**

1. ✅ UI/UX improvements
2. ✅ Error handling
3. ✅ End-to-end testing
4. ✅ Documentation

**Total Time: 9-13 days (2-3 weeks)**

---

## 📝 NOTES FOR LATER

**Artur's Request:**
> "Zadanie na potem, pamiętaj aby mi je potem przypomnieć"

**When to Implement:**
- ✅ After basic hybrid system is tested
- ✅ After Telus investigation proves system works
- ✅ When user requests: "Czas na destiny-chat-ui integration!"

**Reminder Triggers:**
- User mentions: "chat ui", "interface", "przeglądarka"
- After successful hybrid system demonstration
- When asked: "co dalej?" or "next steps?"

**Priority:** HIGH - User explicitly requested this
**Status:** PENDING - Zapisane jako TODO
**Owner:** Aleksander will remind Artur when ready

---

## 🎯 VISION

**Ultimate Goal:**

```
Artur otwiera przeglądarkę:
  → localhost:3000/destiny-chat-ui

Wpisuje:
  → "Zbadaj transakcję Telusa"

Widzi real-time:
  → Local LLM scraping sources
  → Quality metrics updating
  → Aleksander reviewing work
  → Final report generated

Wszystko w pięknym, modern UI
Wszystko 100% local (privacy)
Wszystko 90% taniej (cost savings)
Wszystko professional quality (Bellingcat)

= PERFECT HYBRID INTELLIGENCE SYSTEM 🎉
```

---

**ZAPISANE. PRZYPOMNĘ CI O TYM, ARTUR! 🎯📌**
