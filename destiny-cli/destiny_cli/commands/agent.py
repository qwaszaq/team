"""
destiny-agent command implementation
Manage and monitor Destiny Team agents

Author: Piotr Nowicki (DevOps Engineer)
Purpose: Agent management and coordination
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

console = Console()
app = typer.Typer(help="Manage Destiny Team agents")


def get_agent_registry():
    """Get all available agents"""
    try:
        # Import all agent classes
        from agents.specialized.tomasz_agent import TomaszAgent
        from agents.specialized.anna_agent import AnnaAgent
        from agents.specialized.magdalena_agent import MagdalenaAgent
        from agents.specialized.michal_agent import MichalAgent
        from agents.specialized.katarzyna_agent import KatarzynaAgent
        from agents.specialized.piotr_agent import PiotrAgent
        from agents.specialized.joanna_agent import JoannaAgent
        from agents.specialized.dr_joanna_agent import DrJoannaAgent
        from agents.specialized.aleksander_agent import AleksanderAgent
        
        agents = [
            ("tomasz", TomaszAgent, "Tomasz Kamiński", "Senior Developer"),
            ("anna", AnnaAgent, "Anna Lewandowska", "QA Engineer"),
            ("magdalena", MagdalenaAgent, "Magdalena Wiśniewska", "UX Designer"),
            ("michal", MichalAgent, "Michał Kowalczyk", "Software Architect"),
            ("katarzyna", KatarzynaAgent, "Katarzyna Zielińska", "Product Manager"),
            ("piotr", PiotrAgent, "Piotr Nowicki", "DevOps Engineer"),
            ("joanna", JoannaAgent, "Joanna Mazur", "Data Scientist"),
            ("dr_joanna", DrJoannaAgent, "Dr. Joanna Kowalska", "Research Lead"),
            ("aleksander", AleksanderAgent, "Aleksander Nowak", "Technical Lead")
        ]
        
        return agents
    except Exception as e:
        console.print(f"[red]Error loading agents: {e}[/red]")
        return []


def get_agent_metadata_from_db():
    """Get agent metadata from PostgreSQL"""
    try:
        import psycopg2
        conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost port=5432")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_name, role, specialties, total_tasks, completed_tasks,
                   failed_tasks, avg_completion_time, last_active, status
            FROM agent_metadata
            ORDER BY agent_name;
        """)
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return rows
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not load from database: {e}[/yellow]")
        return []


# ============================================================================
# COMMAND: list
# ============================================================================

@app.command()
def list(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Filter by role (developer, qa, ux, etc.)"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (idle, busy, error)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information")
):
    """
    List all Destiny Team agents
    
    Examples:
        destiny agent list
        destiny agent list --role developer
        destiny agent list --status idle
        destiny agent list --verbose
    """
    console.print("\n[bold cyan]🤖 DESTINY TEAM AGENTS[/bold cyan]\n")
    
    agents = get_agent_registry()
    
    if not agents:
        console.print("[red]No agents found![/red]\n")
        return
    
    # Filter by role if specified
    if role:
        agents = [a for a in agents if role.lower() in a[3].lower()]
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=15)
    table.add_column("Name", style="green", width=25)
    table.add_column("Role", style="yellow", width=20)
    table.add_column("Status", style="blue", width=12)
    
    if verbose:
        table.add_column("Tasks", style="white", width=10)
        table.add_column("Success Rate", style="white", width=12)
    
    # Try to get metadata from DB
    db_metadata = {}
    for row in get_agent_metadata_from_db():
        name, role_db, specs, total, completed, failed, avg_time, last_active, status_db = row
        db_metadata[name] = {
            'total': total or 0,
            'completed': completed or 0,
            'failed': failed or 0,
            'status': status_db or 'idle'
        }
    
    # Add rows
    for agent_id, agent_class, name, role_text in agents:
        # Get status from DB or default
        agent_status = db_metadata.get(name, {}).get('status', 'idle')
        
        # Filter by status if specified
        if status and status.lower() != agent_status.lower():
            continue
        
        # Status icon
        if agent_status == 'idle':
            status_display = "🟢 Idle"
        elif agent_status == 'busy':
            status_display = "🔴 Busy"
        else:
            status_display = "⚪ Unknown"
        
        if verbose and name in db_metadata:
            meta = db_metadata[name]
            total_tasks = meta['total']
            completed_tasks = meta['completed']
            success_rate = f"{(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "N/A"
            
            table.add_row(
                agent_id,
                name,
                role_text,
                status_display,
                str(total_tasks),
                success_rate
            )
        else:
            table.add_row(agent_id, name, role_text, status_display)
    
    console.print(table)
    
    # Summary
    total_agents = len([a for a in agents if not status or status.lower() == db_metadata.get(a[2], {}).get('status', 'idle').lower()])
    console.print(f"\n[bold green]✅ {total_agents} agent(s) shown[/bold green]")
    console.print("[dim]Use --verbose for detailed information[/dim]\n")


# ============================================================================
# COMMAND: info
# ============================================================================

@app.command()
def info(
    agent_id: str = typer.Argument(..., help="Agent ID (e.g., tomasz, anna, michal)"),
    show_history: bool = typer.Option(False, "--history", "-h", help="Show task history")
):
    """
    Show detailed information about a specific agent
    
    Examples:
        destiny agent info tomasz
        destiny agent info anna --history
    """
    console.print(f"\n[bold cyan]🤖 AGENT INFORMATION[/bold cyan]\n")
    
    agents = get_agent_registry()
    agent_data = None
    
    # Find agent
    for aid, aclass, name, role in agents:
        if aid == agent_id.lower():
            agent_data = (aid, aclass, name, role)
            break
    
    if not agent_data:
        console.print(f"[red]❌ Agent '{agent_id}' not found![/red]")
        console.print(f"[dim]Available agents: {', '.join([a[0] for a in agents])}[/dim]\n")
        return
    
    aid, aclass, name, role = agent_data
    
    # Create agent instance to get details
    try:
        agent = aclass()
        
        # Get specialization from agent
        specialty_str = agent.specialization if hasattr(agent, 'specialization') else agent.role
        
        # Display basic info
        panel = Panel(
            f"""[bold]Name:[/bold] {agent.name}
[bold]Role:[/bold] {agent.role}
[bold]Status:[/bold] 🟢 Available
[bold]Specialties:[/bold] {specialty_str}

[dim]Agent class: {aclass.__name__}[/dim]
[dim]Module: {aclass.__module__}[/dim]""",
            title=f"[bold green]{name}[/bold green]",
            border_style="cyan"
        )
        
        console.print(panel)
        
        # Get metadata from DB if available
        db_rows = get_agent_metadata_from_db()
        agent_meta = None
        for row in db_rows:
            if row[0] == name:
                agent_meta = row
                break
        
        if agent_meta:
            _, _, specs, total, completed, failed, avg_time, last_active, status_db = agent_meta
            
            # Statistics
            console.print("\n[bold]📊 Statistics:[/bold]")
            stats_table = Table(show_header=False, box=None)
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green")
            
            stats_table.add_row("Total Tasks", str(total or 0))
            stats_table.add_row("Completed", str(completed or 0))
            stats_table.add_row("Failed", str(failed or 0))
            
            if total and total > 0:
                success_rate = (completed / total * 100) if completed else 0
                stats_table.add_row("Success Rate", f"{success_rate:.1f}%")
            
            if avg_time:
                stats_table.add_row("Avg Completion Time", f"{avg_time:.1f} minutes")
            
            if last_active:
                stats_table.add_row("Last Active", last_active.strftime("%Y-%m-%d %H:%M"))
            
            console.print(stats_table)
        
        # Show recent history if requested
        if show_history:
            console.print("\n[bold]📜 Recent Task History:[/bold]")
            
            try:
                import psycopg2
                conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost port=5432")
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT title, status, created_at, completed_at
                    FROM tasks
                    WHERE assigned_to = %s
                    ORDER BY created_at DESC
                    LIMIT 10;
                """, (name,))
                
                tasks = cursor.fetchall()
                cursor.close()
                conn.close()
                
                if tasks:
                    history_table = Table(show_header=True, header_style="bold magenta")
                    history_table.add_column("Task", style="yellow", width=40)
                    history_table.add_column("Status", style="green", width=12)
                    history_table.add_column("Date", style="cyan", width=20)
                    
                    for title, status, created, completed in tasks:
                        date_str = completed.strftime("%Y-%m-%d %H:%M") if completed else created.strftime("%Y-%m-%d %H:%M")
                        history_table.add_row(title[:37] + "..." if len(title) > 40 else title, status, date_str)
                    
                    console.print(history_table)
                else:
                    console.print("[dim]No task history found[/dim]")
                    
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not load task history: {e}[/yellow]")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]❌ Error loading agent: {e}[/red]\n")


# ============================================================================
# COMMAND: workload
# ============================================================================

@app.command()
def workload(
    sort_by: str = typer.Option("tasks", "--sort", "-s", help="Sort by: tasks, name, success_rate"),
    limit: int = typer.Option(9, "--limit", "-n", help="Number of agents to show")
):
    """
    Show current workload across all agents
    
    Examples:
        destiny agent workload
        destiny agent workload --sort success_rate
        destiny agent workload --limit 5
    """
    console.print("\n[bold cyan]📊 AGENT WORKLOAD OVERVIEW[/bold cyan]\n")
    
    agents = get_agent_registry()
    db_metadata = get_agent_metadata_from_db()
    
    if not db_metadata:
        console.print("[yellow]⚠️  No workload data available (database not initialized)[/yellow]")
        console.print("[dim]Run: destiny setup init[/dim]\n")
        return
    
    # Create workload table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", width=25)
    table.add_column("Role", style="yellow", width=20)
    table.add_column("Tasks", style="white", width=10)
    table.add_column("Completed", style="green", width=10)
    table.add_column("Failed", style="red", width=10)
    table.add_column("Success Rate", style="blue", width=12)
    table.add_column("Workload", style="magenta", width=15)
    
    # Process data
    workload_data = []
    for row in db_metadata:
        name, role, specs, total, completed, failed, avg_time, last_active, status_db = row
        
        success_rate = (completed / total * 100) if total and total > 0 else 0
        
        # Calculate workload indicator
        if total == 0:
            workload = "░░░░░ Idle"
        elif total < 5:
            workload = "▓░░░░ Light"
        elif total < 10:
            workload = "▓▓░░░ Medium"
        elif total < 20:
            workload = "▓▓▓░░ Busy"
        else:
            workload = "▓▓▓▓▓ Very Busy"
        
        workload_data.append({
            'name': name,
            'role': role,
            'total': total or 0,
            'completed': completed or 0,
            'failed': failed or 0,
            'success_rate': success_rate,
            'workload': workload
        })
    
    # Sort
    if sort_by == "tasks":
        workload_data.sort(key=lambda x: x['total'], reverse=True)
    elif sort_by == "name":
        workload_data.sort(key=lambda x: x['name'])
    elif sort_by == "success_rate":
        workload_data.sort(key=lambda x: x['success_rate'], reverse=True)
    
    # Display
    for item in workload_data[:limit]:
        table.add_row(
            item['name'],
            item['role'],
            str(item['total']),
            str(item['completed']),
            str(item['failed']),
            f"{item['success_rate']:.1f}%",
            item['workload']
        )
    
    console.print(table)
    
    # Summary statistics
    total_tasks = sum(item['total'] for item in workload_data)
    total_completed = sum(item['completed'] for item in workload_data)
    total_failed = sum(item['failed'] for item in workload_data)
    
    console.print(f"\n[bold]Team Summary:[/bold]")
    console.print(f"  Total Tasks: {total_tasks}")
    console.print(f"  Completed: {total_completed} ({(total_completed/total_tasks*100):.1f}%)" if total_tasks > 0 else "  Completed: 0")
    console.print(f"  Failed: {total_failed}")
    
    console.print(f"\n[dim]💡 Tip: Use --sort to change sorting (tasks, name, success_rate)[/dim]\n")


# ============================================================================
# COMMAND: stats
# ============================================================================

@app.command()
def stats(
    agent_id: Optional[str] = typer.Option(None, "--agent", "-a", help="Specific agent ID"),
    period: int = typer.Option(30, "--days", "-d", help="Time period in days")
):
    """
    Show agent performance statistics
    
    Examples:
        destiny agent stats
        destiny agent stats --agent tomasz
        destiny agent stats --days 7
    """
    console.print("\n[bold cyan]📈 AGENT PERFORMANCE STATISTICS[/bold cyan]\n")
    
    if agent_id:
        console.print(f"[bold]Agent:[/bold] {agent_id.title()}")
    console.print(f"[bold]Period:[/bold] Last {period} days\n")
    
    try:
        import psycopg2
        conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost port=5432")
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=period)
        
        if agent_id:
            # Specific agent stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'done' THEN 1 END) as completed,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
                    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))/60) as avg_minutes
                FROM tasks
                WHERE assigned_to ILIKE %s
                AND created_at >= %s;
            """, (f"%{agent_id}%", cutoff_date))
            
            result = cursor.fetchone()
            if result and result[0] > 0:
                total, completed, failed, avg_time = result
                
                console.print(f"[bold]Tasks:[/bold] {total}")
                console.print(f"[green]Completed:[/green] {completed} ({(completed/total*100):.1f}%)")
                console.print(f"[red]Failed:[/red] {failed} ({(failed/total*100):.1f}%)")
                if avg_time:
                    console.print(f"[blue]Avg Time:[/blue] {avg_time:.1f} minutes")
            else:
                console.print(f"[yellow]No tasks found for agent '{agent_id}' in last {period} days[/yellow]")
        else:
            # All agents comparison
            cursor.execute("""
                SELECT 
                    assigned_to,
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'done' THEN 1 END) as completed,
                    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))/60) as avg_minutes
                FROM tasks
                WHERE created_at >= %s
                GROUP BY assigned_to
                ORDER BY total DESC;
            """, (cutoff_date,))
            
            results = cursor.fetchall()
            
            if results:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Agent", style="cyan", width=30)
                table.add_column("Tasks", style="white", width=10)
                table.add_column("Completed", style="green", width=12)
                table.add_column("Success Rate", style="yellow", width=12)
                table.add_column("Avg Time", style="blue", width=12)
                
                for agent_name, total, completed, avg_time in results:
                    success_rate = (completed / total * 100) if total > 0 else 0
                    avg_time_str = f"{avg_time:.1f} min" if avg_time else "N/A"
                    
                    table.add_row(
                        agent_name or "Unassigned",
                        str(total),
                        str(completed),
                        f"{success_rate:.1f}%",
                        avg_time_str
                    )
                
                console.print(table)
            else:
                console.print(f"[yellow]No task data found in last {period} days[/yellow]")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        console.print(f"[red]❌ Error loading statistics: {e}[/red]")
        console.print("[yellow]⚠️  Make sure database is initialized: destiny setup init[/yellow]")
    
    console.print()


# ============================================================================
# COMMAND: assign
# ============================================================================

@app.command()
def assign(
    agent_id: str = typer.Argument(..., help="Agent ID to assign task to"),
    task: str = typer.Argument(..., help="Task description"),
    priority: int = typer.Option(3, "--priority", "-p", help="Task priority (1-5)"),
    deadline: Optional[str] = typer.Option(None, "--deadline", "-d", help="Deadline (YYYY-MM-DD)")
):
    """
    Assign a task to a specific agent
    
    Examples:
        destiny agent assign tomasz "Implement login feature"
        destiny agent assign anna "Test checkout flow" --priority 5
        destiny agent assign michal "Design architecture" --deadline 2025-12-01
    """
    console.print(f"\n[bold cyan]📝 ASSIGNING TASK[/bold cyan]\n")
    
    agents = get_agent_registry()
    agent_data = None
    
    # Find agent
    for aid, aclass, name, role in agents:
        if aid == agent_id.lower():
            agent_data = (aid, aclass, name, role)
            break
    
    if not agent_data:
        console.print(f"[red]❌ Agent '{agent_id}' not found![/red]")
        console.print(f"[dim]Available agents: {', '.join([a[0] for a in agents])}[/dim]\n")
        return
    
    aid, aclass, name, role = agent_data
    
    # Create task in database
    try:
        import psycopg2
        from uuid import uuid4
        
        conn = psycopg2.connect("dbname=destiny_team user=user password=password host=localhost port=5432")
        cursor = conn.cursor()
        
        task_id = str(uuid4())
        created_at = datetime.now()
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
        
        cursor.execute("""
            INSERT INTO tasks (
                task_id, project_id, title, description, assigned_to, assigned_by,
                priority, status, created_at, deadline, context
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            task_id,
            "destiny-team-framework-master",
            task[:500],  # Title limit
            task,  # Full description
            name,
            "CLI User",
            priority,
            "pending",
            created_at,
            deadline_dt,
            '{}'
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Success message
        panel = Panel(
            f"""[bold]Task:[/bold] {task}
[bold]Assigned to:[/bold] {name} ({role})
[bold]Priority:[/bold] {'🔥' * priority} ({priority}/5)
[bold]Status:[/bold] ⏳ Pending
[bold]Created:[/bold] {created_at.strftime("%Y-%m-%d %H:%M")}
{f"[bold]Deadline:[/bold] {deadline}" if deadline else ""}

[dim]Task ID: {task_id}[/dim]""",
            title="[bold green]✅ Task Assigned[/bold green]",
            border_style="green"
        )
        
        console.print(panel)
        console.print()
        
    except Exception as e:
        console.print(f"[red]❌ Error assigning task: {e}[/red]")
        console.print("[yellow]⚠️  Make sure database is initialized: destiny setup init[/yellow]\n")


# ============================================================================
# COMMAND: performance
# ============================================================================

@app.command()
def performance(
    agent_id: Optional[str] = typer.Option(None, "--agent", "-a", help="Specific agent ID"),
    metric: str = typer.Option("success_rate", "--metric", "-m", help="Metric to show: success_rate, speed, volume")
):
    """
    Show agent performance over time
    
    Examples:
        destiny agent performance
        destiny agent performance --agent tomasz
        destiny agent performance --metric speed
    """
    console.print("\n[bold cyan]📊 AGENT PERFORMANCE OVER TIME[/bold cyan]\n")
    
    # This would ideally show graphs/charts
    # For CLI, we'll show a simple trend analysis
    
    console.print(f"[bold]Metric:[/bold] {metric}")
    if agent_id:
        console.print(f"[bold]Agent:[/bold] {agent_id.title()}\n")
    else:
        console.print("[bold]Scope:[/bold] All Agents\n")
    
    console.print("[yellow]📈 Performance visualization coming soon![/yellow]")
    console.print("[dim]This would show performance trends, graphs, and comparisons[/dim]\n")
    
    # For now, show a simple message
    console.print("[bold]Available metrics:[/bold]")
    console.print("  • success_rate - Task completion rate over time")
    console.print("  • speed - Average task completion speed")
    console.print("  • volume - Number of tasks completed\n")


def agent_command():
    """Entry point for the agent command group"""
    app()


if __name__ == "__main__":
    app()
