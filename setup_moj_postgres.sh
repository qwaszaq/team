#!/bin/bash
# Setup dla Twojego kontenera PostgreSQL: sms-postgres

echo "================================================"
echo "  PostgreSQL Setup dla Destiny Team"
echo "  Kontener: sms-postgres"
echo "================================================"
echo ""

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Twoje dane z inspect
CONTAINER_NAME="sms-postgres"
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_PORT="5432"

echo -e "${BLUE}📦 Twój kontener: $CONTAINER_NAME${NC}"
echo -e "${BLUE}👤 User: $POSTGRES_USER${NC}"
echo -e "${BLUE}🔌 Port: $POSTGRES_PORT${NC}"
echo ""

# Sprawdź czy kontener działa
echo -e "${YELLOW}Krok 1: Sprawdzanie kontenera...${NC}"
if ! docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}❌ Kontener $CONTAINER_NAME nie jest uruchomiony${NC}"
    echo ""
    echo "Uruchom kontener i spróbuj ponownie."
    exit 1
fi
echo -e "${GREEN}✓ Kontener działa${NC}"
echo ""

# Pokaż obecne bazy (przed utworzeniem nowej)
echo -e "${YELLOW}Krok 2: Twoje obecne bazy danych:${NC}"
echo ""
docker exec -i $CONTAINER_NAME psql -U $POSTGRES_USER << EOF
\l
EOF
echo ""
echo -e "${BLUE}👆 To są Twoje obecne bazy - zaraz dodamy 'destiny_team'${NC}"
echo ""

# Pytaj o potwierdzenie
echo -e "${YELLOW}Teraz utworzę NOWĄ bazę 'destiny_team' w tym samym kontenerze.${NC}"
echo -e "${GREEN}Twoje istniejące bazy NIE będą dotknięte!${NC}"
echo ""
read -p "Kontynuować? (tak/nie): " confirm
if [[ ! $confirm =~ ^[Tt]ak$ ]]; then
    echo "Anulowano."
    exit 0
fi
echo ""

# Utwórz nową bazę destiny_team
echo -e "${YELLOW}Krok 3: Tworzenie bazy 'destiny_team'...${NC}"
echo ""

docker exec -i $CONTAINER_NAME psql -U $POSTGRES_USER << 'EOF'
-- Próba utworzenia bazy (ignoruj błąd jeśli już istnieje)
SELECT 'CREATE DATABASE destiny_team'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'destiny_team')\gexec

-- Pokaż wszystkie bazy po utworzeniu
\l
EOF

echo ""
echo -e "${GREEN}✓ Baza 'destiny_team' gotowa!${NC}"
echo ""

# Connection string
CONN_STRING="dbname=destiny_team user=$POSTGRES_USER password=$POSTGRES_PASSWORD host=localhost port=$POSTGRES_PORT"

echo -e "${YELLOW}Krok 4: Zapisywanie konfiguracji...${NC}"
echo ""

# Zapisz do .env.postgres
cat > .env.postgres << EOF
# PostgreSQL Connection Configuration
# Wygenerowano: $(date)
# Kontener: $CONTAINER_NAME

POSTGRES_CONNECTION_STRING="$CONN_STRING"
POSTGRES_HOST=localhost
POSTGRES_PORT=$POSTGRES_PORT
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DATABASE=destiny_team
POSTGRES_CONTAINER=$CONTAINER_NAME
EOF

echo -e "${GREEN}✓ Konfiguracja zapisana w .env.postgres${NC}"
echo ""

# Utwórz helper do połączenia
cat > postgres_polacz.py << 'PYEOF'
#!/usr/bin/env python3
"""
Szybki test połączenia z PostgreSQL
"""
import os

def get_connection_string():
    """Wczytaj connection string z .env.postgres"""
    if os.path.exists('.env.postgres'):
        with open('.env.postgres', 'r') as f:
            for line in f:
                if line.startswith('POSTGRES_CONNECTION_STRING='):
                    return line.split('=', 1)[1].strip().strip('"')
    return None

def test():
    """Test połączenia"""
    from postgres_context_store import PostgresContextStore
    
    conn_string = get_connection_string()
    if not conn_string:
        print("❌ Nie znaleziono .env.postgres")
        return False
    
    print(f"Connection string: {conn_string}")
    print("\n🔌 Testowanie połączenia...")
    
    try:
        store = PostgresContextStore(conn_string)
        print("✅ Połączenie udane!")
        print("\n📊 Utworzone tabele:")
        
        with store.conn.cursor() as cur:
            cur.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                ORDER BY tablename;
            """)
            tables = cur.fetchall()
            
            if tables:
                for table in tables:
                    print(f"  ✓ {table[0]}")
            else:
                print("  (brak tabel - uruchom inicjalizację)")
        
        # Pokaż statystyki
        with store.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM messages;")
            msg_count = cur.fetchone()[0]
            print(f"\n📨 Wiadomości w bazie: {msg_count}")
        
        store.close()
        return True
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return False

if __name__ == "__main__":
    test()
PYEOF

chmod +x postgres_polacz.py

# Inicjalizuj schemat
echo -e "${YELLOW}Krok 5: Inicjalizacja schematu...${NC}"
echo ""

python3 << PYEOF
from postgres_context_store import PostgresContextStore

conn_string = "$CONN_STRING"
print("🗄️  Tworzenie tabel w bazie destiny_team...")
print("")

try:
    store = PostgresContextStore(conn_string)
    print("✅ Tabele utworzone pomyślnie!")
    print("")
    print("Utworzone tabele:")
    print("  - messages (komunikacja agentów)")
    print("  - agent_contexts (wiedza agentów)")
    print("  - projects (projekty)")
    print("  - agent_work_queue (zadania)")
    print("  - decisions (decyzje)")
    store.close()
except Exception as e:
    print(f"❌ Błąd: {e}")
    exit(1)
PYEOF

echo ""
echo "================================================"
echo -e "${GREEN}  ✅ INSTALACJA ZAKOŃCZONA!${NC}"
echo "================================================"
echo ""
echo -e "${GREEN}🎉 Twoje dane są bezpieczne!${NC}"
echo ""
echo -e "${BLUE}Struktura baz danych:${NC}"
echo ""
echo "  📁 Twoje istniejące bazy"
echo "  ├── postgres (nietknięta)"
echo "  ├── [inne twoje bazy] (nietknięte)"
echo "  └── destiny_team (NOWA - dla agentów)"
echo ""
echo "================================================"
echo ""
echo -e "${YELLOW}Następne kroki:${NC}"
echo ""
echo "1️⃣  Test połączenia:"
echo "   ${BLUE}python3 postgres_polacz.py${NC}"
echo ""
echo "2️⃣  Uruchom testy systemowe:"
echo "   ${BLUE}python3 test_postgres_context.py${NC}"
echo ""
echo "3️⃣  Zobacz demo wizualne:"
echo "   ${BLUE}python3 postgres_visual_example.py${NC}"
echo ""
echo "4️⃣  Użyj w swoim kodzie:"
echo '   from postgres_integration import DestinyTeamWithPostgres'
echo '   '
echo '   # Wczytaj connection string'
echo '   with open(".env.postgres") as f:'
echo '       for line in f:'
echo '           if "POSTGRES_CONNECTION_STRING" in line:'
echo '               conn = line.split("=", 1)[1].strip().strip("\"")'
echo '   '
echo '   # Utwórz team z nieograniczonym kontekstem'
echo '   team = DestinyTeamWithPostgres(conn)'
echo '   project_id = team.start_project("Mój Projekt", "Opis")'
echo ""
echo "================================================"
echo ""
echo -e "${GREEN}✨ Gotowe! Twoi agenci mają teraz nieograniczony kontekst! ✨${NC}"
echo ""
