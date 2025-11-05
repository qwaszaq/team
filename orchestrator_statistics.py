#!/usr/bin/env python3
"""
Aleksander's Orchestration Statistics System
============================================
Tracks and analyzes task delegation patterns across all agents
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from pathlib import Path
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

class OrchestratorStatistics:
    """Aleksander's statistical analysis of task orchestration"""
    
    def __init__(self):
        self.db_path = "orchestration_stats.db"
        self.initialize_db()
        
    def initialize_db(self):
        """Create statistics tables if they don't exist"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Task delegation table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_delegations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            task_type TEXT NOT NULL,
            priority INTEGER DEFAULT 5,
            delegated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status TEXT DEFAULT 'pending',
            tokens_used INTEGER DEFAULT 0,
            execution_time_seconds FLOAT,
            parent_task_id TEXT,
            result_quality_score FLOAT
        )
        """)
        
        # Agent performance metrics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_metrics (
            agent_name TEXT PRIMARY KEY,
            total_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            failed_tasks INTEGER DEFAULT 0,
            avg_execution_time FLOAT DEFAULT 0,
            avg_tokens_used FLOAT DEFAULT 0,
            specialization_score FLOAT DEFAULT 0,
            last_active TIMESTAMP
        )
        """)
        
        # Task type statistics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_type_stats (
            task_type TEXT PRIMARY KEY,
            total_count INTEGER DEFAULT 0,
            avg_completion_time FLOAT DEFAULT 0,
            success_rate FLOAT DEFAULT 0,
            preferred_agent TEXT
        )
        """)
        
        conn.commit()
        conn.close()
        
    def record_task_delegation(self, 
                             task_id: str,
                             agent_name: str,
                             task_type: str,
                             priority: int = 5,
                             parent_task_id: str = None):
        """Record when a task is delegated to an agent"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO task_delegations 
        (task_id, agent_name, task_type, priority, parent_task_id)
        VALUES (?, ?, ?, ?, ?)
        """, (task_id, agent_name, task_type, priority, parent_task_id))
        
        # Update agent metrics
        cursor.execute("""
        INSERT INTO agent_metrics (agent_name, total_tasks, last_active)
        VALUES (?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(agent_name) DO UPDATE SET
        total_tasks = total_tasks + 1,
        last_active = CURRENT_TIMESTAMP
        """, (agent_name,))
        
        conn.commit()
        conn.close()
        
    def record_task_completion(self,
                             task_id: str,
                             tokens_used: int,
                             execution_time: float,
                             quality_score: float = None):
        """Record task completion metrics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE task_delegations
        SET status = 'completed',
            completed_at = CURRENT_TIMESTAMP,
            tokens_used = ?,
            execution_time_seconds = ?,
            result_quality_score = ?
        WHERE task_id = ?
        """, (tokens_used, execution_time, quality_score, task_id))
        
        # Get agent name for this task
        cursor.execute("SELECT agent_name FROM task_delegations WHERE task_id = ?", (task_id,))
        agent = cursor.fetchone()
        
        if agent:
            agent_name = agent[0]
            # Update agent metrics
            cursor.execute("""
            UPDATE agent_metrics
            SET completed_tasks = completed_tasks + 1,
                avg_tokens_used = (avg_tokens_used * completed_tasks + ?) / (completed_tasks + 1),
                avg_execution_time = (avg_execution_time * completed_tasks + ?) / (completed_tasks + 1)
            WHERE agent_name = ?
            """, (tokens_used, execution_time, agent_name))
        
        conn.commit()
        conn.close()
        
    def generate_orchestration_report(self, days: int = 7) -> str:
        """Generate comprehensive orchestration statistics report"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Calculate time range
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        report = f"""
# 🎯 ALEKSANDER'S ORCHESTRATION STATISTICS
## Period: Last {days} days
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 OVERALL METRICS
"""
        
        # Overall statistics
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
            AVG(CASE WHEN status = 'completed' THEN execution_time_seconds END) as avg_time,
            SUM(CASE WHEN status = 'completed' THEN tokens_used ELSE 0 END) as total_tokens
        FROM task_delegations
        WHERE delegated_at >= ?
        """, (cutoff_date,))
        
        stats = cursor.fetchone()
        
        completion_rate = (stats[1] / stats[0] * 100) if stats[0] > 0 else 0
        
        report += f"""
- **Total Tasks Delegated:** {stats[0]}
- **Completed:** {stats[1]} ({completion_rate:.1f}%)
- **Failed:** {stats[2]}
- **Pending:** {stats[3]}
- **Average Execution Time:** {stats[4]:.1f}s
- **Total Tokens Used:** {stats[5]:,}

---

## 🤖 AGENT PERFORMANCE BREAKDOWN
"""
        
        # Agent statistics
        cursor.execute("""
        SELECT 
            td.agent_name,
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN td.status = 'completed' THEN 1 END) as completed,
            AVG(CASE WHEN td.status = 'completed' THEN td.execution_time_seconds END) as avg_time,
            SUM(CASE WHEN td.status = 'completed' THEN td.tokens_used ELSE 0 END) as total_tokens,
            AVG(CASE WHEN td.status = 'completed' THEN td.result_quality_score END) as avg_quality
        FROM task_delegations td
        WHERE td.delegated_at >= ?
        GROUP BY td.agent_name
        ORDER BY total_tasks DESC
        """, (cutoff_date,))
        
        agents = cursor.fetchall()
        
        report += """
| Agent | Tasks | Completed | Avg Time | Tokens Used | Quality Score |
|-------|-------|-----------|----------|-------------|---------------|"""
        
        for agent in agents:
            success_rate = (agent[2] / agent[1] * 100) if agent[1] > 0 else 0
            avg_time = agent[3] if agent[3] else 0
            quality = agent[5] if agent[5] else 0
            
            report += f"""
| {agent[0]} | {agent[1]} | {agent[2]} ({success_rate:.0f}%) | {avg_time:.1f}s | {agent[4]:,} | {quality:.2f}/10 |"""
            
        # Task type distribution
        report += """

---

## 📋 TASK TYPE DISTRIBUTION
"""
        
        cursor.execute("""
        SELECT 
            task_type,
            COUNT(*) as count,
            agent_name,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
        FROM task_delegations
        WHERE delegated_at >= ?
        GROUP BY task_type, agent_name
        ORDER BY count DESC
        """, (cutoff_date,))
        
        task_types = cursor.fetchall()
        
        # Group by task type
        task_distribution = defaultdict(lambda: {'total': 0, 'agents': {}})
        for tt in task_types:
            task_distribution[tt[0]]['total'] += tt[1]
            task_distribution[tt[0]]['agents'][tt[2]] = tt[1]
            
        report += """
| Task Type | Total | Primary Agent | Distribution |
|-----------|-------|---------------|--------------|"""
        
        for task_type, data in sorted(task_distribution.items(), key=lambda x: x[1]['total'], reverse=True):
            primary_agent = max(data['agents'].items(), key=lambda x: x[1])[0]
            distribution = ", ".join([f"{agent}: {count}" for agent, count in data['agents'].items()])
            
            report += f"""
| {task_type} | {data['total']} | {primary_agent} | {distribution} |"""
            
        # Time-based patterns
        report += """

---

## ⏰ TEMPORAL PATTERNS
"""
        
        cursor.execute("""
        SELECT 
            strftime('%H', delegated_at) as hour,
            COUNT(*) as task_count
        FROM task_delegations
        WHERE delegated_at >= ?
        GROUP BY hour
        ORDER BY hour
        """, (cutoff_date,))
        
        hourly = cursor.fetchall()
        
        report += """
### Tasks by Hour of Day
"""
        
        max_tasks = max([h[1] for h in hourly]) if hourly else 1
        for hour, count in hourly:
            bar = "█" * int(20 * count / max_tasks)
            report += f"\n{hour}:00 | {bar} {count}"
            
        # Agent specialization analysis
        report += """

---

## 🎯 AGENT SPECIALIZATION ANALYSIS
"""
        
        cursor.execute("""
        SELECT 
            agent_name,
            task_type,
            COUNT(*) as count,
            AVG(CASE WHEN status = 'completed' THEN execution_time_seconds END) as avg_time
        FROM task_delegations
        WHERE delegated_at >= ?
        GROUP BY agent_name, task_type
        HAVING count >= 3
        ORDER BY agent_name, count DESC
        """, (cutoff_date,))
        
        specializations = cursor.fetchall()
        
        current_agent = None
        for spec in specializations:
            if spec[0] != current_agent:
                current_agent = spec[0]
                report += f"\n\n### {current_agent}"
                report += "\nSpecializes in:"
            
            report += f"\n- **{spec[1]}**: {spec[2]} tasks (avg {spec[3]:.1f}s)"
            
        # Token efficiency
        report += """

---

## 💰 TOKEN EFFICIENCY ANALYSIS
"""
        
        cursor.execute("""
        SELECT 
            agent_name,
            AVG(tokens_used) as avg_tokens,
            MIN(tokens_used) as min_tokens,
            MAX(tokens_used) as max_tokens,
            SUM(tokens_used) as total_tokens
        FROM task_delegations
        WHERE status = 'completed' AND delegated_at >= ?
        GROUP BY agent_name
        ORDER BY avg_tokens ASC
        """, (cutoff_date,))
        
        token_stats = cursor.fetchall()
        
        report += """
| Agent | Avg Tokens | Min | Max | Total Used |
|-------|------------|-----|-----|------------|"""
        
        for ts in token_stats:
            report += f"""
| {ts[0]} | {ts[1]:.0f} | {ts[2]} | {ts[3]} | {ts[4]:,} |"""
            
        # Recommendations
        report += """

---

## 💡 ALEKSANDER'S RECOMMENDATIONS

Based on the analysis above:
"""
        
        # Find most efficient agent
        if agents:
            most_efficient = min(agents, key=lambda x: x[4]/max(x[2], 1))
            report += f"\n1. **Most Token-Efficient:** {most_efficient[0]} (avg {most_efficient[4]/max(most_efficient[2], 1):.0f} tokens/task)"
            
        # Find fastest agent
        if agents:
            fastest = min([a for a in agents if a[3] is not None], key=lambda x: x[3], default=None)
            if fastest:
                report += f"\n2. **Fastest Executor:** {fastest[0]} (avg {fastest[3]:.1f}s per task)"
                
        # Find specialization opportunities
        report += "\n3. **Specialization Opportunities:**"
        for task_type, data in task_distribution.items():
            if data['total'] >= 10:
                primary = max(data['agents'].items(), key=lambda x: x[1])
                percentage = (primary[1] / data['total']) * 100
                if percentage < 80:
                    report += f"\n   - Consider dedicating {primary[0]} to {task_type} tasks (currently {percentage:.0f}%)"
                    
        conn.close()
        
        return report
        
    def visualize_statistics(self, output_dir: str = "orchestration_reports"):
        """Generate visual statistics charts"""
        
        Path(output_dir).mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        # Create visualizations
        plt.style.use('seaborn')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Task distribution by agent
        df = pd.read_sql_query("""
        SELECT agent_name, COUNT(*) as task_count
        FROM task_delegations
        GROUP BY agent_name
        """, conn)
        
        if not df.empty:
            df.plot(kind='bar', x='agent_name', y='task_count', ax=axes[0,0], legend=False)
            axes[0,0].set_title('Tasks by Agent')
            axes[0,0].set_xlabel('Agent')
            axes[0,0].set_ylabel('Number of Tasks')
            
        # 2. Token usage over time
        df_tokens = pd.read_sql_query("""
        SELECT DATE(delegated_at) as date, SUM(tokens_used) as daily_tokens
        FROM task_delegations
        WHERE status = 'completed'
        GROUP BY DATE(delegated_at)
        ORDER BY date
        """, conn)
        
        if not df_tokens.empty:
            df_tokens.plot(x='date', y='daily_tokens', ax=axes[0,1], kind='line', marker='o')
            axes[0,1].set_title('Daily Token Usage')
            axes[0,1].set_xlabel('Date')
            axes[0,1].set_ylabel('Tokens Used')
            axes[0,1].legend(['Tokens'])
            
        # 3. Task completion times
        df_times = pd.read_sql_query("""
        SELECT agent_name, AVG(execution_time_seconds) as avg_time
        FROM task_delegations
        WHERE status = 'completed'
        GROUP BY agent_name
        """, conn)
        
        if not df_times.empty:
            df_times.plot(kind='barh', x='agent_name', y='avg_time', ax=axes[1,0], legend=False)
            axes[1,0].set_title('Average Execution Time by Agent')
            axes[1,0].set_xlabel('Seconds')
            
        # 4. Task type pie chart
        df_types = pd.read_sql_query("""
        SELECT task_type, COUNT(*) as count
        FROM task_delegations
        GROUP BY task_type
        """, conn)
        
        if not df_types.empty:
            df_types.set_index('task_type')['count'].plot(kind='pie', ax=axes[1,1], autopct='%1.1f%%')
            axes[1,1].set_title('Task Type Distribution')
            axes[1,1].set_ylabel('')
            
        plt.suptitle('Aleksander\'s Orchestration Dashboard', fontsize=16)
        plt.tight_layout()
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(f"{output_dir}/orchestration_stats_{timestamp}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        conn.close()
        
        print(f"📊 Visualizations saved to {output_dir}/orchestration_stats_{timestamp}.png")


# Simulate some data for demonstration
def simulate_orchestration_data():
    """Simulate some orchestration data for testing"""
    
    import random
    import uuid
    
    stats = OrchestratorStatistics()
    
    agents = ['Helena', 'Marcus', 'Elena', 'Viktor', 'Adrian', 'Damian']
    task_types = ['analysis', 'investigation', 'documentation', 'search', 'report', 'validation']
    
    print("🎲 Simulating orchestration data...")
    
    # Simulate 100 tasks over the past week
    for i in range(100):
        task_id = str(uuid.uuid4())
        agent = random.choice(agents)
        task_type = random.choice(task_types)
        priority = random.randint(1, 10)
        
        # Delegate task
        stats.record_task_delegation(task_id, agent, task_type, priority)
        
        # 90% completion rate
        if random.random() < 0.9:
            tokens = random.randint(100, 5000)
            exec_time = random.uniform(0.5, 120.0)
            quality = random.uniform(6.0, 9.5)
            
            stats.record_task_completion(task_id, tokens, exec_time, quality)
            
    print("✅ Simulation complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Aleksander's Orchestration Statistics")
    parser.add_argument('--report', action='store_true', help='Generate statistics report')
    parser.add_argument('--visualize', action='store_true', help='Generate visual charts')
    parser.add_argument('--simulate', action='store_true', help='Simulate data for testing')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze')
    
    args = parser.parse_args()
    
    stats = OrchestratorStatistics()
    
    if args.simulate:
        simulate_orchestration_data()
        
    if args.report:
        report = stats.generate_orchestration_report(args.days)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"orchestration_report_{timestamp}.md"
        with open(report_path, 'w') as f:
            f.write(report)
            
        print(report)
        print(f"\n📄 Report saved to {report_path}")
        
    if args.visualize:
        stats.visualize_statistics()
        
    if not any([args.report, args.visualize, args.simulate]):
        parser.print_help()
        print("\nExamples:")
        print("  # Generate report for last 30 days")
        print("  python orchestrator_statistics.py --report --days 30")
        print()
        print("  # Create visualization charts")
        print("  python orchestrator_statistics.py --visualize")
        print()
        print("  # Simulate data and generate report")
        print("  python orchestrator_statistics.py --simulate --report")