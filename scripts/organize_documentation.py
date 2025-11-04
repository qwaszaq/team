#!/usr/bin/env python3
"""
Documentation Organization Script
==================================
Automatically organize all .md files into proper folder structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")

# Target structure
STRUCTURE = {
    'protocols': [
        'PROTOCOL', 'PROCESS', 'PROCEDURE', 'MONITORING',
        'DATA_LOADING', 'DATA_PERSISTENCE', 'VERIFICATION'
    ],
    'team': [
        'ALEKSANDER', 'HELENA', 'TEAM', 'AGENT', 'COOPERATION',
        'ANALYTICAL_TEAM', 'PAIR', 'WORKING_RELATIONSHIP'
    ],
    'status': [
        'STATUS', 'FINAL', 'COMPLETE', 'SUMMARY', 'REPORT',
        'DAY_', 'HANDOFF', 'ANNOUNCEMENT'
    ],
    'architecture': [
        'ARCHITECTURE', 'FRAMEWORK', 'DESIGN', 'SYSTEM',
        'INTEGRATION', 'STRUCTURE'
    ],
    'guides': [
        'GUIDE', 'SETUP', 'QUICK_START', 'README',
        'TUTORIAL', 'HOWTO'
    ],
    'analysis': [
        'ANALYSIS', 'RESEARCH', 'ASSESSMENT', 'EVALUATION',
        'GAP', 'DEEP_DIVE', 'TOOLKITS'
    ],
    'tasks': [
        'TASK', 'CHALLENGE', 'TODO', 'CHECKLIST'
    ]
}

def classify_file(filename: str) -> str:
    """Determine which category a file belongs to"""
    
    filename_upper = filename.upper()
    
    # Check each category
    for category, keywords in STRUCTURE.items():
        for keyword in keywords:
            if keyword in filename_upper:
                return category
                
    # Default to 'general' if no match
    return 'general'

def organize_docs():
    """Organize all .md files"""
    
    print("="*80)
    print(" "*25 + "📁 ORGANIZING DOCUMENTATION")
    print("="*80)
    print()
    
    # Get all .md files in root
    md_files = list(PROJECT_ROOT.glob("*.md"))
    
    if not md_files:
        print("✅ No .md files to organize in root directory")
        return
        
    print(f"📄 Found {len(md_files)} markdown files in root")
    print()
    
    # Create categories
    docs_dir = PROJECT_ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Create all category folders
    for category in list(STRUCTURE.keys()) + ['general']:
        category_dir = docs_dir / category
        category_dir.mkdir(exist_ok=True)
        
    # Track moves
    moves = {}
    
    # Classify and move files
    for md_file in md_files:
        category = classify_file(md_file.name)
        target_dir = docs_dir / category
        target_path = target_dir / md_file.name
        
        # Track
        if category not in moves:
            moves[category] = []
        moves[category].append(md_file.name)
        
        # Move file
        try:
            shutil.move(str(md_file), str(target_path))
        except Exception as e:
            print(f"⚠️  Could not move {md_file.name}: {e}")
            
    # Report
    print("📊 ORGANIZATION SUMMARY:")
    print()
    
    for category, files in sorted(moves.items()):
        print(f"📁 {category.upper()}/")
        for filename in sorted(files):
            print(f"   ├─ {filename}")
        print()
        
    print("="*80)
    print(f"✅ Organized {sum(len(f) for f in moves.values())} files into {len(moves)} categories")
    print("="*80)
    
    # Create index
    create_index(moves)
    
def create_index(moves: dict):
    """Create documentation index"""
    
    index_path = PROJECT_ROOT / "docs" / "INDEX.md"
    
    content = f"""# 📚 Documentation Index

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Documents:** {sum(len(f) for f in moves.values())}

---

## 📁 Structure

"""
    
    for category, files in sorted(moves.items()):
        content += f"\n### {category.upper()} ({len(files)} files)\n\n"
        
        category_desc = {
            'protocols': 'Process definitions, monitoring procedures, data handling protocols',
            'team': 'Team member profiles, agent definitions, collaboration patterns',
            'status': 'Status reports, completion summaries, project updates',
            'architecture': 'System design, framework documentation, integration patterns',
            'guides': 'Setup guides, tutorials, quick starts, how-to documents',
            'analysis': 'Research documents, assessments, deep dives',
            'tasks': 'Task definitions, challenges, checklists',
            'general': 'Miscellaneous documentation'
        }
        
        content += f"*{category_desc.get(category, 'Various documents')}*\n\n"
        
        for filename in sorted(files):
            # Create relative link
            link = f"{category}/{filename}"
            title = filename.replace('.md', '').replace('_', ' ')
            content += f"- [{title}]({link})\n"
            
        content += "\n"
        
    content += """
---

## 🔍 Quick Navigation

### By Topic

- **Getting Started:** See [guides/](guides/)
- **Team Information:** See [team/](team/)
- **System Architecture:** See [architecture/](architecture/)
- **Process Protocols:** See [protocols/](protocols/)
- **Project Status:** See [status/](status/)
- **Analysis & Research:** See [analysis/](analysis/)

### By Date

Most recent documents are typically in [status/](status/)

---

**Note:** This index is automatically generated. To reorganize documentation, run:
```bash
python3 scripts/organize_documentation.py
```
"""
    
    index_path.write_text(content)
    print(f"\n📋 Created index: docs/INDEX.md")

if __name__ == "__main__":
    organize_docs()
