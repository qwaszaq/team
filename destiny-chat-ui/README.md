# 🎯 Destiny Chat UI

**Graficzny interfejs do komunikacji z zespołem agentów Destiny Team**

## 📋 Opis projektu

Destiny Chat UI to webowa aplikacja typu chat, która umożliwia interakcję z 9 wyspecjalizowanymi agentami AI z Destiny Team Framework poprzez przyjazny, graficzny interfejs.

### Funkcje:
- 💬 Chat interface (jak Discord/Slack)
- 🤖 Wybór agenta do rozmowy (@Aleksander, @Tomasz, @All...)
- 📊 Status agentów w real-time
- 💾 Historia rozmów zapisana w bazie danych
- ⚡ Real-time updates przez WebSocket
- 🎨 Modern UI z TailwindCSS

## 🏗️ Architektura

```
destiny-chat-ui/
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + WebSocket
└── docs/              # Dokumentacja
```

### Stack techniczny:
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, Shadcn/ui
- **Backend:** FastAPI, WebSocket, Python 3.11+
- **Real-time:** WebSocket dla live updates
- **Database:** PostgreSQL (współdzielony z głównym projektem, ale osobny namespace)

## 🔒 Separacja od głównego projektu

**WAŻNE:** Ten projekt jest całkowicie oddzielony od głównego Destiny Team Framework:

✅ **Oddzielny folder:** `destiny-chat-ui/` nie miesza się z głównym projektem  
✅ **Własny PROJECT_ID:** `"destiny-chat-ui"` (nie `"destiny-team-framework-master"`)  
✅ **Własne dependencies:** Osobne `package.json` i `requirements.txt`  
✅ **Dane w DB:** Używa tego samego PostgreSQL, ale własny namespace  
✅ **Import agentów:** Read-only z `../agents/` (nie modyfikuje!)  

### Cleanup:
Jeśli chcesz usunąć ten POC:
```bash
# Usuń folder
rm -rf destiny-chat-ui/

# Wyczyść dane z DB
python3 ../cleanup_project.py --project-id destiny-chat-ui
```

## 🚀 Quick Start

### Prerequisites:
- Node.js 18+
- Python 3.11+
- Docker (dla baz danych)
- Działający Destiny Team Framework

### 1. Backend Setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 2. Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

### 3. Otwórz w przeglądarce:
```
http://localhost:5173
```

## 📚 Dokumentacja

- [Backend API](docs/backend-api.md)
- [Frontend Components](docs/frontend-components.md)
- [User Guide](docs/user-guide.md)
- [Development Guide](docs/development-guide.md)

## 👥 Zespół (Destiny Team Agents)

Projekt stworzony przez agentów Destiny Team:

- **Aleksander Nowak** - Orchestrator (koordynacja projektu)
- **Joanna Mazur** - UX Designer (design + frontend)
- **Tomasz Zieliński** - Developer (backend + integracja)
- **Anna Nowakowska** - QA Engineer (testowanie)
- **Piotr Szymański** - DevOps (Docker + deploy)
- **Helena Kowalczyk** - Knowledge Manager (dokumentacja)

## 📄 Licencja

Ten projekt jest POC (Proof of Concept) dla Destiny Team Framework.

---

**Wersja:** 0.1.0-POC  
**Data:** 2025-11-03  
**Status:** 🚧 W budowie
