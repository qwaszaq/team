#!/bin/bash
# Setup script for Docker PostgreSQL

echo "================================================"
echo "  PostgreSQL Setup for Destiny Team (Docker)"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Krok 1: Sprawdzanie kontenera PostgreSQL...${NC}"
echo ""

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo -e "${RED}❌ Docker nie jest uruchomiony${NC}"
    echo "Uruchom Docker Desktop i spróbuj ponownie"
    exit 1
fi

# Find PostgreSQL container
POSTGRES_CONTAINER=$(docker ps --filter "ancestor=postgres" --format "{{.Names}}" | head -n 1)

if [ -z "$POSTGRES_CONTAINER" ]; then
    # Try to find any container with postgres in name
    POSTGRES_CONTAINER=$(docker ps --format "{{.Names}}" | grep -i postgres | head -n 1)
fi

if [ -z "$POSTGRES_CONTAINER" ]; then
    echo -e "${RED}❌ Nie znaleziono kontenera PostgreSQL${NC}"
    echo ""
    echo "Dostępne kontenery:"
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
    echo ""
    read -p "Podaj nazwę kontenera PostgreSQL: " POSTGRES_CONTAINER
fi

echo -e "${GREEN}✓ Znaleziono kontener: $POSTGRES_CONTAINER${NC}"
echo ""

# Get connection details
echo -e "${YELLOW}Krok 2: Pobieranie szczegółów połączenia...${NC}"
echo ""

# Try to get port
POSTGRES_PORT=$(docker port $POSTGRES_CONTAINER 5432 2>/dev/null | cut -d':' -f2)
if [ -z "$POSTGRES_PORT" ]; then
    POSTGRES_PORT="5432"
fi

echo "Port PostgreSQL: $POSTGRES_PORT"
echo ""

# Get PostgreSQL user (usually postgres)
echo "Domyślny użytkownik to zazwyczaj 'postgres'"
read -p "Podaj użytkownika PostgreSQL (Enter = postgres): " POSTGRES_USER
POSTGRES_USER=${POSTGRES_USER:-postgres}

# Get password if needed
read -sp "Podaj hasło PostgreSQL (Enter jeśli brak): " POSTGRES_PASSWORD
echo ""
echo ""

# Build connection string
if [ -z "$POSTGRES_PASSWORD" ]; then
    CONN_STRING="dbname=destiny_team user=$POSTGRES_USER host=localhost port=$POSTGRES_PORT"
else
    CONN_STRING="dbname=destiny_team user=$POSTGRES_USER password=$POSTGRES_PASSWORD host=localhost port=$POSTGRES_PORT"
fi

echo -e "${YELLOW}Krok 3: Tworzenie nowej bazy danych 'destiny_team'...${NC}"
echo ""
echo -e "${GREEN}To NIE wpłynie na Twoje istniejące bazy!${NC}"
echo ""

# Create database
if [ -z "$POSTGRES_PASSWORD" ]; then
    docker exec -it $POSTGRES_CONTAINER psql -U $POSTGRES_USER -c "CREATE DATABASE destiny_team;" 2>&1 | grep -v "already exists"
else
    docker exec -it $POSTGRES_CONTAINER bash -c "PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -c 'CREATE DATABASE destiny_team;'" 2>&1 | grep -v "already exists"
fi

echo -e "${GREEN}✓ Baza 'destiny_team' gotowa${NC}"
echo ""

# List all databases to show isolation
echo -e "${YELLOW}Krok 4: Lista wszystkich baz danych (dla weryfikacji):${NC}"
echo ""

if [ -z "$POSTGRES_PASSWORD" ]; then
    docker exec -it $POSTGRES_CONTAINER psql -U $POSTGRES_USER -c "\l" | grep -E "Name|---|destiny_team|$(echo $POSTGRES_USER | head -c 10)"
else
    docker exec -it $POSTGRES_CONTAINER bash -c "PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -c '\l'" | grep -E "Name|---|destiny_team"
fi

echo ""
echo -e "${GREEN}✓ Jak widzisz, Twoje istniejące bazy są nietknięte!${NC}"
echo ""

# Save connection string to file
echo -e "${YELLOW}Krok 5: Zapisywanie konfiguracji...${NC}"
echo ""

cat > .env.postgres << EOF
# PostgreSQL Connection Configuration
# Generated: $(date)

POSTGRES_CONNECTION_STRING="$CONN_STRING"
POSTGRES_HOST=localhost
POSTGRES_PORT=$POSTGRES_PORT
POSTGRES_USER=$POSTGRES_USER
POSTGRES_DATABASE=destiny_team
EOF

echo -e "${GREEN}✓ Konfiguracja zapisana w .env.postgres${NC}"
echo ""

# Create Python connection example
cat > postgres_connect.py << 'EOF'
"""
Quick connection test for Docker PostgreSQL
"""
import os

# Read connection string from .env.postgres
def get_connection_string():
    if os.path.exists('.env.postgres'):
        with open('.env.postgres', 'r') as f:
            for line in f:
                if line.startswith('POSTGRES_CONNECTION_STRING='):
                    return line.split('=', 1)[1].strip().strip('"')
    
    # Fallback
    return "dbname=destiny_team user=postgres host=localhost port=5432"

# Test connection
def test_connection():
    from postgres_context_store import PostgresContextStore
    
    conn_string = get_connection_string()
    print(f"Connection string: {conn_string}")
    print("\nTesting connection...")
    
    try:
        store = PostgresContextStore(conn_string)
        print("✅ Połączenie udane!")
        print("\nTabele utworzone:")
        
        with store.conn.cursor() as cur:
            cur.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                ORDER BY tablename;
            """)
            tables = cur.fetchall()
            for table in tables:
                print(f"  - {table[0]}")
        
        store.close()
        return True
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return False

if __name__ == "__main__":
    test_connection()
EOF

chmod +x postgres_connect.py

echo -e "${YELLOW}Krok 6: Inicjalizacja schematu...${NC}"
echo ""

# Initialize schema
python3 - << EOF
from postgres_context_store import PostgresContextStore

conn_string = "$CONN_STRING"
print(f"Tworzenie tabel w bazie destiny_team...")

try:
    store = PostgresContextStore(conn_string)
    print("✅ Schema utworzona pomyślnie!")
    store.close()
except Exception as e:
    print(f"❌ Błąd: {e}")
EOF

echo ""
echo "================================================"
echo -e "${GREEN}  ✅ INSTALACJA ZAKOŃCZONA!${NC}"
echo "================================================"
echo ""
echo -e "${GREEN}Twoje dane są bezpieczne!${NC}"
echo ""
echo "Następne kroki:"
echo ""
echo "1. Test połączenia:"
echo "   python3 postgres_connect.py"
echo ""
echo "2. Uruchom testy:"
echo "   python3 test_postgres_context.py"
echo ""
echo "3. Użyj w kodzie:"
cat << 'PYEOF'
   from postgres_integration import DestinyTeamWithPostgres
   
   # Wczytaj connection string
   with open('.env.postgres') as f:
       for line in f:
           if line.startswith('POSTGRES_CONNECTION_STRING='):
               conn = line.split('=', 1)[1].strip().strip('"')
   
   team = DestinyTeamWithPostgres(conn)
PYEOF
echo ""
echo "================================================"
echo ""
