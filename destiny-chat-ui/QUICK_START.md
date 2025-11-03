# 🚀 Destiny Chat UI - Quick Start Guide

## ⚡ Szybkie uruchomienie (5 minut)

### Prerequisite: Uruchom główny projekt

```bash
# 1. Sprawdź czy Docker containers działają
cd /Users/artur/coursor-agents-destiny-folder
docker ps | grep -E "postgres|neo4j|qdrant|redis"

# Powinny być 4 kontenery: postgres, neo4j, qdrant, redis
# Jeśli nie działają:
docker-compose up -d
```

### Krok 1: Backend Setup (2 minuty)

```bash
# Przejdź do projektu
cd /Users/artur/coursor-agents-destiny-folder/destiny-chat-ui

# Stwórz środowisko
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Skopiuj konfigurację
cp ../.env.example .env

# Uruchom backend
python main.py
```

**Backend powinien być dostępny na:** http://localhost:8000

**API Docs:** http://localhost:8000/docs

---

### Krok 2: Frontend Setup (3 minuty)

```bash
# W NOWYM terminalu
cd /Users/artur/coursor-agents-destiny-folder/destiny-chat-ui/frontend

# Zainstaluj Node.js dependencies
npm install

# Uruchom development server
npm run dev
```

**Frontend powinien być dostępny na:** http://localhost:5173

---

## ✅ Weryfikacja

### 1. Backend działa?
Otwórz: http://localhost:8000

Powinno wyświetlić:
```json
{
  "service": "Destiny Chat UI API",
  "status": "operational",
  "version": "0.1.0",
  "project_id": "destiny-chat-ui",
  "agents": 9
}
```

### 2. Frontend działa?
Otwórz: http://localhost:5173

Powinien załadować się chat interface z listą agentów po lewej stronie.

### 3. Test komunikacji
1. Wybierz agenta (np. @Aleksander)
2. Napisz wiadomość: "Cześć!"
3. Powinieneś otrzymać odpowiedź od agenta

---

## 🎯 Pierwsze kroki

### Wybór agenta:
- **@All** - wysyła do Aleksandra (orchestrator), który koordynuje zespół
- **@Aleksander** - bezpośrednio do orchestratora
- **@Tomasz** - do developera
- **@Anna** - do QA Engineer
- itd.

### Przykładowe pytania:
```
"Chcę zbudować system logowania"
"Potrzebuję pomocy z testami"
"Jak zarchitekturować aplikację?"
"Zaprojektuj mi ładny UI dla dashboardu"
```

---

## 🐛 Troubleshooting

### Problem: Backend nie startuje
**Błąd:** `ModuleNotFoundError: No module named 'agents'`

**Rozwiązanie:**
```bash
# Backend musi mieć dostęp do głównego projektu
cd backend
# Sprawdź czy main.py ma:
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
```

### Problem: Agents = 0 w response
**Oznacza:** Agenci się nie zainicjalizowali

**Rozwiązanie:**
```bash
# Sprawdź logi backend:
# Powinny być:
# ✅ Initialized 9 agents

# Jeśli ❌ Error initializing agents:
# Sprawdź czy PostgreSQL działa i czy masz connection
```

### Problem: Frontend pokazuje błąd połączenia
**Błąd:** "Error sending message"

**Rozwiązanie:**
1. Sprawdź czy backend działa (http://localhost:8000)
2. Sprawdź CORS settings w backend/main.py
3. Sprawdź network tab w devtools przeglądarki

### Problem: Brak odpowiedzi od agentów
**Możliwe przyczyny:**
- Backend nie ma połączenia z bazami danych
- Agenci nie zostali zainicjalizowani

**Rozwiązanie:**
```bash
# Terminal backend - sprawdź logi:
# ✅ Initialized 9 agents
# ✅ {agent.name} ({agent.role}) initialized

# Jeśli brak, sprawdź:
docker ps  # czy PostgreSQL działa
```

---

## 📊 Sprawdzenie poprawności

### Test 1: Health Check
```bash
curl http://localhost:8000/
```

Wynik powinien pokazać `"agents": 9`

### Test 2: Lista agentów
```bash
curl http://localhost:8000/agents
```

Powinien zwrócić tablicę z 9 agentami.

### Test 3: Wysłanie wiadomości
```bash
curl -X POST http://localhost:8000/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello",
    "to_agent": "@Aleksander",
    "from_user": "Test"
  }'
```

Powinna przyjść odpowiedź od Aleksandra.

---

## 🎉 Gotowe!

Jeśli wszystkie testy przeszły, masz działający Destiny Chat UI!

**Teraz możesz:**
- Rozmawiać z agentami
- Zadawać pytania
- Prosić o pomoc w projektach
- Testować różne scenariusze

---

## 📚 Dalsze kroki

- [User Guide](docs/user-guide.md) - Jak używać interfejsu
- [Backend API](docs/backend-api.md) - Dokumentacja API
- [Development Guide](docs/development-guide.md) - Jak modyfikować kod

---

**Stworzony przez:** Destiny Team  
**Orchestrator:** Aleksander Nowak  
**Developers:** Tomasz Zieliński, Joanna Mazur  
**Date:** 2025-11-03
