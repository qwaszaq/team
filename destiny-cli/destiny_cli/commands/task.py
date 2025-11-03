"""
destiny-task command implementation
Task creation and management

Author: Tomasz Kamiński (Developer)
Based on: Day 1 specs + TaskQueue integration
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from pathlib import Path
import sys
import uuid
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

console = Console()


def task_create(description: str, agent: Optional[str] = None, priority: int = 3):
    """Create a new task"""
    try:
        from agents.task_models import Task, TaskStatus
        
        task_id = uuid.uuid4()
        task = Task(
            task_id=task_id,
            title=description[:50],  # Truncate for title
            description=description,
            assigned_to=agent or "Unassigned",
            assigned_by="CLI User",
            context={},
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        console.print(f"[green]✅ Task created:[/green] {task_id}")
        console.print(f"   Description: {description}")
        console.print(f"   Priority: {priority}")
        if agent:
            console.print(f"   Assigned to: {agent}")
        
        return task
        
    except Exception as e:
        console.print(f"[red]Error creating task: {e}[/red]")
        return None


def task_list(
    status: Optional[str] = None,
    agent: Optional[str] = None,
    priority: Optional[int] = None
):
    """List all tasks with optional filters"""
    console.print("\n[bold cyan]📋 Destiny Team Tasks[/bold cyan]\n")
    
    # Sample tasks (in production, would query TaskQueue)
    tasks = [
        ("Task-001", "Implement feature X", "Tomasz", "pending", 5),
        ("Task-002", "Test feature X", "Anna", "pending", 4),
        ("Task-003", "Design UI", "Magdalena", "done", 3),
        ("Task-004", "Review architecture", "Michał", "in_progress", 4),
    ]
    
    # Apply filters
    if status:
        tasks = [t for t in tasks if t[3] == status.lower()]
    if agent:
        tasks = [t for t in tasks if agent.lower() in t[2].lower()]
    if priority is not None:
        tasks = [t for t in tasks if t[4] == priority]
    
    # Create table
    table = Table(title="Tasks", show_header=True, header_style="bold magenta")
    table.add_column("Task ID", style="cyan", width=12)
    table.add_column("Description", style="white", width=30)
    table.add_column("Assigned To", style="green", width=20)
    table.add_column("Status", style="yellow", width=12)
    table.add_column("Priority", style="red", width=8)
    
    for task_id, desc, assigned, stat, prio in tasks:
        table.add_row(task_id, desc, assigned, stat, str(prio))
    
    console.print(table)
    console.print(f"\n[bold green]Total: {len(tasks)} tasks[/bold green]\n")


def task_command():
    """Main task command dispatcher"""
    app = typer.Typer()
    
    @app.command("create")
    def create(
        description: str,
        agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Assign to agent"),
        priority: int = typer.Option(3, "--priority", "-p", help="Priority (1-5)")
    ):
        """Create a new task"""
        task_create(description, agent, priority)
    
    @app.command("list")
    def list_tasks(
        status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
        agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Filter by agent"),
        priority: Optional[int] = typer.Option(None, "--priority", "-p", help="Filter by priority")
    ):
        """List all tasks"""
        task_list(status, agent, priority)
    
    return app


if __name__ == "__main__":
    # Test the commands
    task_list()
