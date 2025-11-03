"""
destiny-setup command implementation
Initialize and verify Destiny Team Framework setup

Author: Piotr Nowicki (DevOps Engineer)
Purpose: Make installation bulletproof
"""

import typer
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
app = typer.Typer(help="Setup and verify Destiny Team Framework")

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


@app.command()
def init(
    connection: str = typer.Option(
        "dbname=destiny_team user=user password=password host=localhost port=5432",
        "--connection", "-c",
        help="PostgreSQL connection string"
    )
):
    """
    Initialize all database tables and indexes
    
    This creates:
    - events table (for memory system)
    - tasks table (for task management)
    - agent_metadata table (for agent tracking)
    
    Examples:
        destiny setup init
        destiny setup init --connection "dbname=mydb user=myuser password=mypass"
    """
    console.print("\n[bold cyan]🔧 Initializing Destiny Team Database[/bold cyan]\n")
    
    # Find init_database.py
    script_path = Path(__file__).parent.parent.parent.parent / "init_database.py"
    
    if not script_path.exists():
        console.print("[red]❌ Error: init_database.py not found![/red]")
        console.print(f"[dim]Expected location: {script_path}[/dim]\n")
        return
    
    # Run initialization
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), connection],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Show output
        console.print(result.stdout)
        
        if result.returncode == 0:
            console.print("[bold green]✅ Database initialized successfully![/bold green]\n")
        else:
            console.print("[bold red]❌ Initialization failed![/bold red]")
            if result.stderr:
                console.print(f"[red]{result.stderr}[/red]\n")
            
    except subprocess.TimeoutExpired:
        console.print("[red]❌ Initialization timed out (>30s)[/red]\n")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]\n")


@app.command()
def check():
    """
    Verify Destiny Team Framework setup
    
    Checks:
    - PostgreSQL connection and tables
    - Neo4j connectivity
    - Qdrant collections
    - Redis connectivity
    - CLI tools availability
    
    Examples:
        destiny setup check
    """
    console.print("\n[bold cyan]🔍 Checking Destiny Team Setup[/bold cyan]\n")
    
    issues = []
    warnings = []
    
    # Check 1: CLI tools
    console.print("[bold]1. CLI Tools[/bold]")
    try:
        # Check if destiny command works
        result = subprocess.run(
            ["destiny", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            console.print("   [green]✅ destiny CLI installed[/green]")
        else:
            console.print("   [red]❌ destiny CLI not working[/red]")
            issues.append("CLI not functioning properly")
    except FileNotFoundError:
        console.print("   [red]❌ destiny command not found[/red]")
        issues.append("destiny CLI not installed")
    except Exception as e:
        console.print(f"   [yellow]⚠️  Could not check CLI: {e}[/yellow]")
        warnings.append("CLI check failed")
    
    console.print()
    
    # Check 2: PostgreSQL
    console.print("[bold]2. PostgreSQL[/bold]")
    try:
        import psycopg2
        conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost port=5432")
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('events', 'tasks', 'agent_metadata')
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['events', 'tasks', 'agent_metadata']
        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                console.print(f"   [green]✅ {table} table exists ({count} rows)[/green]")
            else:
                console.print(f"   [red]❌ {table} table missing[/red]")
                issues.append(f"PostgreSQL: {table} table not created")
        
        cursor.close()
        conn.close()
        
    except ImportError:
        console.print("   [red]❌ psycopg2 not installed[/red]")
        issues.append("psycopg2 module missing")
    except Exception as e:
        console.print(f"   [red]❌ Connection failed: {e}[/red]")
        issues.append("PostgreSQL not accessible")
    
    console.print()
    
    # Check 3: Neo4j
    console.print("[bold]3. Neo4j[/bold]")
    try:
        result = subprocess.run(
            ["docker", "exec", "sms-neo4j", "cypher-shell",
             "-u", "neo4j", "-p", "password",
             "RETURN 'OK' as status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            console.print("   [green]✅ Neo4j accessible[/green]")
        else:
            console.print("   [yellow]⚠️  Neo4j query failed[/yellow]")
            warnings.append("Neo4j not responding")
    except Exception as e:
        console.print(f"   [yellow]⚠️  Neo4j not accessible: {str(e)[:50]}[/yellow]")
        warnings.append("Neo4j not available")
    
    console.print()
    
    # Check 4: Qdrant
    console.print("[bold]4. Qdrant[/bold]")
    try:
        import requests
        response = requests.get("http://localhost:6333/collections", timeout=5)
        if response.status_code == 200:
            collections = response.json().get('result', {}).get('collections', [])
            console.print(f"   [green]✅ Qdrant accessible ({len(collections)} collections)[/green]")
        else:
            console.print(f"   [yellow]⚠️  Qdrant HTTP {response.status_code}[/yellow]")
            warnings.append("Qdrant not responding")
    except ImportError:
        console.print("   [red]❌ requests module not installed[/red]")
        issues.append("requests module missing")
    except Exception as e:
        console.print(f"   [yellow]⚠️  Qdrant not accessible: {str(e)[:50]}[/yellow]")
        warnings.append("Qdrant not available")
    
    console.print()
    
    # Check 5: Redis
    console.print("[bold]5. Redis[/bold]")
    try:
        result = subprocess.run(
            ["docker", "exec", "kg-redis", "redis-cli", "PING"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and "PONG" in result.stdout:
            console.print("   [green]✅ Redis accessible[/green]")
        else:
            console.print("   [yellow]⚠️  Redis ping failed[/yellow]")
            warnings.append("Redis not responding")
    except Exception as e:
        console.print(f"   [yellow]⚠️  Redis not accessible: {str(e)[:50]}[/yellow]")
        warnings.append("Redis not available")
    
    console.print()
    console.print("="*70)
    console.print()
    
    # Summary
    if not issues and not warnings:
        console.print("[bold green]✅ ALL CHECKS PASSED![/bold green]")
        console.print("[dim]Your Destiny Team installation is ready to use.[/dim]\n")
    elif not issues:
        console.print(f"[bold yellow]⚠️  {len(warnings)} WARNING(S)[/bold yellow]")
        for w in warnings:
            console.print(f"   • {w}")
        console.print("\n[dim]System functional but some components unavailable.[/dim]\n")
    else:
        console.print(f"[bold red]❌ {len(issues)} CRITICAL ISSUE(S)[/bold red]")
        for i in issues:
            console.print(f"   • {i}")
        if warnings:
            console.print(f"\n[yellow]{len(warnings)} warning(s):[/yellow]")
            for w in warnings:
                console.print(f"   • {w}")
        console.print("\n[bold]Recommended fix:[/bold]")
        console.print("  destiny setup init")
        console.print()


@app.command()
def doctor():
    """
    Comprehensive health check with fix suggestions
    
    This is like 'destiny setup check' but with more detailed
    diagnostics and actionable fix recommendations.
    
    Examples:
        destiny setup doctor
    """
    console.print("\n[bold cyan]🏥 Destiny Team Health Check[/bold cyan]\n")
    
    # Run the check
    check()
    
    # Provide fix suggestions
    console.print("[bold]💡 Common Fixes:[/bold]\n")
    
    panel = Panel(
        """[bold]Issue: PostgreSQL tables missing[/bold]
→ Run: destiny setup init

[bold]Issue: Database connection failed[/bold]
→ Check: docker ps | grep postgres
→ Start: docker start your-postgres-container

[bold]Issue: CLI not working[/bold]
→ Reinstall: pip install -e .
→ Verify: which destiny

[bold]Issue: Dependencies missing[/bold]
→ Install: pip install -r requirements.txt

[bold]Issue: Neo4j/Qdrant/Redis down[/bold]
→ These are optional but recommended
→ Check containers: docker ps
""",
        title="Troubleshooting Guide",
        border_style="cyan"
    )
    
    console.print(panel)
    console.print()


def setup_command():
    """Entry point for the setup command group"""
    app()


if __name__ == "__main__":
    app()
