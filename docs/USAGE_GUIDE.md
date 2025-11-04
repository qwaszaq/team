# 🚀 Destiny System - Przewodnik Użycia

**Data utworzenia:** 2025-11-04  
**Status systemu:** ✅ Operational  
**Wersja:** 1.0

---

## 📋 Spis Treści

1. [Szybki Start](#szybki-start)
2. [Podstawowe Użycie](#podstawowe-użycie)
3. [Praca z Dokumentacją](#praca-z-dokumentacją)
4. [Praca z Kodem](#praca-z-kodem)
5. [Wyszukiwanie Wiedzy](#wyszukiwanie-wiedzy)
6. [Praca z Agentami](#praca-z-agentami)
7. [Dashboardy i Monitoring](#dashboardy-i-monitoring)
8. [Przykłady Praktyczne](#przykłady-praktyczne)

---

## 🚀 Szybki Start

### Uruchomienie Systemu

```bash
# Jedna komenda uruchamia wszystko
./start_destiny_system.sh
```

**Co się dzieje:**
- ✅ Docker sprawdzony
- ✅ 4 bazy danych uruchomione (Qdrant, PostgreSQL, Neo4j, Redis)
- ✅ Helena Watcher aktywowana (auto-processing)
- ✅ Wszystko zweryfikowane i gotowe

### Sprawdzenie Statusu

```bash
# Zobacz logi Heleny (real-time monitoring)
tail -f logs/watcher.log

# Status kontenerów Docker
docker ps

# Ile punktów w Qdrant
curl -s http://localhost:6333/collections/destiny-team-framework-master | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['result']['points_count'])"
```

---

## 📝 Podstawowe Użycie

### 1. Dodaj Dokumentację (Automatycznie Indeksowana!)

```bash
# Utwórz nowy plik markdown w docs/
cat > docs/my-feature.md << 'EOF'
# Moja Nowa Funkcja

## Opis
To jest opis mojej nowej funkcji...

## Implementacja
Szczegóły implementacji...
EOF
```

**Co się stanie automatycznie:**
1. ⏱️ **W ciągu 2-3 sekund** Helena wykryje plik
2. 📊 Wygeneruje metadane i zindeksuje
3. 🗄️ Doda do **wszystkich 4 baz danych:**
   - PostgreSQL (strukturalne dane)
   - Neo4j (relacje w grafie wiedzy)
   - Qdrant (wyszukiwanie semantyczne)
   - Redis (szybki cache)
4. ✅ Potwierdzenie w `logs/watcher.log`

**Sprawdź:**
```bash
# Zobacz że Helena to przetworzyła
tail -20 logs/watcher.log

# Sprawdź w Qdrant dashboard
open http://localhost:6333/dashboard
```

---

### 2. Zmień Kod (Auto-Dokumentacja!)

```bash
# Zrób jakąkolwiek zmianę w kodzie
echo "# TODO: Add feature X" >> some_file.py

# Commituj
git add some_file.py
git commit -m "feat: Add feature X placeholder"
```

**Co się stanie automatycznie:**
1. 🪝 **Post-commit hook** się włączy
2. 📝 Wygeneruje dokumentację w `docs/auto-generated/YYYY-MM-DD/`
3. 👁️ Helena wykryje nowy plik .md
4. 🗄️ Zindeksuje w 4 bazach
5. ✅ Twoja zmiana jest teraz przeszukiwalna!

**Sprawdź:**
```bash
# Zobacz auto-wygenerowaną dokumentację
ls -lh docs/auto-generated/$(date +%Y-%m-%d)/

# Przeczytaj
cat docs/auto-generated/$(date +%Y-%m-%d)/COMMIT_*.md
```

---

## 🔍 Wyszukiwanie Wiedzy

### Qdrant - Wyszukiwanie Semantyczne

**Dashboard (najłatwiejszy):**
```bash
open http://localhost:6333/dashboard
```

**Programatically (Python):**
```python
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# Wyszukaj podobne dokumenty
results = client.search(
    collection_name="destiny-team-framework-master",
    query_text="How do I fix database connectivity issues?",
    limit=5
)

for result in results:
    print(f"Score: {result.score}")
    print(f"Document: {result.payload['title']}")
    print(f"Path: {result.payload['file_path']}")
    print("---")
```

### Neo4j - Graf Wiedzy

**Browser:**
```bash
open http://localhost:7474
```

**Przykładowe Cypher Queries:**
```cypher
// Znajdź wszystkie dokumenty związane z "Redis"
MATCH (d:Document)-[:RELATES_TO]->(t:Topic {name: "Redis"})
RETURN d.title, d.file_path

// Znajdź commity typu bugfix
MATCH (c:Commit {type: "bugfix"})
RETURN c.hash, c.subject, c.timestamp

// Znajdź powiązania między dokumentami
MATCH (d1:Document)-[r]->(d2:Document)
RETURN d1.title, type(r), d2.title
LIMIT 20
```

### PostgreSQL - Zapytania Strukturalne

```bash
# Połącz się z bazą
psql -h localhost -U postgres -d destinyframework
```

```sql
-- Zobacz ostatnie dokumenty
SELECT title, document_type, created_at 
FROM documents 
ORDER BY created_at DESC 
LIMIT 10;

-- Znajdź dokumenty o konkretnym temacie
SELECT title, file_path 
FROM documents 
WHERE content_preview ILIKE '%connectivity%';

-- Statystyki
SELECT document_type, COUNT(*) 
FROM documents 
GROUP BY document_type;
```

### Redis - Szybki Cache

```bash
# Zobacz co jest w cache
redis-cli -h localhost -p 6379 KEYS "*"

# Sprawdź konkretny klucz
redis-cli -h localhost -p 6379 GET "redis_20251104_124358_COMMIT_550ceab_bugfix"

# Statystyki
redis-cli -h localhost -p 6379 INFO stats
```

---

## 🤖 Praca z Agentami

### Dostępne Agenty

Twój system ma **9-osobowy zespół AI**:

1. **Aleksander Nowak** - Orchestrator
2. **Helena Kowalczyk** - Knowledge Manager (auto-processing!)
3. **Magdalena Kowalska** - Product Manager
4. **Katarzyna Wiśniewska** - Architect
5. **Tomasz Zieliński** - Developer
6. **Anna Nowakowska** - QA Engineer
7. **Piotr Szymański** - DevOps Engineer
8. **Michał Dąbrowski** - Security Specialist
9. **Joanna Wójcik** - Data Scientist

### Uruchom Demo Zespołu

```bash
# Współpraca wszystkich agentów
python3 examples/enhanced_collaboration_demo.py

# Test systemu z weryfikacją
python3 examples/helena_with_verification_example.py

# Pełny test integracyjny
python3 tests/test_integrated_system.py
```

### Programatyczne Użycie

```python
from full_team_integration import FullDestinyTeam

# Zainicjuj zespół
team = FullDestinyTeam(project_id="my-project")

# Poproś o analizę
team.analyze_requirement("I need to implement user authentication")

# Poproś o decyzję architektoniczną
team.make_architecture_decision("Should we use Redis for sessions?")

# Poproś o code review
team.review_code("path/to/code.py")
```

---

## 📊 Dashboardy i Monitoring

### Qdrant Dashboard
```bash
open http://localhost:6333/dashboard
```
**Pokazuje:**
- Liczbę punktów (aktualnie 362+)
- Status kolekcji
- Wyszukiwanie semantyczne
- Statystyki indeksowania

### Neo4j Browser
```bash
open http://localhost:7474
```
**Login:** neo4j / hasło z konfiguracji

**Pokazuje:**
- Graf wiedzy
- Relacje między encjami
- Wizualizacja powiązań
- Cypher queries

### Helena Logs (Real-time)
```bash
# Monitoring na żywo
tail -f logs/watcher.log

# Ostatnie 50 linii
tail -50 logs/watcher.log

# Szukaj błędów
grep "ERROR" logs/watcher.log
```

### Docker Status
```bash
# Status wszystkich kontenerów
docker ps

# Logi konkretnego kontenera
docker logs sms-qdrant
docker logs sms-postgres
docker logs sms-neo4j
docker logs kg-redis
```

---

## 💡 Przykłady Praktyczne

### Przykład 1: Dodanie Nowej Funkcji z Dokumentacją

```bash
# 1. Utwórz dokumentację funkcji
cat > docs/features/user-login.md << 'EOF'
# User Login Feature

## Overview
New login system with OAuth2 support.

## Components
- Login form
- OAuth2 integration
- Session management

## Security
- JWT tokens
- Redis session store
- Rate limiting
EOF

# 2. Helena automatycznie zindeksuje (czekaj 3 sekundy)
sleep 3

# 3. Sprawdź że jest w systemie
tail -20 logs/watcher.log

# 4. Teraz możesz wyszukać semantycznie
# "user authentication OAuth" → znajdzie Twój dokument!
```

### Przykład 2: Fix Bug i Auto-Dokumentacja

```bash
# 1. Napraw bug
vim some_file.py

# 2. Commit z opisem
git add some_file.py
git commit -m "fix: Resolve login timeout issue

The login was timing out after 5 seconds.
Increased timeout to 30 seconds and added retry logic."

# 3. Post-commit hook AUTOMATYCZNIE:
#    - Wygeneruje docs/auto-generated/YYYY-MM-DD/COMMIT_xxxxx_bugfix.md
#    - Helena zindeksuje to
#    - Będzie przeszukiwalne w 4 bazach

# 4. Sprawdź auto-doc
ls -lh docs/auto-generated/$(date +%Y-%m-%d)/
cat docs/auto-generated/$(date +%Y-%m-%d)/COMMIT_*_bugfix.md
```

### Przykład 3: Wyszukiwanie Rozwiązań

```python
# search_knowledge.py
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

def search_knowledge(query: str, limit: int = 5):
    """Wyszukaj w bazie wiedzy"""
    results = client.search(
        collection_name="destiny-team-framework-master",
        query_text=query,
        limit=limit
    )
    
    print(f"\n🔍 Wyniki dla: '{query}'\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.payload.get('title', 'No title')}")
        print(f"   Score: {result.score:.3f}")
        print(f"   Path: {result.payload.get('file_path', 'Unknown')}")
        print(f"   Preview: {result.payload.get('content_preview', '')[:100]}...")
        print()

# Użycie
search_knowledge("How to fix Redis connectivity")
search_knowledge("PostgreSQL database schema")
search_knowledge("startup script timeout issues")
```

### Przykład 4: Morning Briefing (Helena's Summary)

```python
# morning_brief.py
from knowledge_manager_agent import KnowledgeManagerAgent

agent = KnowledgeManagerAgent(
    name="Helena",
    project_id="destiny-framework"
)

# Pobierz podsumowanie
summary = agent.summarize_project()

print("📊 MORNING BRIEFING")
print("=" * 60)
print(summary)
print("\n📈 Recent Changes:")
recent_docs = agent.get_recent_documents(days=1)
for doc in recent_docs:
    print(f"  • {doc['title']} ({doc['created_at']})")
```

---

## 🛑 Zatrzymanie Systemu

```bash
# Zatrzymaj Helena Watcher
kill $(ps aux | grep realtime_md_watcher | grep -v grep | awk '{print $2}')

# Zatrzymaj kontenery (opcjonalne)
docker stop sms-qdrant sms-postgres sms-neo4j kg-redis

# Lub zostaw je działające (nie będą używać dużo zasobów)
```

---

## 🆘 Troubleshooting

### Problem: Helena nie wykrywa plików

```bash
# Sprawdź czy watcher działa
ps aux | grep realtime_md_watcher

# Sprawdź logi
tail -50 logs/watcher.log

# Restart watchera
pkill -f realtime_md_watcher
./start_watcher_conda.sh
```

### Problem: Brak połączenia z bazą

```bash
# Sprawdź kontenery
docker ps

# Restart kontenera
docker restart sms-postgres  # lub inny

# Sprawdź porty
nc -z localhost 5432  # PostgreSQL
nc -z localhost 6333  # Qdrant
nc -z localhost 7474  # Neo4j
nc -z localhost 6379  # Redis
```

### Problem: Post-commit hook nie działa

```bash
# Sprawdź czy hook istnieje
ls -la .git/hooks/post-commit

# Sprawdź uprawnienia
chmod +x .git/hooks/post-commit

# Test ręcznie
python3 scripts/auto_doc_generator.py HEAD
```

---

## 📚 Dodatkowe Zasoby

- **Dokumentacja zespołu:** `docs/team/`
- **Statusy projektów:** `docs/status/`
- **Auto-dokumentacja:** `docs/auto-generated/`
- **Przykłady:** `examples/`
- **Testy:** `tests/`

---

## 🎯 Najważniejsze Porady

1. **Dokumentuj wszystko w Markdown** - Helena automatycznie zindeksuje
2. **Pisz dobre commit messages** - będą automatycznie dokumentowane
3. **Używaj semantic search** - Qdrant znajdzie podobne koncepty
4. **Sprawdzaj logi** - `tail -f logs/watcher.log` pokazuje co się dzieje
5. **Eksploruj graf** - Neo4j pokazuje powiązania między wiedzą

---

**System jest gotowy! Twórz, commituj, dokumentuj - reszta dzieje się automatycznie!** 🚀

