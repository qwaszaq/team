"""
destiny-memory command implementation
Explore and analyze multi-layer memory system

Author: Joanna Mazur (Data Scientist)
Integrates: Helena's 4-database architecture
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

console = Console()
app = typer.Typer(help="Explore Destiny Team memory system")


def get_helena_core():
    """Initialize HelenaCore for database access"""
    try:
        from helena_core import HelenaCore
        helena = HelenaCore(
            project_id="destiny-team-framework-master"
        )
        return helena
    except Exception as e:
        console.print(f"[red]Error initializing HelenaCore: {e}[/red]")
        return None


# ============================================================================
# COMMAND: stats
# ============================================================================

@app.command()
def stats(
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Filter by project ID"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed statistics")
):
    """
    Show memory system statistics across all 4 databases
    
    Examples:
        destiny memory stats
        destiny memory stats --project destiny-team-master
        destiny memory stats --verbose
    """
    console.print("\n[bold cyan]🧠 DESTINY MEMORY SYSTEM - STATISTICS[/bold cyan]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    project_id = project or helena.project_id
    
    # Create main table
    table = Table(title=f"Project: {project_id}", show_header=True, header_style="bold magenta")
    table.add_column("Database", style="cyan", width=20)
    table.add_column("Status", style="green", width=12)
    table.add_column("Records", style="yellow", width=20)
    table.add_column("Details", style="blue", width=40)
    
    # Check PostgreSQL
    try:
        import psycopg2
        conn = psycopg2.connect(helena.postgres_conn)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events WHERE project_id = %s", (project_id,))
        event_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        table.add_row(
            "PostgreSQL",
            "🟢 Healthy",
            f"{event_count:,} events",
            "Structured event data"
        )
        pg_status = "✅"
    except Exception as e:
        table.add_row(
            "PostgreSQL",
            "🔴 Error",
            "N/A",
            f"Connection failed: {str(e)[:30]}"
        )
        pg_status = "❌"
    
    # Check Neo4j
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "exec", helena.neo4j_container, "cypher-shell",
             "-u", helena.neo4j_user, "-p", helena.neo4j_password,
             "MATCH (n) RETURN count(n) as count"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Parse output (simple parsing)
            node_count = "Unknown"
            for line in result.stdout.split('\n'):
                if line.strip().isdigit():
                    node_count = f"{int(line.strip()):,} nodes"
                    break
            
            table.add_row(
                "Neo4j",
                "🟢 Healthy",
                node_count,
                "Knowledge graph & relationships"
            )
            neo4j_status = "✅"
        else:
            table.add_row(
                "Neo4j",
                "🔴 Error",
                "N/A",
                "Query failed"
            )
            neo4j_status = "❌"
    except Exception as e:
        table.add_row(
            "Neo4j",
            "⚠️ Warning",
            "N/A",
            f"Not accessible: {str(e)[:30]}"
        )
        neo4j_status = "⚠️"
    
    # Check Qdrant
    try:
        import requests
        response = requests.get(f"{helena.qdrant_url}/collections/{project_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                points = data['result'].get('points_count', 0)
                vectors = data['result'].get('vectors_count', 0)
                
                table.add_row(
                    "Qdrant",
                    "🟢 Healthy",
                    f"{points:,} vectors",
                    "Semantic embeddings for search"
                )
                qdrant_status = "✅"
            else:
                table.add_row(
                    "Qdrant",
                    "⚠️ Warning",
                    "Collection not found",
                    f"No collection '{project_id}'"
                )
                qdrant_status = "⚠️"
        else:
            table.add_row(
                "Qdrant",
                "🔴 Error",
                "N/A",
                f"HTTP {response.status_code}"
            )
            qdrant_status = "❌"
    except Exception as e:
        table.add_row(
            "Qdrant",
            "⚠️ Warning",
            "N/A",
            f"Connection failed: {str(e)[:30]}"
        )
        qdrant_status = "⚠️"
    
    # Check Redis
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "exec", helena.redis_container, "redis-cli", "DBSIZE"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            key_count = result.stdout.strip().split()[-1]
            
            table.add_row(
                "Redis",
                "🟢 Healthy",
                f"{key_count} keys",
                "Fast cache & queues"
            )
            redis_status = "✅"
        else:
            table.add_row(
                "Redis",
                "🔴 Error",
                "N/A",
                "Command failed"
            )
            redis_status = "❌"
    except Exception as e:
        table.add_row(
            "Redis",
            "⚠️ Warning",
            "N/A",
            f"Not accessible: {str(e)[:30]}"
        )
        redis_status = "⚠️"
    
    console.print(table)
    
    # Overall health summary
    all_statuses = [pg_status, neo4j_status, qdrant_status, redis_status]
    healthy_count = all_statuses.count("✅")
    
    console.print()
    if healthy_count == 4:
        console.print(f"[bold green]✅ All 4 databases operational ({healthy_count}/4)[/bold green]")
    elif healthy_count >= 2:
        console.print(f"[bold yellow]⚠️ Partial operation ({healthy_count}/4 databases healthy)[/bold yellow]")
    else:
        console.print(f"[bold red]❌ System degraded ({healthy_count}/4 databases healthy)[/bold red]")
    
    console.print("\n[dim]💡 Tip: Use 'destiny memory search <term>' to query memories[/dim]\n")
    
    if verbose:
        console.print("\n[bold]Database Architecture:[/bold]")
        console.print("  • PostgreSQL: Structured events, task history")
        console.print("  • Neo4j: Knowledge graph, agent relationships")
        console.print("  • Qdrant: Semantic vectors for context search")
        console.print("  • Redis: Hot cache, real-time queues\n")


# ============================================================================
# COMMAND: search
# ============================================================================

@app.command()
def search(
    query: str = typer.Argument(..., help="Search term or phrase"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Filter by agent name"),
    limit: int = typer.Option(5, "--limit", "-n", help="Number of results"),
    threshold: float = typer.Option(0.6, "--threshold", "-t", help="Similarity threshold (0.0-1.0)")
):
    """
    Search memories using semantic similarity (Qdrant)
    
    Examples:
        destiny memory search "authentication bug"
        destiny memory search "login" --agent tomasz
        destiny memory search "architecture" --limit 10
    """
    console.print(f"\n[bold cyan]🔍 MEMORY SEARCH: '{query}'[/bold cyan]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    try:
        # Use Helena's search capability
        results = helena.load_context(query, limit=limit)
        
        if not results or "memories" not in results or not results["memories"]:
            console.print(f"[yellow]No memories found matching '{query}'[/yellow]")
            console.print("[dim]Try a different search term or lower threshold[/dim]\n")
            return
        
        memories = results["memories"]
        
        # Filter by agent if specified
        if agent:
            memories = [m for m in memories if agent.lower() in m.get("made_by", "").lower()]
        
        # Filter by threshold
        memories = [m for m in memories if m.get("score", 0) >= threshold]
        
        if not memories:
            console.print(f"[yellow]No memories found above threshold {threshold}[/yellow]")
            return
        
        console.print(f"[bold green]Found {len(memories)} relevant memories:[/bold green]\n")
        
        for i, memory in enumerate(memories[:limit], 1):
            score = memory.get("score", 0)
            made_by = memory.get("made_by", "Unknown")
            content = memory.get("content", "")
            event_type = memory.get("event_type", "unknown")
            timestamp = memory.get("timestamp", "")
            
            # Color code by relevance
            if score >= 0.9:
                relevance_label = "[bold green]🔥 Very relevant[/bold green]"
            elif score >= 0.75:
                relevance_label = "[green]✅ Relevant[/green]"
            elif score >= 0.6:
                relevance_label = "[yellow]⚠️ Somewhat relevant[/yellow]"
            else:
                relevance_label = "[dim]Low relevance[/dim]"
            
            panel = Panel(
                f"{content[:300]}{'...' if len(content) > 300 else ''}",
                title=f"#{i} [{made_by}] - {event_type.upper()}",
                subtitle=f"{relevance_label} (score: {score:.1%}) | {timestamp[:10] if timestamp else 'N/A'}",
                border_style="cyan" if score >= 0.75 else "dim"
            )
            console.print(panel)
        
        console.print(f"\n[dim]💡 Use --limit to see more results | Use --agent to filter by agent[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]Search failed: {e}[/red]")
        console.print("[yellow]⚠️ Make sure Qdrant is running and collection exists[/yellow]\n")


# ============================================================================
# COMMAND: agent
# ============================================================================

@app.command()
def agent(
    agent_name: str = typer.Argument(..., help="Agent name (e.g., tomasz, anna)"),
    last_days: int = typer.Option(30, "--last-days", "-d", help="Show memories from last N days"),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of memories to show")
):
    """
    Show memories for a specific agent
    
    Examples:
        destiny memory agent tomasz
        destiny memory agent anna --last-days 7
        destiny memory agent michal --limit 20
    """
    console.print(f"\n[bold cyan]🤖 AGENT MEMORIES: {agent_name.upper()}[/bold cyan]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    try:
        import psycopg2
        conn = psycopg2.connect(helena.postgres_conn)
        cursor = conn.cursor()
        
        # Query agent's recent events
        cutoff_date = datetime.now() - timedelta(days=last_days)
        
        cursor.execute("""
            SELECT event_type, content, importance, timestamp, additional_data
            FROM events
            WHERE made_by ILIKE %s
              AND timestamp >= %s
              AND project_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """, (f"%{agent_name}%", cutoff_date, helena.project_id, limit))
        
        memories = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not memories:
            console.print(f"[yellow]No memories found for '{agent_name}' in last {last_days} days[/yellow]")
            console.print("[dim]Try increasing --last-days or check agent name[/dim]\n")
            return
        
        # Display agent info header
        console.print(f"[bold]Agent:[/bold] {agent_name.title()}")
        console.print(f"[bold]Period:[/bold] Last {last_days} days")
        console.print(f"[bold]Memories:[/bold] {len(memories)}\n")
        
        # Create table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Type", style="green", width=15)
        table.add_column("Content", style="yellow", width=60)
        table.add_column("Importance", style="red", width=10)
        
        for event_type, content, importance, timestamp, _ in memories:
            # Truncate content
            content_short = content[:57] + "..." if len(content) > 60 else content
            
            # Format importance
            imp_str = f"{importance:.1f}"
            if importance >= 0.8:
                imp_str = f"[red]{imp_str}[/red] 🔥"
            elif importance >= 0.6:
                imp_str = f"[yellow]{imp_str}[/yellow]"
            else:
                imp_str = f"[dim]{imp_str}[/dim]"
            
            table.add_row(
                timestamp.strftime("%Y-%m-%d"),
                event_type,
                content_short,
                imp_str
            )
        
        console.print(table)
        console.print(f"\n[dim]💡 Use --last-days to change period | Use --limit for more results[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]Failed to fetch agent memories: {e}[/red]")
        console.print("[yellow]⚠️ Make sure PostgreSQL is running and configured[/yellow]\n")


# ============================================================================
# COMMAND: relationships
# ============================================================================

@app.command()
def relationships(
    agent_name: Optional[str] = typer.Option(None, "--agent", "-a", help="Show relationships for specific agent"),
    depth: int = typer.Option(1, "--depth", "-d", help="Relationship depth (1-3)")
):
    """
    Explore agent collaboration relationships (Neo4j graph)
    
    Examples:
        destiny memory relationships
        destiny memory relationships --agent tomasz
        destiny memory relationships --agent anna --depth 2
    """
    console.print("\n[bold cyan]🕸️ AGENT COLLABORATION NETWORK[/bold cyan]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    try:
        import subprocess
        
        if agent_name:
            # Query specific agent relationships
            query = f"""
            MATCH (a:Agent {{name: '{agent_name.title()}'}})-[r]->(b)
            RETURN a.name as from, type(r) as relationship, b.name as to, r.count as count
            ORDER BY r.count DESC
            LIMIT 20
            """
        else:
            # Query all relationships
            query = """
            MATCH (a:Agent)-[r]->(b:Agent)
            RETURN a.name as from, type(r) as relationship, b.name as to, r.count as count
            ORDER BY r.count DESC
            LIMIT 30
            """
        
        result = subprocess.run(
            ["docker", "exec", helena.neo4j_container, "cypher-shell",
             "-u", helena.neo4j_user, "-p", helena.neo4j_password,
             query],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode != 0:
            console.print(f"[red]Neo4j query failed[/red]")
            console.print("[yellow]⚠️ Make sure Neo4j is running[/yellow]\n")
            return
        
        # Parse output (simple parsing - in production, use proper driver)
        lines = result.stdout.strip().split('\n')
        
        if len(lines) < 3:
            console.print(f"[yellow]No relationships found{' for ' + agent_name if agent_name else ''}[/yellow]")
            console.print("[dim]Try running some agent tasks to build relationships[/dim]\n")
            return
        
        # Create visualization
        if agent_name:
            console.print(f"[bold]Agent:[/bold] {agent_name.title()}\n")
        
        # Build tree structure
        tree = Tree(f"🕸️ [bold cyan]Collaboration Network[/bold cyan]")
        
        # Parse relationships (skip header and footer)
        relationships = {}
        for line in lines[1:-1]:  # Skip first (header) and last (summary)
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    from_agent = parts[0].strip('"')
                    rel_type = parts[1].strip('"')
                    to_agent = parts[2].strip('"')
                    count = parts[3].strip('"')
                    
                    if from_agent not in relationships:
                        relationships[from_agent] = []
                    relationships[from_agent].append((rel_type, to_agent, count))
        
        # Build tree
        for from_agent, rels in list(relationships.items())[:10]:  # Limit to 10 agents
            agent_branch = tree.add(f"[bold cyan]{from_agent}[/bold cyan]")
            for rel_type, to_agent, count in rels[:5]:  # Top 5 relationships per agent
                agent_branch.add(f"[green]─[{rel_type}]→[/green] {to_agent} [dim]({count} times)[/dim]")
        
        console.print(tree)
        
        console.print(f"\n[bold green]✅ Showing collaboration patterns[/bold green]")
        console.print("[dim]💡 These relationships show how agents work together[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]Failed to query relationships: {e}[/red]")
        console.print("[yellow]⚠️ Make sure Neo4j container is running and accessible[/yellow]\n")


# ============================================================================
# COMMAND: health
# ============================================================================

@app.command()
def health(
    check_all: bool = typer.Option(False, "--check-all", help="Run detailed health checks"),
    fix: bool = typer.Option(False, "--fix", help="Attempt to fix common issues")
):
    """
    Check health of all 4 databases
    
    Examples:
        destiny memory health
        destiny memory health --check-all
        destiny memory health --fix
    """
    console.print("\n[bold cyan]🏥 MEMORY SYSTEM HEALTH CHECK[/bold cyan]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    issues = []
    warnings = []
    
    # Check 1: PostgreSQL
    console.print("[bold]1. PostgreSQL[/bold] (Structured Events)")
    try:
        import psycopg2
        conn = psycopg2.connect(helena.postgres_conn)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM events;")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        console.print(f"   [green]✅ Connected[/green]")
        console.print(f"   [dim]Events: {count:,} | Version: {version[:30]}...[/dim]")
    except Exception as e:
        console.print(f"   [red]❌ Failed: {e}[/red]")
        issues.append(("PostgreSQL", str(e)))
    
    console.print()
    
    # Check 2: Neo4j
    console.print("[bold]2. Neo4j[/bold] (Knowledge Graph)")
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "exec", helena.neo4j_container, "cypher-shell",
             "-u", helena.neo4j_user, "-p", helena.neo4j_password,
             "RETURN 'OK' as status"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            console.print(f"   [green]✅ Connected[/green]")
            console.print(f"   [dim]Container: {helena.neo4j_container}[/dim]")
        else:
            console.print(f"   [red]❌ Query failed[/red]")
            issues.append(("Neo4j", "Query execution failed"))
    except Exception as e:
        console.print(f"   [yellow]⚠️ Warning: {e}[/yellow]")
        warnings.append(("Neo4j", str(e)))
    
    console.print()
    
    # Check 3: Qdrant
    console.print("[bold]3. Qdrant[/bold] (Semantic Vectors)")
    try:
        import requests
        response = requests.get(f"{helena.qdrant_url}/collections", timeout=5)
        if response.status_code == 200:
            collections = response.json().get('result', {}).get('collections', [])
            console.print(f"   [green]✅ Connected[/green]")
            console.print(f"   [dim]Collections: {len(collections)}[/dim]")
            
            # Check if project collection exists
            project_exists = any(c['name'] == helena.project_id for c in collections)
            if not project_exists:
                console.print(f"   [yellow]⚠️ Warning: Collection '{helena.project_id}' not found[/yellow]")
                warnings.append(("Qdrant", f"Missing collection '{helena.project_id}'"))
        else:
            console.print(f"   [red]❌ HTTP {response.status_code}[/red]")
            issues.append(("Qdrant", f"HTTP error {response.status_code}"))
    except Exception as e:
        console.print(f"   [yellow]⚠️ Warning: {e}[/yellow]")
        warnings.append(("Qdrant", str(e)))
    
    console.print()
    
    # Check 4: Redis
    console.print("[bold]4. Redis[/bold] (Fast Cache)")
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "exec", helena.redis_container, "redis-cli", "PING"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and "PONG" in result.stdout:
            console.print(f"   [green]✅ Connected[/green]")
            console.print(f"   [dim]Container: {helena.redis_container}[/dim]")
        else:
            console.print(f"   [red]❌ Ping failed[/red]")
            issues.append(("Redis", "Ping failed"))
    except Exception as e:
        console.print(f"   [yellow]⚠️ Warning: {e}[/yellow]")
        warnings.append(("Redis", str(e)))
    
    console.print()
    console.print("="*80)
    console.print()
    
    # Summary
    if not issues and not warnings:
        console.print("[bold green]✅ ALL SYSTEMS HEALTHY[/bold green]")
        console.print("[dim]All 4 databases are operational[/dim]\n")
    elif not issues:
        console.print(f"[bold yellow]⚠️ {len(warnings)} WARNING(S)[/bold yellow]")
        for db, msg in warnings:
            console.print(f"   • {db}: {msg}")
        console.print()
    else:
        console.print(f"[bold red]❌ {len(issues)} CRITICAL ISSUE(S)[/bold red]")
        for db, msg in issues:
            console.print(f"   • {db}: {msg}")
        if warnings:
            console.print(f"\n[yellow]{len(warnings)} warning(s):[/yellow]")
            for db, msg in warnings:
                console.print(f"   • {db}: {msg}")
        console.print()
    
    if fix and (issues or warnings):
        console.print("[bold]🔧 Attempting automatic fixes...[/bold]")
        console.print("[dim](Not implemented yet - manual fixes required)[/dim]\n")


# ============================================================================
# COMMAND: cleanup
# ============================================================================

@app.command()
def cleanup(
    older_than_days: int = typer.Option(90, "--older-than", help="Delete memories older than N days"),
    project: Optional[str] = typer.Option(None, "--project", help="Project ID to clean up"),
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="Show what would be deleted"),
    confirm: bool = typer.Option(False, "--confirm", "-y", help="Skip confirmation prompt")
):
    """
    Clean up old memories (DESTRUCTIVE - use with caution!)
    
    Examples:
        destiny memory cleanup --older-than 90 --dry-run
        destiny memory cleanup --project test-* --dry-run
        destiny memory cleanup --older-than 180 --execute --confirm
    """
    console.print("\n[bold red]⚠️ MEMORY CLEANUP (DESTRUCTIVE OPERATION)[/bold red]\n")
    
    helena = get_helena_core()
    if not helena:
        return
    
    project_id = project or helena.project_id
    cutoff_date = datetime.now() - timedelta(days=older_than_days)
    
    console.print(f"[bold]Target:[/bold] Memories older than {cutoff_date.strftime('%Y-%m-%d')}")
    console.print(f"[bold]Project:[/bold] {project_id}")
    console.print(f"[bold]Mode:[/bold] {'DRY RUN (no changes)' if dry_run else 'EXECUTE (will delete!)'}\n")
    
    if not dry_run and not confirm:
        proceed = typer.confirm("⚠️ This will permanently delete data. Continue?")
        if not proceed:
            console.print("[yellow]Cancelled[/yellow]\n")
            return
    
    try:
        import psycopg2
        conn = psycopg2.connect(helena.postgres_conn)
        cursor = conn.cursor()
        
        # Count affected records
        cursor.execute("""
            SELECT COUNT(*) FROM events
            WHERE timestamp < %s AND project_id = %s
        """, (cutoff_date, project_id))
        
        count = cursor.fetchone()[0]
        
        console.print(f"[yellow]Found {count:,} memories to clean up[/yellow]\n")
        
        if count == 0:
            console.print("[green]Nothing to clean up[/green]\n")
            cursor.close()
            conn.close()
            return
        
        if dry_run:
            console.print("[bold green]✅ DRY RUN COMPLETE[/bold green]")
            console.print("[dim]Run with --execute to actually delete these memories[/dim]\n")
        else:
            # Execute deletion
            cursor.execute("""
                DELETE FROM events
                WHERE timestamp < %s AND project_id = %s
            """, (cutoff_date, project_id))
            
            conn.commit()
            deleted = cursor.rowcount
            
            console.print(f"[bold green]✅ Deleted {deleted:,} memories[/bold green]\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        console.print(f"[red]Cleanup failed: {e}[/red]\n")


# ============================================================================
# Main entry point (for testing)
# ============================================================================

def memory_command():
    """Entry point for the memory command group"""
    app()


if __name__ == "__main__":
    app()
