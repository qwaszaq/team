#!/usr/bin/env python3
"""
Aleksander's Task Delegation Statistics
=======================================
Real-time analysis of orchestration patterns
"""

import json
import psycopg2
from datetime import datetime, timedelta
from collections import defaultdict
import requests

class AleksanderRealStats:
    """Analyze real task delegation from PostgreSQL"""
    
    def __init__(self):
        # PostgreSQL connection
        self.pg_config = {
            'host': 'localhost',
            'database': 'destiny_team',
            'user': 'user',
            'password': 'password'
        }
        
    def get_real_statistics(self, days: int = 7) -> str:
        """Get real statistics from PostgreSQL"""
        
        try:
            conn = psycopg2.connect(**self.pg_config)
            cursor = conn.cursor()
            
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            
            report = f"""
# 🎯 ALEKSANDER'S ORCHESTRATION STATISTICS (REAL DATA)
## Period: Last {days} days  
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
"""
            
            # 1. Message flow by agent
            cursor.execute("""
            SELECT 
                agent_name,
                COUNT(*) as message_count,
                COUNT(DISTINCT DATE(created_at)) as active_days,
                MIN(created_at) as first_message,
                MAX(created_at) as last_message
            FROM messages
            WHERE created_at >= %s
            GROUP BY agent_name
            ORDER BY message_count DESC
            """, (cutoff,))
            
            agent_stats = cursor.fetchall()
            
            if agent_stats:
                report += """
## 📊 AGENT ACTIVITY OVERVIEW

| Agent | Messages | Active Days | First Activity | Last Activity |
|-------|----------|-------------|----------------|---------------|"""
                
                for stat in agent_stats:
                    report += f"""
| {stat[0]} | {stat[1]} | {stat[2]} | {stat[3].strftime('%Y-%m-%d %H:%M')} | {stat[4].strftime('%Y-%m-%d %H:%M')} |"""
                    
            # 2. Decision patterns
            cursor.execute("""
            SELECT 
                agent_name,
                decision_type,
                COUNT(*) as count
            FROM decisions
            WHERE created_at >= %s
            GROUP BY agent_name, decision_type
            ORDER BY count DESC
            LIMIT 20
            """, (cutoff,))
            
            decisions = cursor.fetchall()
            
            if decisions:
                report += """

## 🤔 DECISION PATTERNS

| Agent | Decision Type | Count |
|-------|---------------|-------|"""
                
                for dec in decisions:
                    report += f"""
| {dec[0]} | {dec[1]} | {dec[2]} |"""
                    
            # 3. Context usage patterns
            cursor.execute("""
            SELECT 
                agent_name,
                COUNT(*) as context_updates,
                COUNT(DISTINCT context_type) as context_types
            FROM agent_contexts
            WHERE created_at >= %s
            GROUP BY agent_name
            ORDER BY context_updates DESC
            """, (cutoff,))
            
            contexts = cursor.fetchall()
            
            if contexts:
                report += """

## 🧠 CONTEXT USAGE

| Agent | Context Updates | Unique Context Types |
|-------|----------------|---------------------|"""
                
                for ctx in contexts:
                    report += f"""
| {ctx[0]} | {ctx[1]} | {ctx[2]} |"""
                    
            # 4. Hourly activity pattern
            cursor.execute("""
            SELECT 
                EXTRACT(HOUR FROM created_at) as hour,
                COUNT(*) as activity_count
            FROM messages
            WHERE created_at >= %s
            GROUP BY hour
            ORDER BY hour
            """, (cutoff,))
            
            hourly = cursor.fetchall()
            
            if hourly:
                report += """

## ⏰ HOURLY ACTIVITY PATTERN
"""
                max_activity = max([h[1] for h in hourly]) if hourly else 1
                
                for hour, count in hourly:
                    bar = "█" * int(30 * count / max_activity)
                    report += f"\n{int(hour):02d}:00 | {bar} {count}"
                    
            # 5. Check Elasticsearch for document processing
            try:
                es_response = requests.get(
                    "http://localhost:9200/project_knowledge/_count",
                    auth=("elastic", "changeme123")
                )
                
                if es_response.status_code == 200:
                    doc_count = es_response.json()['count']
                    report += f"""

## 📚 KNOWLEDGE BASE STATUS
- **Indexed Documents:** {doc_count:,}
- **Search Capability:** ✅ Active
"""
            except:
                report += """

## 📚 KNOWLEDGE BASE STATUS
- **Elasticsearch:** ⚠️  Not accessible
"""
                
            # 6. Helena task processing
            cursor.execute("""
            SELECT 
                COUNT(*) as total_tasks,
                COUNT(DISTINCT DATE(created_at)) as days_active,
                AVG(CHAR_LENGTH(content)) as avg_task_length
            FROM messages
            WHERE agent_name = 'Helena' 
                AND content LIKE '%task%'
                AND created_at >= %s
            """, (cutoff,))
            
            helena_stats = cursor.fetchone()
            
            if helena_stats and helena_stats[0] > 0:
                report += f"""

## 🔮 HELENA TASK PROCESSING
- **Tasks Processed:** {helena_stats[0]}
- **Days Active:** {helena_stats[1]}
- **Avg Task Complexity:** {helena_stats[2]:.0f} characters
"""
                
            # 7. Calculate efficiency metrics
            report += """

## 📈 EFFICIENCY ANALYSIS
"""
            
            # Messages per agent per day
            cursor.execute("""
            SELECT 
                agent_name,
                CAST(COUNT(*) AS FLOAT) / GREATEST(COUNT(DISTINCT DATE(created_at)), 1) as msgs_per_day
            FROM messages
            WHERE created_at >= %s
            GROUP BY agent_name
            ORDER BY msgs_per_day DESC
            """, (cutoff,))
            
            efficiency = cursor.fetchall()
            
            if efficiency:
                report += """
### Daily Message Volume (Efficiency Indicator)
"""
                for eff in efficiency[:5]:
                    report += f"\n- **{eff[0]}**: {eff[1]:.1f} messages/day"
                    
            # 8. Recommendations
            report += """

---

## 💡 ALEKSANDER'S ORCHESTRATION RECOMMENDATIONS

Based on the analysis:
"""
            
            if agent_stats:
                # Find most and least active
                most_active = agent_stats[0][0]
                least_active = agent_stats[-1][0] if len(agent_stats) > 1 else None
                
                report += f"""
1. **Workload Distribution:**
   - {most_active} is handling the most tasks ({agent_stats[0][1]} messages)"""
                
                if least_active:
                    report += f"""
   - Consider delegating more to {least_active} ({agent_stats[-1][1]} messages)"""
                    
            # Peak hours recommendation
            if hourly:
                peak_hour = max(hourly, key=lambda x: x[1])
                report += f"""

2. **Resource Planning:**
   - Peak activity at {int(peak_hour[0]):02d}:00 ({peak_hour[1]} activities)
   - Consider scheduling heavy tasks outside peak hours"""
                
            # Specialization recommendations
            if decisions:
                # Group decisions by agent
                agent_decisions = defaultdict(list)
                for dec in decisions:
                    agent_decisions[dec[0]].append(dec[1])
                    
                report += """

3. **Agent Specialization:**"""
                
                for agent, dec_types in list(agent_decisions.items())[:3]:
                    primary = dec_types[0] if dec_types else "general"
                    report += f"""
   - {agent} excels at {primary} decisions"""
                    
            conn.close()
            
            return report
            
        except Exception as e:
            return f"""
# ❌ ERROR GENERATING STATISTICS

Unable to connect to PostgreSQL or analyze data:
{str(e)}

Please ensure:
1. PostgreSQL is running
2. Database 'destiny_team' exists
3. Required tables are present
"""

def main():
    """Generate Aleksander's orchestration report"""
    
    print("🎯 ALEKSANDER: Analyzing orchestration patterns...\n")
    
    stats = AleksanderRealStats()
    
    # Try different time periods
    for days in [1, 7, 30]:
        print(f"\n{'='*80}")
        print(f"Analyzing last {days} day(s)...")
        print('='*80)
        
        report = stats.get_real_statistics(days)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"aleksander_stats_{days}days_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write(report)
            
        print(report)
        print(f"\n📄 Report saved to: {filename}")
        
        if days < 30:
            input("\nPress Enter to analyze longer period...")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Aleksander's Real Statistics")
    parser.add_argument('--days', type=int, default=7, help='Days to analyze')
    parser.add_argument('--save', action='store_true', help='Save to file')
    
    args = parser.parse_args()
    
    stats = AleksanderRealStats()
    report = stats.get_real_statistics(args.days)
    
    print(report)
    
    if args.save:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"aleksander_orchestration_stats_{timestamp}.md"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n✅ Saved to: {filename}")