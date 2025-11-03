#!/usr/bin/env python3
"""
Database Initialization Script for Destiny Team Framework
Creates all required tables and indexes

Author: Piotr Nowicki (DevOps Engineer)
Purpose: Prevent "relation does not exist" errors
"""

import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime


# SQL for creating events table
CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    importance FLOAT NOT NULL,
    made_by VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    additional_data JSONB
);
"""

CREATE_EVENTS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_events_project_id ON events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_made_by ON events(made_by);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_importance ON events(importance);
"""

# SQL for creating tasks table
CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    assigned_to VARCHAR(255),
    assigned_by VARCHAR(255),
    priority INTEGER DEFAULT 3,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    context JSONB
);
"""

CREATE_TASKS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
"""

# SQL for creating agent_metadata table
CREATE_AGENT_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS agent_metadata (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(255) NOT NULL,
    specialties TEXT[],
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    avg_completion_time FLOAT,
    last_active TIMESTAMP,
    status VARCHAR(50) DEFAULT 'idle',
    metadata JSONB
);
"""

CREATE_AGENT_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_agent_name ON agent_metadata(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_status ON agent_metadata(status);
"""


def check_postgresql_connection(conn_string):
    """Check if PostgreSQL is accessible"""
    try:
        conn = psycopg2.connect(conn_string)
        conn.close()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)


def create_tables(conn_string):
    """Create all required tables and indexes"""
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("📊 Creating tables...")
        
        # Create events table
        print("  - Creating events table...")
        cursor.execute(CREATE_EVENTS_TABLE)
        cursor.execute(CREATE_EVENTS_INDEXES)
        print("    ✅ events table created")
        
        # Create tasks table
        print("  - Creating tasks table...")
        cursor.execute(CREATE_TASKS_TABLE)
        cursor.execute(CREATE_TASKS_INDEXES)
        print("    ✅ tasks table created")
        
        # Create agent_metadata table
        print("  - Creating agent_metadata table...")
        cursor.execute(CREATE_AGENT_METADATA_TABLE)
        cursor.execute(CREATE_AGENT_INDEXES)
        print("    ✅ agent_metadata table created")
        
        conn.commit()
        
        # Verify tables exist
        print("\n🔍 Verifying tables...")
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('events', 'tasks', 'agent_metadata')
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table[0]}: {count} rows")
        
        cursor.close()
        conn.close()
        
        return True, "All tables created successfully"
        
    except Exception as e:
        return False, f"Error creating tables: {e}"


def seed_agent_metadata(conn_string):
    """Seed initial agent metadata"""
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("\n👥 Seeding agent metadata...")
        
        agents = [
            ("Tomasz Kamiński", "Senior Developer", ["Python", "Backend", "API", "Implementation"]),
            ("Anna Lewandowska", "QA Engineer", ["Testing", "Quality Assurance", "Test Automation"]),
            ("Magdalena Wiśniewska", "UX Designer", ["UI/UX", "Design", "User Experience"]),
            ("Michał Kowalczyk", "Software Architect", ["Architecture", "System Design", "Scalability"]),
            ("Katarzyna Zielińska", "Product Manager", ["Product", "Strategy", "Requirements"]),
            ("Piotr Nowicki", "DevOps Engineer", ["DevOps", "CI/CD", "Infrastructure", "Deployment"]),
            ("Joanna Mazur", "Data Scientist", ["Analytics", "Machine Learning", "Visualization"]),
            ("Dr. Joanna Kowalska", "Research Lead", ["Research", "Innovation", "Best Practices"]),
            ("Aleksander Nowak", "Technical Lead", ["Orchestration", "Leadership", "Coordination"])
        ]
        
        for name, role, specialties in agents:
            cursor.execute("""
                INSERT INTO agent_metadata (agent_name, role, specialties, status, last_active, metadata)
                VALUES (%s, %s, %s, 'idle', %s, %s)
                ON CONFLICT (agent_name) DO UPDATE
                SET role = EXCLUDED.role,
                    specialties = EXCLUDED.specialties
            """, (name, role, specialties, datetime.now(), '{}'))
            print(f"  ✅ {name} ({role})")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "Agent metadata seeded"
        
    except Exception as e:
        return False, f"Error seeding agents: {e}"


def main():
    """Main initialization function"""
    print("="*70)
    print("  🔧 DESTINY TEAM - DATABASE INITIALIZATION")
    print("="*70)
    print()
    
    # Default connection string
    conn_string = "dbname=destiny_team user=user password=password host=localhost port=5432"
    
    # Allow override from command line
    if len(sys.argv) > 1:
        conn_string = sys.argv[1]
    
    print(f"📡 Connection: {conn_string.split('password=')[0]}password=***")
    print()
    
    # Step 1: Check connection
    print("🔍 Step 1: Checking PostgreSQL connection...")
    success, message = check_postgresql_connection(conn_string)
    if not success:
        print(f"  ❌ Connection failed: {message}")
        print()
        print("Troubleshooting:")
        print("  1. Is PostgreSQL running? Check: docker ps | grep postgres")
        print("  2. Is the database created? Check: psql -l")
        print("  3. Are credentials correct?")
        print()
        print("Usage:")
        print(f"  python3 {sys.argv[0]} \"dbname=YOUR_DB user=YOUR_USER password=YOUR_PASS host=localhost\"")
        sys.exit(1)
    
    print(f"  ✅ {message}")
    print()
    
    # Step 2: Create tables
    print("🔧 Step 2: Creating tables and indexes...")
    success, message = create_tables(conn_string)
    if not success:
        print(f"  ❌ {message}")
        sys.exit(1)
    
    print(f"  ✅ {message}")
    print()
    
    # Step 3: Seed agents
    print("🌱 Step 3: Seeding initial data...")
    success, message = seed_agent_metadata(conn_string)
    if not success:
        print(f"  ⚠️  {message}")
        print("  (continuing anyway...)")
    else:
        print(f"  ✅ {message}")
    
    print()
    print("="*70)
    print("  ✅ DATABASE INITIALIZATION COMPLETE!")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Test: destiny memory stats")
    print("  2. Test: destiny memory health")
    print("  3. All should show 🟢 healthy!")
    print()


if __name__ == "__main__":
    main()
