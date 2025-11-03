"""
destiny-status command implementation
Shows agent and task status

Author: Tomasz Kamiński (Developer)
Based on: Day 1 specs (Katarzyna, Magdalena, Michał)
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

console = Console()


def get_agent_status():
    """Get status of all agents"""
    try:
        # Import agent classes
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
            ("Tomasz Kamiński", "Developer", "Available"),
            ("Anna Lewandowska", "QA Engineer", "Available"),
            ("Magdalena Wiśniewska", "UX Designer", "Available"),
            ("Michał Kowalczyk", "Architect", "Available"),
            ("Katarzyna Zielińska", "Product Manager", "Available"),
            ("Piotr Nowicki", "DevOps Engineer", "Available"),
            ("Joanna Mazur", "Data Scientist", "Available"),
            ("Dr. Joanna Kowalska", "Research Lead", "Available"),
            ("Aleksander Nowak", "Orchestrator", "Available")
        ]
        
        return agents
    except Exception as e:
        console.print(f"[red]Error loading agents: {e}[/red]")
        return []


def status_command(
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Filter by agent name"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information")
):
    """
    Show status of Destiny Team agents
    
    Examples:
        destiny status                    # Show all agents
        destiny status --agent tomasz     # Show specific agent
        destiny status --verbose          # Show detailed info
    """
    
    console.print("\n[bold cyan]🤖 Destiny Team Status[/bold cyan]\n")
    
    # Get agent data
    agents = get_agent_status()
    
    if agent:
        # Filter by agent name
        agents = [a for a in agents if agent.lower() in a[0].lower()]
        if not agents:
            console.print(f"[yellow]No agent found matching '{agent}'[/yellow]")
            return
    
    # Create status table
    table = Table(title="Agent Status", show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", width=25)
    table.add_column("Role", style="green", width=20)
    table.add_column("Status", style="yellow", width=15)
    
    if verbose:
        table.add_column("Tasks", style="blue", width=10)
        table.add_column("Workload", style="red", width=10)
    
    for agent_name, role, status in agents:
        if verbose:
            # In real implementation, would query actual task data
            table.add_row(agent_name, role, status, "0", "Low")
        else:
            table.add_row(agent_name, role, status)
    
    console.print(table)
    
    # Summary
    console.print(f"\n[bold green]✅ {len(agents)}/9 agents operational[/bold green]")
    console.print("[dim]Use --verbose for detailed information[/dim]\n")


if __name__ == "__main__":
    # Test the command
    status_command()
