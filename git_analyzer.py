#!/usr/bin/env python3
"""
Git Commit Analyzer
Analyzes git commit history and generates insights

Created by: Destiny Team Framework
- Requirements: Magdalena Kowalska
- Architecture: Katarzyna Wiśniewska  
- Data Analysis: Dr. Joanna Wójcik
- Implementation: Tomasz Zieliński
"""

import subprocess
import sys
import argparse
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import os


@dataclass
class Commit:
    """Represents a single git commit"""
    hash: str
    author: str
    date: datetime
    message: str
    files_changed: int = 0


@dataclass
class AnalysisResults:
    """Results of commit analysis"""
    total_commits: int
    authors: Dict[str, int]  # author -> commit count
    timeline: Dict[str, int]  # date -> commits
    top_contributors: List[Tuple[str, int]]
    date_range: Tuple[datetime, datetime]


class GitLogParser:
    """Parses git log output into structured data"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def parse(self, limit: int = None) -> List[Commit]:
        """
        Parse git log and return list of commits
        
        Args:
            limit: Maximum number of commits to parse (None = all)
            
        Returns:
            List of Commit objects
        """
        try:
            # Build git log command
            cmd = [
                "git",
                "-C", self.repo_path,
                "log",
                "--pretty=format:%H|%an|%ai|%s",
                "--numstat"
            ]
            
            if limit:
                cmd.append(f"-{limit}")
            
            # Execute git log
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output
            commits = []
            lines = result.stdout.strip().split('\n')
            
            current_commit = None
            files_count = 0
            
            for line in lines:
                if '|' in line and not line.startswith('\t'):
                    # Commit line
                    if current_commit:
                        current_commit.files_changed = files_count
                        commits.append(current_commit)
                        files_count = 0
                    
                    parts = line.split('|')
                    if len(parts) >= 4:
                        hash_val, author, date_str, message = parts[0], parts[1], parts[2], parts[3]
                        
                        try:
                            date = datetime.fromisoformat(date_str.replace(' +', '+').replace(' -', '-'))
                        except:
                            date = datetime.now()
                        
                        current_commit = Commit(
                            hash=hash_val,
                            author=author,
                            date=date,
                            message=message
                        )
                elif line.strip() and current_commit:
                    # File change line
                    files_count += 1
            
            # Don't forget last commit
            if current_commit:
                current_commit.files_changed = files_count
                commits.append(current_commit)
            
            return commits
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: Not a git repository or git not found", file=sys.stderr)
            print(f"   Make sure you're in a git repository", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error parsing git log: {e}", file=sys.stderr)
            sys.exit(1)


class DataAnalyzer:
    """Analyzes commit data and calculates metrics"""
    
    def analyze(self, commits: List[Commit]) -> AnalysisResults:
        """
        Analyze commits and generate metrics
        
        Args:
            commits: List of Commit objects
            
        Returns:
            AnalysisResults object with metrics
        """
        if not commits:
            return AnalysisResults(
                total_commits=0,
                authors={},
                timeline={},
                top_contributors=[],
                date_range=(datetime.now(), datetime.now())
            )
        
        # Count commits per author
        author_counts = Counter(commit.author for commit in commits)
        
        # Count commits per day
        timeline = defaultdict(int)
        for commit in commits:
            date_key = commit.date.strftime("%Y-%m-%d")
            timeline[date_key] += 1
        
        # Top contributors
        top_contributors = author_counts.most_common(10)
        
        # Date range
        dates = [commit.date for commit in commits]
        date_range = (min(dates), max(dates))
        
        return AnalysisResults(
            total_commits=len(commits),
            authors=dict(author_counts),
            timeline=dict(timeline),
            top_contributors=top_contributors,
            date_range=date_range
        )


class ReportGenerator:
    """Generates human-readable reports"""
    
    def generate(self, results: AnalysisResults) -> str:
        """
        Generate formatted report
        
        Args:
            results: AnalysisResults object
            
        Returns:
            Formatted report string
        """
        if results.total_commits == 0:
            return "No commits found."
        
        lines = []
        lines.append("=" * 70)
        lines.append(" " * 20 + "GIT COMMIT ANALYSIS REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("📊 SUMMARY")
        lines.append("─" * 70)
        lines.append(f"Total Commits:      {results.total_commits:,}")
        lines.append(f"Contributors:       {len(results.authors)}")
        lines.append(f"Date Range:         {results.date_range[0].strftime('%Y-%m-%d')} to {results.date_range[1].strftime('%Y-%m-%d')}")
        
        days = (results.date_range[1] - results.date_range[0]).days + 1
        lines.append(f"Duration:           {days} days")
        lines.append(f"Avg Commits/Day:    {results.total_commits / max(days, 1):.1f}")
        lines.append("")
        
        # Top Contributors
        lines.append("👥 TOP CONTRIBUTORS")
        lines.append("─" * 70)
        
        for i, (author, count) in enumerate(results.top_contributors[:10], 1):
            percentage = (count / results.total_commits) * 100
            bar_length = int(count / (results.total_commits / 40))
            bar = "█" * bar_length
            
            # Mark core contributors (>10%)
            marker = "⭐" if percentage > 10 else "  "
            
            lines.append(f"{marker} {i:2}. {author:30} {count:4} commits ({percentage:5.1f}%) {bar}")
        
        lines.append("")
        lines.append("⭐ = Core contributor (>10% of commits)")
        lines.append("")
        
        # Activity Timeline (last 30 days)
        lines.append("📈 RECENT ACTIVITY (Last 30 Days)")
        lines.append("─" * 70)
        
        # Get last 30 days
        sorted_dates = sorted(results.timeline.keys(), reverse=True)[:30]
        if sorted_dates:
            max_commits = max(results.timeline[d] for d in sorted_dates)
            
            for date in reversed(sorted_dates[-10:]):  # Show last 10 days
                count = results.timeline[date]
                bar_length = int(count / max(max_commits, 1) * 30)
                bar = "█" * bar_length
                lines.append(f"{date}: {count:3} {bar}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Analyze git commit history and generate insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Analyze current repository
  %(prog)s --repo /path/to/repo  # Analyze specific repository
  %(prog)s --limit 100        # Analyze last 100 commits
  
Created by: Destiny Team Framework
        """
    )
    
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of commits to analyze (default: all)"
    )
    
    parser.add_argument(
        "--output",
        help="Save report to file (default: print to console)"
    )
    
    args = parser.parse_args()
    
    # Check if repo exists
    if not os.path.exists(args.repo):
        print(f"❌ Error: Repository path does not exist: {args.repo}", file=sys.stderr)
        sys.exit(1)
    
    print("🔍 Analyzing git commits...")
    print(f"   Repository: {os.path.abspath(args.repo)}")
    if args.limit:
        print(f"   Limit: {args.limit} commits")
    print()
    
    # Pipeline execution
    try:
        # Stage 1: Parse
        parser_obj = GitLogParser(args.repo)
        commits = parser_obj.parse(limit=args.limit)
        print(f"✅ Parsed {len(commits):,} commits")
        
        # Stage 2: Analyze
        analyzer = DataAnalyzer()
        results = analyzer.analyze(commits)
        print(f"✅ Analyzed {len(results.authors)} contributors")
        
        # Stage 3: Report
        generator = ReportGenerator()
        report = generator.generate(results)
        print(f"✅ Generated report")
        print()
        
        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.output}")
        else:
            print(report)
        
    except KeyboardInterrupt:
        print("\n\n❌ Analysis interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
