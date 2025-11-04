# ⚡ Szybki Test - 30 sekund

## 🔍 Sprawdź że wszystko działa (PRZED instalacją)

```bash
# Test 1: Kontener działa?
docker ps | grep sms-postgres
```
✅ Zobaczysz: `sms-postgres` w liście

```bash
# Test 2: PostgreSQL odpowiada?
docker exec -i sms-postgres psql -U user -c "SELECT version();"
```
✅ Zobaczysz: wersję PostgreSQL 17.6

```bash
# Test 3: Twoje bazy są tam?
docker exec -i sms-postgres psql -U user -c "\l"
```
✅ Zobaczysz: listę Twoich baz

---

## 🚀 Instalacja (dosłownie 1 komenda)

```bash
cd /Users/artur/coursor-agents-destiny-folder
./setup_moj_postgres.sh
```

Skrypt:
1. Sprawdzi kontener ✓
2. Pokaże Twoje bazy ✓
3. Zapyta o zgodę ✓
4. Utworzy `destiny_team` ✓
5. Zainicjalizuje tabele ✓
6. Przetestuje ✓

**Czas: ~2 minuty**

---

## ✅ Po instalacji - Szybki test

```bash
# Test: Połączenie działa?
python3 postgres_polacz.py
```

Zobaczysz:
```
✅ Połączenie udane!

📊 Utworzone tabele:
  ✓ messages
  ✓ agent_contexts
  ✓ projects
  ✓ agent_work_queue
  ✓ decisions

📨 Wiadomości w bazie: 0
```

---

## 🎯 Najszybszy możliwy test (dosłownie 1 linia)

```bash
python3 -c "from postgres_context_store import PostgresContextStore; s = PostgresContextStore('dbname=destiny_team user=user password=password host=localhost port=5432'); print('✅ DZIAŁA!'); s.close()"
```

---

## 🔒 Weryfikacja bezpieczeństwa

```bash
# Zobacz że destiny_team jest oddzielona
docker exec -i sms-postgres psql -U user -c "
SELECT 
    datname as baza,
    pg_size_pretty(pg_database_size(datname)) as rozmiar
FROM pg_database 
WHERE datname IN ('postgres', 'destiny_team')
ORDER BY datname;
"
```

Zobaczysz:
```
     baza      | rozmiar
---------------+---------
 destiny_team  | 45 KB   ← Nowa (pusta)
 postgres      | 150 MB  ← Twoja (nietknięta)
```

---

## 💻 Użyj w kodzie (najprostszy przykład)

```python
from postgres_integration import DestinyTeamWithPostgres

# Połącz
team = DestinyTeamWithPostgres(
    "dbname=destiny_team user=user password=password host=localhost port=5432"
)

# Utwórz projekt
project_id = team.start_project("Test", "Test project")
print(f"✅ Projekt: {project_id}")

# Statystyki
stats = team.get_project_summary()
print(f"📊 Wiadomości: {stats['project_stats']['total_messages']}")

team.close()
```

Zapisz jako `test_quick.py` i uruchom:
```bash
python3 test_quick.py
```

---

## 🎉 To wszystko!

**3 kroki:**
1. `./setup_moj_postgres.sh` (instalacja)
2. `python3 postgres_polacz.py` (test)
3. Użyj w swoim kodzie! 🚀

**Twoje dane: BEZPIECZNE ✅**  
**Czas: 2 minuty ⚡**  
**Rezultat: Nieograniczony kontekst 🎯**
