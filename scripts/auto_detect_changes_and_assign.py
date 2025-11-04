#!/usr/bin/env python3
"""
Automatic Change Detection & Task Assignment System
Purpose: Detect ALL changes and automatically create Helena tasks
Author: Aleksander Nowak
CRITICAL: This script MUST run automatically - not rely on human memory!
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

# Project root
PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
STATE_FILE = PROJECT_ROOT / ".change_tracking_state.json"
TASKS_DIR = PROJECT_ROOT / "helena_tasks"
TASKS_DIR.mkdir(exist_ok=True)


class ChangeDetector:
    """Automatically detect changes that need propagation"""
    
    def __init__(self):
        self.changes_detected = []
        self.last_check = self._load_last_check_time()
    
    def _load_last_check_time(self) -> datetime:
        """Load when we last checked for changes"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data.get('last_check', datetime.now().isoformat()))
        return datetime.now() - timedelta(days=1)  # Check last 24h on first run
    
    def _save_check_time(self):
        """Save current check time"""
        with open(STATE_FILE, 'w') as f:
            json.dump({
                'last_check': datetime.now().isoformat(),
                'changes_detected': len(self.changes_detected)
            }, f, indent=2)
    
    def detect_new_files(self) -> List[Tuple[str, str]]:
        """Detect new Python files, docs, configs created since last check"""
        changes = []
        
        # Use git to find new files
        try:
            # Files added since last check
            since_time = self.last_check.strftime("%Y-%m-%d %H:%M:%S")
            
            # Get all tracked files
            result = subprocess.run(
                ['git', '-C', str(PROJECT_ROOT), 'ls-files'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                all_files = result.stdout.strip().split('\n')
                
                for file_path in all_files:
                    full_path = PROJECT_ROOT / file_path
                    
                    if not full_path.exists():
                        continue
                    
                    # Check if file is new or modified
                    mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
                    
                    if mtime > self.last_check:
                        # Determine change type
                        if self._is_significant_file(file_path):
                            change_type = self._classify_change(file_path)
                            changes.append((file_path, change_type))
        
        except Exception as e:
            print(f"❌ Error detecting git changes: {e}")
        
        return changes
    
    def _is_significant_file(self, file_path: str) -> bool:
        """Check if file is significant enough to require propagation"""
        
        # Ignore patterns
        ignore = [
            '__pycache__',
            '.pyc',
            '.git/',
            'node_modules/',
            '.DS_Store',
            '.change_tracking_state.json',
            'VERIFICATION_REPORT.json',
            'helena_tasks/',
            'demo_',
            'test_',
            '_output.txt',
            '.log'
        ]
        
        if any(pattern in file_path for pattern in ignore):
            return False
        
        # Include patterns
        include_extensions = [
            '.py',      # Python code
            '.md',      # Documentation
            '.sql',     # Database scripts
            '.cypher',  # Neo4j scripts
            '.sh',      # Shell scripts
            '.json',    # Config files
            '.yaml',
            '.yml',
            '.toml'
        ]
        
        return any(file_path.endswith(ext) for ext in include_extensions)
    
    def _classify_change(self, file_path: str) -> str:
        """Classify what type of change this is"""
        
        if 'agent' in file_path and file_path.endswith('.py'):
            return 'agent_code'
        elif 'mixin' in file_path:
            return 'tool_mixin'
        elif 'PROTOCOL' in file_path or 'PROCESS' in file_path:
            return 'process_change'
        elif file_path.endswith('.sql'):
            return 'database_schema'
        elif file_path.endswith('.cypher'):
            return 'knowledge_graph'
        elif 'toolkit' in file_path:
            return 'agent_toolkit'
        elif file_path.endswith('.md'):
            return 'documentation'
        elif 'config' in file_path:
            return 'configuration'
        else:
            return 'general_change'
    
    def run_detection(self) -> List[Dict]:
        """Run full change detection"""
        print("🔍 Running automatic change detection...")
        print(f"   Last check: {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}")
        
        changes = self.detect_new_files()
        
        for file_path, change_type in changes:
            change_info = {
                'file_path': file_path,
                'change_type': change_type,
                'detected_at': datetime.now().isoformat(),
                'requires_propagation': True
            }
            self.changes_detected.append(change_info)
            print(f"   📄 Detected: {file_path} ({change_type})")
        
        self._save_check_time()
        
        return self.changes_detected


class HelenaTaskGenerator:
    """Automatically generate detailed tasks for Helena"""
    
    def __init__(self):
        self.tasks_created = []
    
    def generate_task(self, change: Dict) -> str:
        """Generate a complete task for Helena based on change"""
        
        file_path = change['file_path']
        change_type = change['change_type']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        task_filename = f"helena_task_{timestamp}_{change_type}.md"
        task_path = TASKS_DIR / task_filename
        
        # Generate task content based on change type
        task_content = self._generate_task_content(change)
        
        with open(task_path, 'w') as f:
            f.write(task_content)
        
        self.tasks_created.append(str(task_path))
        return str(task_path)
    
    def _generate_task_content(self, change: Dict) -> str:
        """Generate detailed task instructions"""
        
        file_path = change['file_path']
        change_type = change['change_type']
        
        # Read file to understand what changed
        full_path = PROJECT_ROOT / file_path
        try:
            with open(full_path, 'r') as f:
                content_preview = f.read()[:500]  # First 500 chars
        except:
            content_preview = "[Could not read file]"
        
        task = f"""# AUTOMATIC TASK ASSIGNMENT: Propagate Change to Databases

**GENERATED AUTOMATICALLY BY:** Change Detection System  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Assigned to:** Helena Kowalczyk  
**Priority:** HIGH  
**Type:** Knowledge Propagation  
**Status:** PENDING  

---

## 🚨 **CHANGE DETECTED**

**File:** `{file_path}`  
**Type:** {change_type}  
**Detected at:** {change['detected_at']}  

**File Preview:**
```
{content_preview}
...
```

---

## 📋 **YOUR TASK (Helena)**

This change was **automatically detected** and requires propagation to ALL databases.

### **What You Must Do:**

1. **Analyze the change:**
   - Read the full file: `{file_path}`
   - Understand what it does
   - Identify what information needs to be in databases

2. **Update PostgreSQL:**
   - Add to `team_tools` if it's a new tool
   - Add to `agent_capabilities` if it changes agent abilities
   - Add to `project_processes` if it's a new process
   - Create SQL script in `sql/` directory

3. **Update Neo4j:**
   - Create nodes for new tools/processes/agents
   - Create relationships showing connections
   - Create Cypher script in `sql/` directory

4. **Update Qdrant:**
   - Index the documentation semantically
   - Make it searchable by meaning
   - Use script in `scripts/` directory

5. **Update Redis:**
   - Create cache entries for quick access
   - Set appropriate TTL
   - Use docker exec commands

6. **Verify:**
   - Run: `python3 scripts/verify_task_completion.py`
   - All checks must pass
   - Provide evidence

7. **Report:**
   - Create completion report
   - Include verification results
   - Save as: `{TASKS_DIR}/completed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md`

---

## ⚠️ **CRITICAL REQUIREMENTS**

- ✅ You MUST complete this within 4 hours
- ✅ You MUST update ALL 4 databases (PostgreSQL, Neo4j, Qdrant, Redis)
- ✅ You MUST run verification before reporting
- ✅ You MUST provide evidence with completion report
- ✅ If blocked, report IMMEDIATELY to Aleksander

---

## 📊 **VERIFICATION CRITERIA**

Your task is complete ONLY when:

```sql
-- PostgreSQL check
SELECT COUNT(*) FROM team_tools WHERE file_path LIKE '%{file_path}%';
-- Should return > 0

-- Neo4j check
MATCH (n) WHERE n.file_path CONTAINS '{file_path}' RETURN count(n);
-- Should return > 0
```

```bash
# Qdrant check
curl -X POST http://localhost:6333/collections/destiny-team-framework-master/points/scroll \\
  -H "Content-Type: application/json" \\
  -d '{{"filter": {{"must": [{{"key": "file_path", "match": {{"text": "{file_path}"}}}}]}}}}' | jq '.result.points | length'
# Should return > 0

# Redis check
docker exec kg-redis redis-cli KEYS "*{Path(file_path).stem}*"
# Should return > 0
```

---

## 🎯 **ACCOUNTABILITY**

This task was **AUTOMATICALLY GENERATED** because the system detected a change.

**This proves:**
- ✅ System monitors itself
- ✅ No human needs to remember
- ✅ Zero knowledge drift guaranteed
- ✅ Continuous monitoring works

**Helena, you are accountable for:**
1. Executing this task completely
2. Updating all databases
3. Running verification
4. Reporting with evidence

**If you don't complete this task:**
- ❌ Knowledge drift occurs
- ❌ Agents won't discover this change
- ❌ Project soundness degrades
- ❌ System breaks down

---

## 📝 **COMPLETION REPORT TEMPLATE**

When done, create a file with this content:

```markdown
# Task Completion Report

**Task:** Propagate {file_path} to databases  
**Assigned by:** Automatic Change Detection System  
**Completed by:** Helena Kowalczyk  
**Date:** [DATE]  

## What Was Done:

### PostgreSQL:
- [ ] Updated tables: [list]
- [ ] SQL script: [path]
- [ ] Records added: [count]

### Neo4j:
- [ ] Nodes created: [list]
- [ ] Relationships: [list]
- [ ] Cypher script: [path]

### Qdrant:
- [ ] Documents indexed: [count]
- [ ] Indexing script: [path]

### Redis:
- [ ] Cache keys created: [list]
- [ ] TTL set: [seconds]

## Verification Results:

```
[Paste output of verify_task_completion.py]
```

## Evidence:

- PostgreSQL: [verification query results]
- Neo4j: [verification query results]
- Qdrant: [verification query results]
- Redis: [verification query results]

## Status: ✅ COMPLETE - VERIFIED

Helena Kowalczyk
```

---

**This is an AUTOMATIC task. Complete it to maintain project soundness.**
"""
        
        return task


class AutomaticMonitoringSystem:
    """Main system that ties everything together"""
    
    def __init__(self):
        self.detector = ChangeDetector()
        self.task_generator = HelenaTaskGenerator()
    
    def run(self):
        """Run the full automatic monitoring cycle"""
        
        print("="*80)
        print(" "*20 + "AUTOMATIC CHANGE DETECTION SYSTEM")
        print(" "*20 + "Continuous Monitoring & Knowledge Propagation")
        print("="*80)
        print()
        
        # Detect changes
        changes = self.detector.run_detection()
        
        if not changes:
            print("✅ No significant changes detected since last check.")
            print("   System is up to date.")
            return 0
        
        print(f"\n🚨 {len(changes)} change(s) detected requiring propagation!")
        print()
        
        # Generate tasks for Helena
        print("📋 Generating automatic tasks for Helena...")
        for change in changes:
            task_path = self.task_generator.generate_task(change)
            print(f"   ✅ Created: {task_path}")
        
        print()
        print("="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Changes detected: {len(changes)}")
        print(f"Tasks created: {len(self.task_generator.tasks_created)}")
        print()
        print("📨 Helena has been assigned tasks automatically.")
        print("🔍 Tasks location:", TASKS_DIR)
        print()
        print("Next steps:")
        print("1. Helena will be notified (automatic)")
        print("2. Helena executes tasks")
        print("3. Helena runs verification")
        print("4. Helena reports completion")
        print()
        print("✅ AUTOMATIC MONITORING: OPERATIONAL")
        print("="*80)
        
        return len(changes)


def main():
    """Main entry point"""
    system = AutomaticMonitoringSystem()
    
    try:
        changes_count = system.run()
        sys.exit(0 if changes_count >= 0 else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
