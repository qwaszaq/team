"""
Analyze Evaluation Feedback - Generate Action Plan

Usage:
    python3 analyze_evaluation.py EVALUATION_FEEDBACK_John.md

This script will:
1. Parse the evaluation feedback markdown
2. Extract scores, verdict, strengths, weaknesses
3. Categorize issues by severity and effort
4. Generate prioritized action plan
5. Recommend next steps

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_evaluation_file(filepath: str) -> Dict:
    """Parse evaluation feedback markdown file"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    data = {
        'filepath': filepath,
        'evaluator': 'Unknown',
        'total_score': None,
        'phase_scores': {},
        'verdict': 'Unknown',
        'strengths': [],
        'weaknesses': [],
        'comments': [],
        'recommendation': 'Unknown'
    }
    
    # Extract evaluator name from filename
    filename = Path(filepath).stem
    if 'EVALUATION_FEEDBACK_' in filename:
        data['evaluator'] = filename.replace('EVALUATION_FEEDBACK_', '')
    
    # Extract total score
    score_match = re.search(r'TOTAL:\s*(\d+)\s*/\s*20', content)
    if score_match:
        data['total_score'] = int(score_match.group(1))
    
    # Extract phase scores
    phase_matches = re.findall(r'Score Phase (\d+):.*?(\d+)\s*/\s*5', content)
    for phase_num, score in phase_matches:
        data['phase_scores'][f'phase_{phase_num}'] = int(score)
    
    # Extract verdict
    verdict_patterns = [
        r'Do you believe this is a REAL multi-agent.*?\[X\]\s*Strongly agree',
        r'Do you believe this is a REAL multi-agent.*?\[X\]\s*Agree',
        r'verdict.*?real',
        r'verdict.*?theatrical'
    ]
    for pattern in verdict_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            if 'strongly agree' in content.lower() or 'definitely' in content.lower():
                data['verdict'] = 'Real - Strong'
                break
            elif 'agree' in content.lower() or 'yes' in content.lower():
                data['verdict'] = 'Real - Moderate'
                break
            elif 'theatrical' in content.lower():
                data['verdict'] = 'Theatrical'
                break
    
    # Extract strengths
    strength_section = re.search(r'TOP 3 STRENGTHS.*?\n\n(.*?)\n\n', content, re.DOTALL)
    if strength_section:
        strengths_text = strength_section.group(1)
        strengths = re.findall(r'\d+\.\s*(.+)', strengths_text)
        data['strengths'] = [s.strip() for s in strengths if s.strip()]
    
    # Extract weaknesses
    weakness_section = re.search(r'TOP 3 WEAKNESSES.*?\n\n(.*?)\n\n', content, re.DOTALL)
    if weakness_section:
        weaknesses_text = weakness_section.group(1)
        weaknesses = re.findall(r'\d+\.\s*(.+)', weaknesses_text)
        data['weaknesses'] = [w.strip() for w in weaknesses if w.strip()]
    
    # Extract overall recommendation
    rec_match = re.search(r'\[X\]\s*(🏆 Excellent|👍 Good|😐 Okay|👎 Weak|❌ Poor)', content)
    if rec_match:
        data['recommendation'] = rec_match.group(1)
    
    return data


def categorize_score(score: int) -> Tuple[str, str, str]:
    """Categorize score and return (category, action, timeline)"""
    
    if score >= 18:
        return ('EXCELLENT', 'Celebrate + Minor polish', '1-2 hours')
    elif score >= 15:
        return ('GOOD', 'Fix high-priority issues', '3-5 hours')
    elif score >= 12:
        return ('ACCEPTABLE', 'Moderate rework', '1-2 days')
    elif score >= 9:
        return ('WEAK', 'Major rework', '3-5 days')
    else:
        return ('POOR', 'Reassess approach', '1-2 weeks')


def categorize_issues(weaknesses: List[str]) -> Dict[str, List[str]]:
    """Categorize weaknesses by severity"""
    
    categories = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': [],
        'quick_wins': []
    }
    
    # Keywords for categorization
    critical_keywords = ['fundamental', 'broken', 'doesn\'t work', 'not real', 'theatrical']
    high_keywords = ['improvement', 'enhance', 'should', 'missing']
    quick_win_keywords = ['documentation', 'comment', 'format', 'naming']
    
    for weakness in weaknesses:
        weakness_lower = weakness.lower()
        
        if any(kw in weakness_lower for kw in critical_keywords):
            categories['critical'].append(weakness)
        elif any(kw in weakness_lower for kw in high_keywords):
            categories['high'].append(weakness)
        elif any(kw in weakness_lower for kw in quick_win_keywords):
            categories['quick_wins'].append(weakness)
        else:
            categories['medium'].append(weakness)
    
    return categories


def generate_action_plan(data: Dict, categorized: Dict) -> List[str]:
    """Generate prioritized action plan"""
    
    score = data['total_score']
    actions = []
    
    if score >= 18:
        actions.append("🎉 CELEBRATE - Score 18+/20!")
        actions.append("1. Update PROJECT_STATUS_FINAL.md with evaluation results")
        actions.append("2. Add evaluation score to README_QUICK_DEMO.md")
        if categorized['quick_wins']:
            actions.append("3. (Optional) Fix quick wins:")
            for qw in categorized['quick_wins']:
                actions.append(f"   - {qw}")
        actions.append("4. Prepare presentation - READY NOW! ✅")
    
    elif score >= 15:
        actions.append("👍 GOOD SCORE - Fix high-priority items")
        actions.append("1. Address high-priority issues:")
        for issue in categorized['critical'] + categorized['high']:
            actions.append(f"   - {issue}")
        actions.append("2. Implement quick wins:")
        for qw in categorized['quick_wins']:
            actions.append(f"   - {qw}")
        actions.append("3. Re-test: python3 test_quick_demo.py")
        actions.append("4. Update documentation")
        actions.append("5. Consider re-evaluation (optional)")
        actions.append("6. Ready to present after fixes (3-5h)")
    
    elif score >= 12:
        actions.append("😐 ACCEPTABLE - Moderate rework needed")
        actions.append("1. Team meeting to review feedback (1h)")
        actions.append("2. Fix all critical issues:")
        for issue in categorized['critical']:
            actions.append(f"   - {issue}")
        actions.append("3. Fix high-priority issues:")
        for issue in categorized['high']:
            actions.append(f"   - {issue}")
        actions.append("4. Consider medium-priority items")
        actions.append("5. Add new tests if needed")
        actions.append("6. Re-test all functionality")
        actions.append("7. Re-evaluate (recommended)")
        actions.append("8. Timeline: 1-2 days")
    
    elif score >= 9:
        actions.append("👎 WEAK - Major rework required")
        actions.append("1. Critical team review meeting (2h)")
        actions.append("2. Identify root causes of low score")
        actions.append("3. Decide: Rework or pivot?")
        actions.append("4. If rework:")
        actions.append("   - Redesign agent logic")
        actions.append("   - Enhance differentiation")
        actions.append("   - Improve demo scenarios")
        actions.append("5. Timeline: 3-5 days")
        actions.append("6. Re-evaluation mandatory")
    
    else:
        actions.append("❌ POOR - Reassess approach")
        actions.append("1. STOP - Full retrospective (1 day)")
        actions.append("2. Read feedback multiple times")
        actions.append("3. Honest assessment: Is approach correct?")
        actions.append("4. Options:")
        actions.append("   A. Restart with new architecture")
        actions.append("   B. Accept limitations, pivot")
        actions.append("   C. Get second opinion")
        actions.append("5. Timeline: 1-2 weeks (if restart)")
    
    return actions


def print_report(data: Dict):
    """Print formatted analysis report"""
    
    print("\n" + "="*80)
    print("EVALUATION ANALYSIS REPORT")
    print("="*80)
    print()
    
    # Header
    print(f"📄 Feedback File: {data['filepath']}")
    print(f"👤 Evaluator: {data['evaluator']}")
    print()
    
    # Score
    score = data['total_score']
    if score:
        category, action, timeline = categorize_score(score)
        stars = '⭐' * (score // 4)
        
        print("━" * 80)
        print(f"📊 TOTAL SCORE: {score}/20")
        print(f"   Rating: {stars} {category}")
        print(f"   Action: {action}")
        print(f"   Timeline: {timeline}")
        print("━" * 80)
        print()
    
    # Phase scores
    if data['phase_scores']:
        print("Phase Scores:")
        for phase, pscore in sorted(data['phase_scores'].items()):
            print(f"  {phase.replace('_', ' ').title()}: {pscore}/5")
        print()
    
    # Verdict
    print(f"🎯 VERDICT: {data['verdict']}")
    print()
    
    # Strengths
    if data['strengths']:
        print("✅ STRENGTHS (Top 3):")
        for i, strength in enumerate(data['strengths'][:3], 1):
            print(f"  {i}. {strength}")
        print()
    
    # Weaknesses
    if data['weaknesses']:
        print("⚠️  WEAKNESSES (Top 3):")
        for i, weakness in enumerate(data['weaknesses'][:3], 1):
            print(f"  {i}. {weakness}")
        print()
        
        # Categorize
        categorized = categorize_issues(data['weaknesses'])
        
        print("Issue Categorization:")
        print(f"  Critical:   {len(categorized['critical'])} issues (MUST FIX)")
        print(f"  High:       {len(categorized['high'])} issues (Should fix)")
        print(f"  Medium:     {len(categorized['medium'])} issues (Nice to have)")
        print(f"  Quick Wins: {len(categorized['quick_wins'])} issues (Easy + impactful)")
        print()
    
    # Recommendation
    print(f"💡 RECOMMENDATION: {data['recommendation']}")
    print()
    
    # Action Plan
    if score:
        categorized = categorize_issues(data['weaknesses'])
        actions = generate_action_plan(data, categorized)
        
        print("━" * 80)
        print("🎯 RECOMMENDED ACTION PLAN:")
        print("━" * 80)
        for action in actions:
            print(action)
        print()
    
    # Next Steps
    print("━" * 80)
    print("📋 IMMEDIATE NEXT STEPS:")
    print("━" * 80)
    print("1. [ ] Review this analysis with team")
    print("2. [ ] Prioritize action items")
    print("3. [ ] Create fix branches (if needed)")
    print("4. [ ] Implement fixes")
    print("5. [ ] Re-test all functionality")
    print("6. [ ] Update documentation")
    print("7. [ ] Consider re-evaluation (if score < 18)")
    print("8. [ ] Prepare presentation (if score >= 15)")
    print()
    
    # Decision
    if score:
        print("━" * 80)
        print("🎬 PRESENTATION DECISION:")
        print("━" * 80)
        if score >= 18:
            print("✅ READY TO PRESENT NOW!")
            print("   Minor polish optional, but system is proven.")
        elif score >= 15:
            print("✅ READY TO PRESENT (after high-priority fixes)")
            print("   Timeline: 3-5 hours of fixes, then ready.")
        elif score >= 12:
            print("⚠️  NOT READY - Need 1-2 days of improvements")
            print("   Consider presenting as 'work in progress'")
        else:
            print("❌ NOT READY TO PRESENT")
            print("   Major work required before showing to stakeholders.")
        print()
    
    print("="*80)
    print("END OF ANALYSIS")
    print("="*80)
    print()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_evaluation.py EVALUATION_FEEDBACK_Name.md")
        print()
        print("Example:")
        print("  python3 analyze_evaluation.py EVALUATION_FEEDBACK_John.md")
        sys.exit(1)
    
    feedback_file = sys.argv[1]
    
    if not Path(feedback_file).exists():
        print(f"❌ Error: File not found: {feedback_file}")
        sys.exit(1)
    
    print(f"\n🔍 Analyzing evaluation feedback...")
    print(f"   File: {feedback_file}")
    print()
    
    try:
        data = parse_evaluation_file(feedback_file)
        print_report(data)
        
        # Save report
        report_file = f"ANALYSIS_{Path(feedback_file).stem}.md"
        print(f"💾 Saving analysis to: {report_file}")
        
        # TODO: Could save formatted markdown report here
        
        print("✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error analyzing feedback: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
