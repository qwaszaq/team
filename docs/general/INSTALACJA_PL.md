# 🚀 Instalacja - Twój Kontener PostgreSQL

## 📋 Twoja Konfiguracja (z inspect)

```
Kontener: sms-postgres
User:     user
Password: password
Port:     5432
Baza:     postgres
```

---

## ⚡ Super Szybka Instalacja (2 minuty)

```bash
cd /Users/artur/coursor-agents-destiny-folder
chmod +x setup_moj_postgres.sh
./setup_moj_postgres.sh
```

**To wszystko!** Skrypt:
1. ✅ Sprawdzi Twój kontener `sms-postgres`
2. ✅ Pokaże Twoje obecne bazy
3. ✅ Utworzy NOWĄ bazę `destiny_team`
4. ✅ Zainicjalizuje tabele
5. ✅ Zapisze konfigurację
6. ✅ Przetestuje połączenie

---

## 🔒 Bezpieczeństwo

### Przed instalacją:
```
Twój kontener sms-postgres:
├── postgres (Twoja obecna baza)
└── [inne twoje bazy]
```

### Po instalacji:
```
Twój kontener sms-postgres:
├── postgres (✅ NIETKNIĘTA)
├── [inne twoje bazy] (✅ NIETKNIĘTE)
└── destiny_team (🆕 NOWA - dla agentów)
```

**Zero wpływu na Twoje dane!**

---

## ✅ Po Instalacji

### Test 1: Sprawdź połączenie
```bash
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

### Test 2: Sprawdź że Twoje dane są nietknięte
```bash
# Zobacz wszystkie bazy
docker exec -i sms-postgres psql -U user -c "\l"

# Zobacz że Twoje tabele są nietknięte
docker exec -i sms-postgres psql -U user -d postgres -c "\dt"
```

---

### Test 3: Uruchom pełne testy
```bash
python3 test_postgres_context.py
```

5 testów sprawdzi:
- ✅ Zapisywanie wiadomości
- ✅ Inteligentne wyszukiwanie kontekstu
- ✅ Oddzielne bazy wiedzy agentów
- ✅ Pełna integracja z systemem
- ✅ Persystencja między sesjami

---

## 💻 Użycie w Kodzie

### Prosty przykład:

```python
from postgres_integration import DestinyTeamWithPostgres
from destiny_team import MessageType, ProjectState

# Wczytaj connection string (zapisany przez skrypt)
with open('.env.postgres') as f:
    for line in f:
        if 'POSTGRES_CONNECTION_STRING' in line:
            conn_string = line.split('=', 1)[1].strip().strip('"')

# Utwórz team z nieograniczonym kontekstem
team = DestinyTeamWithPostgres(conn_string)

# Start projektu
project_id = team.start_project(
    "Moja Aplikacja",
    "Opis projektu"
)

print(f"✅ Projekt utworzony: {project_id}")

# Agenci komunikują się (automatycznie zapisywane w PostgreSQL)
pm = team.agents['pm']
pm.send_message(
    recipient=None,
    message_type=MessageType.REQUEST,
    content="Jakie są główne wymagania?"
)

# Architekt myśli z NIEOGRANICZONYM kontekstem
architect = team.agents['architect']
response = architect.think(
    "Zaprojektuj architekturę systemu",
    project_state=ProjectState(
        project_name="Moja Aplikacja",
        description="Opis projektu"
    )
)

print(f"\n🏗️ Architekt odpowiada:\n{response}")

# Wyszukaj w całej historii
results = team.search_project_history("architektura")
print(f"\n🔍 Znaleziono {len(results)} wiadomości o architekturze")

# Statystyki projektu
summary = team.get_project_summary()
print(f"\n📊 Statystyki:")
print(f"  Wiadomości: {summary['project_stats']['total_messages']}")
print(f"  Aktywni agenci: {summary['project_stats']['active_agents']}")

# Zamknij
team.close()
```

---

### Wznowienie projektu (później):

```python
# Dzień/tydzień/miesiąc później...
team = DestinyTeamWithPostgres(conn_string, project_id=project_id)

# Cała historia dostępna!
history = team.search_project_history("wymagania")
print(f"Znaleziono {len(history)} wiadomości z poprzednich sesji")
```

---

## 🔍 Monitoring

### Zobacz co się dzieje w bazie:

```bash
# Połącz się z destiny_team
docker exec -it sms-postgres psql -U user -d destiny_team

# W psql:
\dt                                           # Lista tabel
SELECT COUNT(*) FROM messages;               # Ile wiadomości
SELECT sender, content FROM messages 
  ORDER BY timestamp DESC LIMIT 5;           # Ostatnie wiadomości
\q                                            # Wyjdź
```

---

### Python monitoring:

```python
from postgres_context_store import PostgresContextStore

store = PostgresContextStore(conn_string)

# Statystyki projektu
stats = store.get_project_statistics(project_id)
print(f"Wiadomości: {stats['total_messages']}")
print(f"Aktywni agenci: {stats['active_agents']}")
print(f"Debaty: {stats['debates']}")
print(f"Zatwierdzenia: {stats['approvals']}")

# Aktywność agenta
activity = store.get_agent_activity_summary(
    project_id=project_id,
    agent_name="Katarzyna Wiśniewska"
)
print(f"\nArchitekt:")
print(f"  Wysłane wiadomości: {activity['messages_sent']}")
print(f"  Kontakty: {activity['agents_contacted']}")
print(f"  Debaty: {activity['debates_initiated']}")

store.close()
```

---

## 📊 Rozmiar Bazy

```bash
# Sprawdź rozmiar wszystkich baz
docker exec -i sms-postgres psql -U user << 'EOF'
SELECT 
    datname as "Baza",
    pg_size_pretty(pg_database_size(datname)) as "Rozmiar"
FROM pg_database
WHERE datname NOT IN ('template0', 'template1')
ORDER BY pg_database_size(datname) DESC;
EOF
```

Zobaczysz:
```
     Baza      | Rozmiar
---------------+---------
 postgres      | 150 MB  ← Twoje dane (bez zmian)
 destiny_team  | 45 KB   ← Nowa baza (prawie pusta)
```

---

## 🐛 Troubleshooting

### Kontener nie działa?
```bash
docker ps | grep sms-postgres
# Jeśli nie widać, uruchom:
docker start sms-postgres
```

### Połączenie odrzucone?
```bash
# Sprawdź port
docker port sms-postgres 5432

# Sprawdź logi
docker logs sms-postgres --tail 50
```

### Baza już istnieje?
```bash
# To OK! Możesz jej używać
# Sprawdź połączenie:
python3 postgres_polacz.py
```

### Chcę usunąć i zacząć od nowa?
```bash
# Usuń bazę destiny_team
docker exec -i sms-postgres psql -U user -c "DROP DATABASE destiny_team;"

# Uruchom setup ponownie
./setup_moj_postgres.sh
```

---

## 🎯 FAQ

### Q: Czy mogę używać moich aplikacji jednocześnie?
**A: TAK!** Twoje aplikacje używają swoich baz (`postgres`, etc.), Destiny Team używa `destiny_team`. Zero kolizji.

### Q: Co jeśli muszę zrestartować kontener?
**A: Wszystko działa!** Dane w PostgreSQL są trwałe (volume: `kg-service_postgres_data`).

### Q: Ile to zajmie miejsca?
**A:**
- Pusta: ~45 KB
- 1,000 wiadomości: ~5 MB
- 10,000 wiadomości: ~40 MB
- 100,000 wiadomości: ~400 MB

### Q: Jak zrobić backup?
```bash
# Backup tylko destiny_team
docker exec sms-postgres pg_dump -U user destiny_team > destiny_backup.sql

# Restore
docker exec -i sms-postgres psql -U user destiny_team < destiny_backup.sql
```

---

## 🎉 Podsumowanie

Po uruchomieniu `./setup_moj_postgres.sh` będziesz miał:

✅ **Nieograniczony kontekst** dla agentów  
✅ **Twoje dane bezpieczne** (oddzielna baza)  
✅ **Persystencja** między sesjami  
✅ **Wyszukiwanie** w całej historii  
✅ **Statystyki** i monitoring  
✅ **Zero wpływu** na istniejący system  

**Gotowy? Uruchom setup!** 🚀

```bash
./setup_moj_postgres.sh
```
