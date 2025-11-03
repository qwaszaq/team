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
