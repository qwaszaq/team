#!/usr/bin/env python3
"""
Automatic Documentation Generator from Git Commits
===================================================

Purpose: Automatically generate markdown documentation from git commits
         so Helena can index ALL project changes, not just manual docs.

Flow:
1. Git post-commit hook triggers this script
2. Analyze the commit (message, files changed, diff stats)
3. Generate structured markdown documentation
4. Save to docs/auto-generated/ (Helena watches this)
5. Helena auto-processes within seconds
6. Change is now in all 4 databases

Author: Destiny Team (Tomasz + Katarzyna)
Date: 2025-11-04
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path("/Users/artur/coursor-agents-destiny-folder")
AUTO_DOC_DIR = PROJECT_ROOT / "docs" / "auto-generated"


class CommitAnalyzer:
    """Analyzes git commits and extracts meaningful information"""
    
    def __init__(self, commit_hash: str = "HEAD"):
        self.commit_hash = commit_hash
        self.commit_info = self._get_commit_info()
        
    def _run_git_command(self, cmd: List[str]) -> str:
        """Run git command and return output"""
        try:
            result = subprocess.run(
                cmd,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
            return ""
    
    def _get_commit_info(self) -> Dict:
        """Extract commit information"""
        # Get commit details
        commit_format = "%H%n%h%n%an%n%ae%n%at%n%s%n%b"
        commit_data = self._run_git_command([
            "git", "show", "-s", f"--format={commit_format}", self.commit_hash
        ]).split('\n')
        
        if len(commit_data) < 6:
            return {}
        
        # Get file statistics
        stat_output = self._run_git_command([
            "git", "show", "--stat", "--oneline", self.commit_hash
        ])
        
        # Get changed files
        files_changed = self._run_git_command([
            "git", "diff-tree", "--no-commit-id", "--name-only", "-r", self.commit_hash
        ]).split('\n')
        
        return {
            'hash': commit_data[0],
            'short_hash': commit_data[1],
            'author': commit_data[2],
            'email': commit_data[3],
            'timestamp': int(commit_data[4]),
            'subject': commit_data[5],
            'body': '\n'.join(commit_data[6:]) if len(commit_data) > 6 else '',
            'files_changed': [f for f in files_changed if f],
            'stats': stat_output
        }
    
    def should_generate_doc(self) -> bool:
        """Determine if this commit should generate documentation"""
        if not self.commit_info:
            return False
        
        # Skip if no files changed
        if not self.commit_info.get('files_changed'):
            return False
        
        # Skip merge commits (usually)
        if self.commit_info.get('subject', '').startswith('Merge'):
            return False
        
        # Skip if commit is only to auto-generated docs (prevent recursion)
        files = self.commit_info.get('files_changed', [])
        if all('auto-generated' in f or 'auto_doc_generator' in f for f in files):
            return False
        
        return True
    
    def categorize_commit(self) -> str:
        """Categorize commit type based on message and files"""
        subject = self.commit_info.get('subject', '').lower()
        
        if subject.startswith('feat'):
            return 'feature'
        elif subject.startswith('fix'):
            return 'bugfix'
        elif subject.startswith('refactor'):
            return 'refactor'
        elif subject.startswith('docs'):
            return 'documentation'
        elif subject.startswith('test'):
            return 'testing'
        elif subject.startswith('chore'):
            return 'maintenance'
        else:
            return 'change'
    
    def get_file_categories(self) -> Dict[str, List[str]]:
        """Categorize changed files by type"""
        categories = {
            'python': [],
            'javascript': [],
            'shell': [],
            'documentation': [],
            'configuration': [],
            'other': []
        }
        
        for file in self.commit_info.get('files_changed', []):
            if file.endswith('.py'):
                categories['python'].append(file)
            elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                categories['javascript'].append(file)
            elif file.endswith('.sh'):
                categories['shell'].append(file)
            elif file.endswith('.md'):
                categories['documentation'].append(file)
            elif file.endswith(('.json', '.yaml', '.yml', '.toml', '.ini')):
                categories['configuration'].append(file)
            else:
                categories['other'].append(file)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}


class DocumentationGenerator:
    """Generates markdown documentation from commit analysis"""
    
    def __init__(self, analyzer: CommitAnalyzer):
        self.analyzer = analyzer
        self.commit_info = analyzer.commit_info
        
    def generate(self) -> str:
        """Generate complete markdown documentation"""
        commit_type = self.analyzer.categorize_commit()
        file_categories = self.analyzer.get_file_categories()
        
        # Build markdown
        doc = []
        doc.append(f"# {self._get_title()}\n")
        doc.append(f"**Auto-Generated Documentation**\n")
        doc.append(f"**Date:** {self._format_timestamp()}")
        doc.append(f"**Commit:** `{self.commit_info['short_hash']}`")
        doc.append(f"**Type:** {commit_type.capitalize()}")
        doc.append(f"**Author:** {self.commit_info['author']}\n")
        doc.append("---\n")
        
        # Commit message
        doc.append("## 📝 Commit Message\n")
        doc.append(f"**{self.commit_info['subject']}**\n")
        if self.commit_info.get('body'):
            doc.append(self.commit_info['body'])
            doc.append("\n")
        
        # Files changed
        doc.append("## 📁 Files Changed\n")
        total_files = len(self.commit_info['files_changed'])
        doc.append(f"**Total:** {total_files} file(s)\n")
        
        for category, files in file_categories.items():
            doc.append(f"### {category.capitalize()} Files ({len(files)})\n")
            for file in files:
                doc.append(f"- `{file}`")
            doc.append("\n")
        
        # Statistics
        doc.append("## 📊 Statistics\n")
        doc.append("```")
        doc.append(self.commit_info['stats'])
        doc.append("```\n")
        
        # Metadata for Helena
        doc.append("## 🤖 Metadata\n")
        doc.append("```json")
        metadata = {
            "commit_hash": self.commit_info['hash'],
            "commit_type": commit_type,
            "timestamp": self.commit_info['timestamp'],
            "files_changed": self.commit_info['files_changed'],
            "auto_generated": True
        }
        doc.append(json.dumps(metadata, indent=2))
        doc.append("```\n")
        
        # Helena processing note
        doc.append("---")
        doc.append("*This document was automatically generated from a git commit.*")
        doc.append("*Helena will process this and add to all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis).*")
        
        return '\n'.join(doc)
    
    def _get_title(self) -> str:
        """Generate title for the document"""
        subject = self.commit_info['subject']
        # Remove conventional commit prefix for cleaner title
        for prefix in ['feat:', 'fix:', 'refactor:', 'docs:', 'test:', 'chore:']:
            if subject.lower().startswith(prefix):
                subject = subject[len(prefix):].strip()
                break
        return subject
    
    def _format_timestamp(self) -> str:
        """Format timestamp as readable date"""
        dt = datetime.fromtimestamp(self.commit_info['timestamp'])
        return dt.strftime('%Y-%m-%d %H:%M:%S')


def generate_doc_for_commit(commit_hash: str = "HEAD") -> Optional[Path]:
    """Main function to generate documentation for a commit"""
    
    print("🔍 Analyzing commit...")
    analyzer = CommitAnalyzer(commit_hash)
    
    if not analyzer.should_generate_doc():
        print("⏭️  Skipping - no documentation needed for this commit")
        return None
    
    print("📝 Generating documentation...")
    generator = DocumentationGenerator(analyzer)
    markdown = generator.generate()
    
    # Create output directory
    today = datetime.now().strftime('%Y-%m-%d')
    output_dir = AUTO_DOC_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    commit_type = analyzer.categorize_commit()
    short_hash = analyzer.commit_info['short_hash']
    filename = f"COMMIT_{short_hash}_{commit_type}.md"
    output_path = output_dir / filename
    
    # Write file
    output_path.write_text(markdown)
    
    print(f"✅ Documentation generated: {output_path}")
    print(f"👁️  Helena will detect and process this within 2-3 seconds...")
    
    return output_path


if __name__ == "__main__":
    # Get commit hash from args or use HEAD
    commit_hash = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     🤖 Automatic Documentation Generator                    ║")
    print("║     Git Commit → Markdown → Helena → Databases              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    try:
        output_path = generate_doc_for_commit(commit_hash)
        if output_path:
            print()
            print("🎉 SUCCESS! Knowledge propagation pipeline activated.")
            sys.exit(0)
        else:
            print()
            print("ℹ️  No documentation generated (not needed for this commit)")
            sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
