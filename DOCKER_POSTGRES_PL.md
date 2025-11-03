# PostgreSQL w Docker - Instrukcja (Polski)

## 🔒 Bezpieczeństwo Danych

**WAŻNE: Twoje istniejące dane są w 100% bezpieczne!**

System utworzy:
- ✅ **Nową bazę danych** o nazwie `destiny_team`
- ✅ W tej samej instancji PostgreSQL (ten sam Docker container)
- ✅ **Całkowicie oddzielnie** od Twoich obecnych baz
- ✅ **Zero wpływu** na istniejące dane

---

## 🚀 Automatyczna Instalacja (Zalecane)

### Krok 1: Uruchom skrypt instalacyjny

```bash
cd /Users/artur/coursor-agents-destiny-folder
chmod +x setup_docker_postgres.sh
./setup_docker_postgres.sh
```

Skrypt automatycznie:
1. Znajdzie Twój kontener PostgreSQL
2. Utworzy nową bazę `destiny_team`
3. Zainicjalizuje tabele
4. Zapisze konfigurację
5. Przetestuje połączenie

**To zajmie ~2 minuty i nic nie zepsuje!**

---

## 🔧 Instalacja Manualna (Jeśli wolisz)

### Krok 1: Sprawdź nazwę kontenera

```bash
docker ps
```

Znajdź kontener z PostgreSQL (np. `postgres`, `my-postgres`, itp.)

### Krok 2: Utwórz nową bazę danych

```bash
# Zamień 'postgres_container' na nazwę Twojego kontenera
docker exec -it postgres_container psql -U postgres -c "CREATE DATABASE destiny_team;"
```

### Krok 3: Zobacz wszystkie bazy (weryfikacja)

```bash
docker exec -it postgres_container psql -U postgres -c "\l"
```

Zobaczysz:
```
                                List of databases
     Name      |  Owner   | Encoding | ...
---------------+----------+----------+-----
 postgres      | postgres | UTF8     | ...  <- Twoja oryginalna baza
 moja_baza     | postgres | UTF8     | ...  <- Twoje dane (nietknięte!)
 destiny_team  | postgres | UTF8     | ...  <- Nowa baza (pusta)
```

### Krok 4: Znajdź port

```bash
docker port postgres_container 5432
```

Zobaczysz np: `0.0.0.0:5432` (port to `5432`)

### Krok 5: Utwórz connection string

```python
# Jeśli bez hasła:
conn_string = "dbname=destiny_team user=postgres host=localhost port=5432"

# Jeśli z hasłem:
conn_string = "dbname=destiny_team user=postgres password=twoje_haslo host=localhost port=5432"
```

### Krok 6: Zainicjalizuj schemat

```bash
python3 << 'EOF'
from postgres_context_store import PostgresContextStore

conn_string = "dbname=destiny_team user=postgres host=localhost port=5432"
store = PostgresContextStore(conn_string)
print("✅ Schema utworzona!")
store.close()
EOF
```

---

## ✅ Test Połączenia

```bash
python3 postgres_connect.py
```

Powinno pokazać:
```
✅ Połączenie udane!

Tabele utworzone:
  - messages
  - agent_contexts
  - projects
  - agent_work_queue
  - decisions
```

---

## 🐳 Docker Compose (Opcjonalnie - Osobna Instancja)

Jeśli mimo wszystko wolisz **osobną instancję PostgreSQL** tylko dla Destiny Team:

```yaml
# docker-compose-destiny.yml
version: '3.8'

services:
  postgres-destiny:
    image: postgres:15
    container_name: destiny-postgres
    environment:
      POSTGRES_USER: destiny
      POSTGRES_PASSWORD: destiny123
      POSTGRES_DB: destiny_team
    ports:
      - "5433:5432"  # Inny port, żeby nie kolidować!
    volumes:
      - destiny_data:/var/lib/postgresql/data

volumes:
  destiny_data:
```

Uruchom:
```bash
docker-compose -f docker-compose-destiny.yml up -d
```

Connection string:
```python
"dbname=destiny_team user=destiny password=destiny123 host=localhost port=5433"
```

---

## 📊 Weryfikacja Bezpieczeństwa

### Sprawdź rozmiar baz danych

```bash
docker exec -it postgres_container psql -U postgres -c "
SELECT 
    datname as database,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
"
```

Zobaczysz:
```
   database    |  size
---------------+---------
 moja_baza     | 150 MB  <- Twoje dane (bez zmian!)
 postgres      | 8 MB
 destiny_team  | 40 KB   <- Nowa baza (prawie pusta)
```

### Sprawdź tabele w różnych bazach

```bash
# Twoje istniejące bazy (bez zmian)
docker exec -it postgres_container psql -U postgres -d moja_baza -c "\dt"

# Nowa baza destiny_team (tylko nasze tabele)
docker exec -it postgres_container psql -U postgres -d destiny_team -c "\dt"
```

---

## 💡 Przykład Użycia

```python
from postgres_integration import DestinyTeamWithPostgres

# Połącz z nową bazą destiny_team
team = DestinyTeamWithPostgres(
    postgres_connection_string="dbname=destiny_team user=postgres host=localhost port=5432"
)

# Start projektu
project_id = team.start_project(
    "Mój Projekt",
    "Opis projektu"
)

# Agenci komunikują się
pm = team.agents['pm']
pm.send_message(None, MessageType.REQUEST, "Jakie są wymagania?")

# Wszystko zapisywane w destiny_team (NIE w Twoich bazach!)
summary = team.get_project_summary()
print(f"Wiadomości: {summary['project_stats']['total_messages']}")

team.close()
```

---

## 🔍 Monitoring

### Zobacz co się dzieje w destiny_team

```bash
# Połącz się z bazą
docker exec -it postgres_container psql -U postgres -d destiny_team

# W psql:
\dt                                    -- Lista tabel
SELECT COUNT(*) FROM messages;        -- Ile wiadomości
SELECT * FROM messages ORDER BY timestamp DESC LIMIT 5;  -- Ostatnie wiadomości
\q                                     -- Wyjdź
```

---

## 🛡️ FAQ Bezpieczeństwo

### Q: Czy to może zepsuć moje dane?
**A: NIE!** Używamy **osobnej bazy danych** (`destiny_team`). Twoje bazy są całkowicie nietknięte.

### Q: Co jeśli coś pójdzie nie tak?
**A: Nic się nie stanie** Twoim danym. Najwyżej usuń bazę `destiny_team`:
```bash
docker exec -it postgres_container psql -U postgres -c "DROP DATABASE destiny_team;"
```

### Q: Czy mogę używać obu systemów jednocześnie?
**A: TAK!** Twoje aplikacje dalej używają swoich baz, Destiny Team używa `destiny_team`.

### Q: Jak dużo miejsca to zajmie?
**A: Bardzo mało.** 
- Pusta baza: ~40 KB
- Po 1000 wiadomości: ~5 MB
- Po 10,000 wiadomości: ~40 MB

### Q: Co jeśli chcę to całkowicie oddzielić?
**A: Użyj Docker Compose** (zobacz powyżej) żeby mieć całkowicie osobną instancję PostgreSQL.

---

## 📞 Troubleshooting

### Błąd: "database already exists"
```bash
# To OK! Baza już istnieje, możesz jej używać
# Sprawdź połączenie:
python3 postgres_connect.py
```

### Błąd: "could not connect"
```bash
# Sprawdź czy kontener działa
docker ps

# Sprawdź logi
docker logs postgres_container

# Sprawdź port
docker port postgres_container 5432
```

### Błąd: "permission denied"
```bash
# Spróbuj z sudo (jeśli Docker wymaga)
sudo docker exec -it postgres_container psql -U postgres
```

---

## 🎯 Podsumowanie

**Zalecana opcja:**
✅ Użyj automatycznego skryptu instalacyjnego:
```bash
./setup_docker_postgres.sh
```

**To co robi:**
1. Tworzy NOWĄ bazę `destiny_team` w Twojej istniejącej instancji
2. Twoje dane pozostają nietknięte (w innych bazach)
3. Wszystko jest oddzielone i bezpieczne
4. Zajmuje 2 minuty

**Wynik:**
- ✅ Nieograniczony kontekst dla agentów
- ✅ Twoje dane bezpieczne
- ✅ Wszystko w jednej instancji PostgreSQL
- ✅ Łatwy monitoring i backup

---

**Masz pytania? Uruchom skrypt i zobacz sam, że to bezpieczne! 🚀**
