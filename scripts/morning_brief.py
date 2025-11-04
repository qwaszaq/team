#!/usr/bin/env python3
"""
Morning Brief Agent 🌅
======================

Automatically analyzes project history and provides hot knowledge brief
Runs at terminal start to get you up to speed instantly

What it does:
- 📊 Analyzes recent changes (last 24h, 7d, 30d)
- 📝 Summarizes latest documentation
- 🔥 Identifies "hot" topics and active areas
- 🎯 Shows what needs attention
- 💡 Provides context for current work
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
DOCS_DIR = PROJECT_ROOT / "docs"


class MorningBriefAgent:
    """Your personal project briefing agent"""
    
    def __init__(self):
        self.now = datetime.now()
        self.changes_24h = []
        self.changes_7d = []
        self.changes_30d = []
        self.hot_topics = defaultdict(int)
        
    def analyze_project(self):
        """Analyze entire project state"""
        
        print("\n" + "="*80)
        print(" "*25 + "🌅 MORNING BRIEF")
        print(" "*20 + datetime.now().strftime("%A, %B %d, %Y"))
        print(" "*25 + datetime.now().strftime("%H:%M:%S"))
        print("="*80)
        print()
        
        # Git analysis
        self.analyze_git_activity()
        
        # Documentation analysis
        self.analyze_documentation()
        
        # Recent work
        self.analyze_recent_work()
        
        # Status summary
        self.show_status_summary()
        
        # Hot topics
        self.show_hot_topics()
        
        # What's next
        self.suggest_next_actions()
        
        print("\n" + "="*80)
        print("☕ Have a great day! All knowledge is fresh and ready.")
        print("="*80 + "\n")
        
    def analyze_git_activity(self):
        """Analyze git commits"""
        
        print("📊 GIT ACTIVITY")
        print("-" * 80)
        
        try:
            # Last commit
            result = subprocess.run(
                ['git', '-C', str(PROJECT_ROOT), 'log', '-1', '--pretty=format:%h|%an|%ar|%s'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                hash, author, time, message = result.stdout.split('|', 3)
                print(f"📌 Last commit: {hash} - {message}")
                print(f"   By {author}, {time}")
            
            # Commits in last 24h
            since_24h = (self.now - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            result = subprocess.run(
                ['git', '-C', str(PROJECT_ROOT), 'log', f'--since={since_24h}', '--oneline'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commits_24h = result.stdout.strip().split('\n') if result.stdout.strip() else []
                print(f"📈 Commits last 24h: {len(commits_24h)}")
                
            # Branch info
            result = subprocess.run(
                ['git', '-C', str(PROJECT_ROOT), 'branch', '--show-current'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                branch = result.stdout.strip()
                print(f"🌿 Current branch: {branch}")
                
        except Exception as e:
            print(f"⚠️  Could not analyze git: {e}")
            
        print()
        
    def analyze_documentation(self):
        """Analyze documentation structure"""
        
        print("📚 DOCUMENTATION STATUS")
        print("-" * 80)
        
        if not DOCS_DIR.exists():
            print("⚠️  docs/ directory not found")
            print()
            return
            
        # Count by category
        categories = {}
        recent_files = []
        
        for category_dir in DOCS_DIR.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                files = list(category_dir.glob("*.md"))
                categories[category_dir.name] = len(files)
                
                # Find recent files
                for f in files:
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if (self.now - mtime).days < 7:
                            recent_files.append((f, mtime))
                    except:
                        pass
                        
        # Show categories
        total_docs = sum(categories.values())
        print(f"📄 Total documents: {total_docs}")
        print(f"📁 Categories: {len(categories)}")
        print()
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * min(count // 2, 30)
            print(f"   {cat:15s} [{count:3d}] {bar}")
            
        # Recent files
        print()
        if recent_files:
            print(f"🔥 Modified in last 7 days: {len(recent_files)}")
            recent_files.sort(key=lambda x: x[1], reverse=True)
            
            for f, mtime in recent_files[:5]:
                rel_path = f.relative_to(DOCS_DIR)
                days_ago = (self.now - mtime).days
                time_str = f"{days_ago}d ago" if days_ago > 0 else "today"
                print(f"   • {rel_path} ({time_str})")
                
        print()
        
    def analyze_recent_work(self):
        """Analyze what was worked on recently"""
        
        print("🔨 RECENT WORK AREAS")
        print("-" * 80)
        
        # Check helena_tasks
        helena_tasks = PROJECT_ROOT / "helena_tasks"
        if helena_tasks.exists():
            tasks = list(helena_tasks.glob("*.md"))
            if tasks:
                print(f"📋 Helena tasks: {len(tasks)} pending")
                
                # Show most recent
                tasks.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for task in tasks[:3]:
                    print(f"   • {task.name}")
                    
        # Check realtime queue
        realtime_queue = PROJECT_ROOT / "helena_tasks" / "realtime_queue"
        if realtime_queue.exists():
            queued = list(realtime_queue.glob("*.json"))
            if queued:
                print(f"⚡ Realtime queue: {len(queued)} items")
                
        # Check recent SQL updates
        sql_updates = PROJECT_ROOT / "sql" / "realtime_updates"
        if sql_updates.exists():
            updates = list(sql_updates.glob("*"))
            if updates:
                print(f"💾 SQL updates: {len(updates)} generated")
                
        print()
        
    def show_status_summary(self):
        """Show current project status"""
        
        print("🎯 PROJECT STATUS")
        print("-" * 80)
        
        # Read latest status files
        status_dir = DOCS_DIR / "status"
        if status_dir.exists():
            status_files = sorted(status_dir.glob("*.md"), 
                                key=lambda x: x.stat().st_mtime, 
                                reverse=True)
            
            if status_files:
                latest = status_files[0]
                print(f"📊 Latest status: {latest.name}")
                
                # Try to extract key info
                try:
                    content = latest.read_text(encoding='utf-8')
                    lines = content.split('\n')
                    
                    # Look for checkmarks or status indicators
                    completed = sum(1 for line in lines if '✅' in line or '[x]' in line.lower())
                    pending = sum(1 for line in lines if '⏳' in line or '[ ]' in line)
                    
                    if completed or pending:
                        print(f"   ✅ Completed items: {completed}")
                        print(f"   ⏳ Pending items: {pending}")
                        
                except:
                    pass
                    
        print()
        
    def show_hot_topics(self):
        """Identify hot topics in recent documentation"""
        
        print("🔥 HOT TOPICS (Last 7 days)")
        print("-" * 80)
        
        # Analyze recent doc content
        hot_keywords = defaultdict(int)
        
        for category_dir in DOCS_DIR.iterdir():
            if not category_dir.is_dir():
                continue
                
            for doc in category_dir.glob("*.md"):
                try:
                    mtime = datetime.fromtimestamp(doc.stat().st_mtime)
                    if (self.now - mtime).days < 7:
                        content = doc.read_text(encoding='utf-8').upper()
                        
                        # Key topics to track
                        topics = {
                            'HELENA': '🤖 Helena (Data Infrastructure)',
                            'ALEKSANDER': '🎯 Aleksander (Orchestration)',
                            'VERIFICATION': '✅ Verification System',
                            'DATABASE': '💾 Database Operations',
                            'PROTOCOL': '📋 Protocols & Processes',
                            'TEAM': '👥 Team Collaboration',
                            'ANALYTICAL': '📊 Analytical Team',
                            'REALTIME': '⚡ Real-Time Processing',
                            'MONITORING': '👀 Monitoring Systems'
                        }
                        
                        for keyword, label in topics.items():
                            if keyword in content:
                                hot_keywords[label] += 1
                                
                except:
                    pass
                    
        # Show top hot topics
        if hot_keywords:
            sorted_topics = sorted(hot_keywords.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)
            
            for topic, count in sorted_topics[:8]:
                heat = "🔥" * min(count, 5)
                print(f"   {topic:35s} {heat} ({count} mentions)")
        else:
            print("   No significant activity in last 7 days")
            
        print()
        
    def suggest_next_actions(self):
        """Suggest what to work on next"""
        
        print("💡 SUGGESTED ACTIONS")
        print("-" * 80)
        
        suggestions = []
        
        # Check for pending tasks
        helena_tasks = PROJECT_ROOT / "helena_tasks"
        if helena_tasks.exists():
            tasks = list(helena_tasks.glob("helena_task_*.md"))
            if tasks:
                suggestions.append(f"📋 Review {len(tasks)} pending Helena tasks")
                
        # Check for realtime queue
        realtime_queue = PROJECT_ROOT / "helena_tasks" / "realtime_queue"
        if realtime_queue.exists():
            queued = list(realtime_queue.glob("*.json"))
            if queued:
                suggestions.append(f"⚡ Process {len(queued)} items in realtime queue")
                
        # Check for uncommitted changes
        try:
            result = subprocess.run(
                ['git', '-C', str(PROJECT_ROOT), 'status', '--porcelain'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                changes = len(result.stdout.strip().split('\n'))
                suggestions.append(f"📝 Commit {changes} uncommitted changes")
                
        except:
            pass
            
        # General suggestions
        if not suggestions:
            suggestions.append("✅ All caught up! Check docs/INDEX.md for overview")
            suggestions.append("🚀 Start real-time watcher: ./start_realtime_helena.sh")
            
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
            
        print()


def create_shell_integration():
    """Create shell integration for auto-loading"""
    
    zshrc_path = Path.home() / ".zshrc"
    
    integration = """
# Destiny Project - Morning Brief Agent
if [ "$PWD" = "/Users/artur/coursor-agents-destiny-folder" ]; then
    python3 scripts/morning_brief.py
fi
"""
    
    print("\n" + "="*80)
    print("🔧 SHELL INTEGRATION")
    print("="*80)
    print()
    print("To automatically show morning brief when entering project directory,")
    print("add this to your ~/.zshrc:")
    print()
    print(integration)
    print()
    print("Or run: python3 scripts/morning_brief.py manually anytime")
    print()


def main():
    """Main entry point"""
    
    agent = MorningBriefAgent()
    agent.analyze_project()
    
    # Offer shell integration on first run
    # (commented out to avoid spam)
    # create_shell_integration()


if __name__ == "__main__":
    main()
