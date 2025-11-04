"""
Supervisor Interface - Quality Assurance for Local LLM
Aleksander (Claude) reviews local LLM work and provides guidance

Responsibilities:
- Review investigation logs from local LLM
- Assess tool usage quality
- Check source attribution compliance
- Evaluate analytical rigor
- Provide guidance for improvements
- Synthesize final professional reports
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter


class SupervisorInterface:
    """
    Interface for cloud supervisor (Aleksander/Claude) to review local LLM work
    
    Reviews:
    - LMStudio logs (what did local LLM do?)
    - Tool usage patterns (did it use right tools?)
    - Output quality (is analysis sound?)
    - Source attribution compliance (are sources cited and archived?)
    - Statistical validity (are calculations correct?)
    
    Provides:
    - Quality assessment report
    - Guidance for next steps
    - Corrections if needed
    - Final report synthesis
    """
    
    def __init__(self, workspace_dir: str = "./shared_workspace"):
        """
        Initialize Supervisor Interface
        
        Args:
            workspace_dir: Shared workspace for communication with local LLM
        """
        self.workspace_dir = Path(workspace_dir)
        self.log_dir = Path("./logs/local_llm")
        
        # Ensure directories exist
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ SupervisorInterface initialized")
        print(f"   Workspace: {self.workspace_dir}")
        print(f"   Logs: {self.log_dir}")
    
    def list_pending_investigations(self) -> List[Dict]:
        """
        List all investigations waiting for supervisor review
        
        Returns:
            [{
                "investigation_id": "...",
                "result_file": Path,
                "log_file": Path,
                "timestamp": "..."
            }, ...]
        """
        results_dir = self.workspace_dir / "results"
        
        if not results_dir.exists():
            return []
        
        investigations = []
        
        for result_file in sorted(results_dir.glob("result_*.json")):
            # Load result
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            # Find corresponding log file
            investigation_id = result.get("investigation_id", "unknown")
            log_file = Path(result.get("log_file", ""))
            
            if log_file.exists():
                investigations.append({
                    "investigation_id": investigation_id,
                    "result_file": result_file,
                    "log_file": log_file,
                    "timestamp": result.get("timestamp", "")
                })
        
        return investigations
    
    def read_investigation_log(self, log_file: Path) -> List[Dict]:
        """
        Read JSONL log file from local LLM
        
        Returns:
            List of action dictionaries
        """
        actions = []
        
        if not log_file.exists():
            return actions
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        actions.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return actions
    
    def read_investigation_result(self, result_file: Path) -> Dict:
        """Read investigation result JSON"""
        with open(result_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_tool_usage(self, actions: List[Dict]) -> Dict:
        """
        Analyze how local LLM used tools
        
        Checks:
        - Which tools were used?
        - How many times?
        - Were appropriate tools used?
        - Any tools missing that should have been used?
        - Any tool errors?
        
        Returns:
            {
                "total_tool_calls": N,
                "tools_used": {"tool_name": count, ...},
                "tool_errors": N,
                "patterns": [
                    {"issue": "...", "severity": "...", "description": "..."},
                    ...
                ],
                "assessment": "excellent" | "good" | "needs_improvement" | "poor"
            }
        """
        tool_calls = [a for a in actions if a.get("type") == "tool_execution"]
        tool_errors = [a for a in actions if a.get("type") == "tool_error"]
        
        analysis = {
            "total_tool_calls": len(tool_calls),
            "tools_used": {},
            "tool_errors": len(tool_errors),
            "error_details": tool_errors,
            "patterns": []
        }
        
        # Count tool usage
        for call in tool_calls:
            tool_name = call.get("tool")
            analysis["tools_used"][tool_name] = analysis["tools_used"].get(tool_name, 0) + 1
        
        # Pattern detection
        
        # Issue 1: Scraping without archiving
        scrapes = analysis["tools_used"].get("scrape_webpage", 0)
        archives = analysis["tools_used"].get("archive_source", 0)
        
        if scrapes > 0 and archives == 0:
            analysis["patterns"].append({
                "issue": "scraping_without_archiving",
                "severity": "high",
                "description": f"Local LLM scraped {scrapes} page(s) but archived 0 sources. SOURCE ATTRIBUTION PROTOCOL violation!"
            })
        elif scrapes > archives:
            analysis["patterns"].append({
                "issue": "incomplete_archiving",
                "severity": "medium",
                "description": f"Local LLM scraped {scrapes} page(s) but only archived {archives}. Some sources not preserved."
            })
        
        # Issue 2: Missing statistical analysis when numbers present
        stats_calls = analysis["tools_used"].get("calculate_statistics", 0)
        
        # Check if any scraped content might have contained numbers
        # (This is a heuristic - can't perfectly detect from logs)
        if scrapes > 3 and stats_calls == 0:
            analysis["patterns"].append({
                "issue": "potential_missing_statistics",
                "severity": "low",
                "description": "Multiple pages scraped but no statistical analysis performed. Consider if numerical data was available."
            })
        
        # Issue 3: Tool errors
        if len(tool_errors) > 0:
            analysis["patterns"].append({
                "issue": "tool_errors",
                "severity": "medium",
                "description": f"{len(tool_errors)} tool error(s) occurred. Check error handling."
            })
        
        # Overall assessment
        if len(analysis["patterns"]) == 0:
            analysis["assessment"] = "excellent"
        elif any(p["severity"] == "high" for p in analysis["patterns"]):
            analysis["assessment"] = "needs_improvement"
        elif len(analysis["patterns"]) > 2:
            analysis["assessment"] = "needs_improvement"
        else:
            analysis["assessment"] = "good"
        
        return analysis
    
    def assess_source_quality(self, actions: List[Dict]) -> Dict:
        """
        Assess source attribution quality
        
        Checks:
        - Are sources cited?
        - Are sources archived?
        - Archive ratio (archived / scraped)
        - Compliance with SOURCE ATTRIBUTION PROTOCOL
        
        Returns:
            {
                "sources_scraped": N,
                "sources_archived": N,
                "archive_ratio": 0.0-1.0,
                "compliance": "excellent" | "good" | "needs_improvement" | "poor",
                "grade": "A+" | "A" | "B" | "C" | "F"
            }
        """
        archive_calls = [a for a in actions if a.get("tool") == "archive_source"]
        scrape_calls = [a for a in actions if a.get("tool") == "scrape_webpage"]
        
        sources_scraped = len(scrape_calls)
        sources_archived = len(archive_calls)
        archive_ratio = sources_archived / sources_scraped if sources_scraped > 0 else 0
        
        # Determine compliance level
        if archive_ratio >= 1.0:
            compliance = "excellent"
            grade = "A+"
        elif archive_ratio >= 0.8:
            compliance = "good"
            grade = "A"
        elif archive_ratio >= 0.5:
            compliance = "needs_improvement"
            grade = "B"
        elif archive_ratio > 0:
            compliance = "poor"
            grade = "C"
        else:
            compliance = "poor"
            grade = "F"
        
        return {
            "sources_scraped": sources_scraped,
            "sources_archived": sources_archived,
            "archive_ratio": archive_ratio,
            "compliance": compliance,
            "grade": grade,
            "protocol_compliant": archive_ratio >= 1.0
        }
    
    def analyze_investigation_flow(self, actions: List[Dict]) -> Dict:
        """
        Analyze investigation execution flow
        
        Returns:
            {
                "llm_calls": N,
                "iterations": N,
                "total_tokens": N,
                "action_breakdown": {"action_type": count, ...},
                "efficiency": "high" | "medium" | "low"
            }
        """
        llm_calls = [a for a in actions if a.get("type") == "llm_call"]
        llm_responses = [a for a in actions if a.get("type") == "llm_response"]
        
        # Calculate total tokens
        total_tokens = sum(
            r.get("usage", {}).get("total_tokens", 0)
            for r in llm_responses
        )
        
        # Action breakdown
        action_types = Counter(a.get("type") for a in actions)
        
        # Estimate efficiency
        iterations = len(llm_calls)
        tool_calls = action_types.get("tool_execution", 0)
        
        if iterations <= 5 and tool_calls >= 3:
            efficiency = "high"
        elif iterations <= 10:
            efficiency = "medium"
        else:
            efficiency = "low"
        
        return {
            "llm_calls": len(llm_calls),
            "iterations": iterations,
            "total_tokens": total_tokens,
            "action_breakdown": dict(action_types),
            "efficiency": efficiency,
            "avg_tokens_per_call": total_tokens / len(llm_responses) if llm_responses else 0
        }
    
    def generate_quality_report(
        self,
        investigation_id: str
    ) -> Dict:
        """
        Generate comprehensive quality assessment report
        
        This is Aleksander's (Claude's) full review of local LLM work
        
        Args:
            investigation_id: ID of investigation to review
        
        Returns:
            Comprehensive quality report
        """
        # Find files
        result_file = self.workspace_dir / "results" / f"result_{investigation_id}.json"
        
        if not result_file.exists():
            return {"error": f"Result file not found for investigation {investigation_id}"}
        
        # Load result
        result = self.read_investigation_result(result_file)
        
        # Load log
        log_file = Path(result.get("log_file", ""))
        if not log_file.exists():
            return {"error": f"Log file not found: {log_file}"}
        
        actions = self.read_investigation_log(log_file)
        
        # Analyze
        tool_analysis = self.analyze_tool_usage(actions)
        source_assessment = self.assess_source_quality(actions)
        flow_analysis = self.analyze_investigation_flow(actions)
        
        # Overall assessment
        grades = {
            "tool_usage": tool_analysis["assessment"],
            "source_attribution": source_assessment["compliance"],
            "efficiency": flow_analysis["efficiency"]
        }
        
        # Calculate overall grade
        grade_scores = {
            "excellent": 5,
            "high": 5,
            "good": 4,
            "medium": 3,
            "needs_improvement": 2,
            "low": 2,
            "poor": 1
        }
        
        avg_score = sum(grade_scores.get(g, 0) for g in grades.values()) / len(grades)
        
        if avg_score >= 4.5:
            overall_grade = "A+"
        elif avg_score >= 4:
            overall_grade = "A"
        elif avg_score >= 3:
            overall_grade = "B"
        elif avg_score >= 2:
            overall_grade = "C"
        else:
            overall_grade = "F"
        
        # Compile report
        report = {
            "investigation_id": investigation_id,
            "timestamp": datetime.now().isoformat(),
            "supervisor": "Aleksander (Claude Sonnet 4.5)",
            "review_type": "comprehensive_quality_assessment",
            
            "execution_metrics": {
                "status": result.get("status"),
                "iterations": result.get("iterations"),
                "llm_calls": flow_analysis["llm_calls"],
                "total_tokens": flow_analysis["total_tokens"],
                "actions_taken": len(actions),
                "efficiency": flow_analysis["efficiency"]
            },
            
            "tool_usage": {
                "total_calls": tool_analysis["total_tool_calls"],
                "tools_used": tool_analysis["tools_used"],
                "errors": tool_analysis["tool_errors"],
                "patterns": tool_analysis["patterns"],
                "assessment": tool_analysis["assessment"]
            },
            
            "source_quality": {
                "scraped": source_assessment["sources_scraped"],
                "archived": source_assessment["sources_archived"],
                "archive_ratio": source_assessment["archive_ratio"],
                "compliance": source_assessment["compliance"],
                "grade": source_assessment["grade"],
                "protocol_compliant": source_assessment["protocol_compliant"]
            },
            
            "overall_assessment": {
                "overall_grade": overall_grade,
                "component_grades": grades,
                "ready_for_publication": overall_grade in ["A+", "A"] and source_assessment["protocol_compliant"]
            },
            
            "findings": {
                "strengths": [],
                "weaknesses": [],
                "recommendations": []
            }
        }
        
        # Identify strengths
        if tool_analysis["assessment"] in ["excellent", "good"]:
            report["findings"]["strengths"].append("Appropriate tool usage")
        
        if source_assessment["protocol_compliant"]:
            report["findings"]["strengths"].append("Full SOURCE ATTRIBUTION PROTOCOL compliance")
        
        if flow_analysis["efficiency"] == "high":
            report["findings"]["strengths"].append("Efficient investigation (few iterations)")
        
        # Identify weaknesses
        for pattern in tool_analysis["patterns"]:
            report["findings"]["weaknesses"].append(f"{pattern['severity'].upper()}: {pattern['description']}")
        
        if not source_assessment["protocol_compliant"]:
            report["findings"]["weaknesses"].append("CRITICAL: Source attribution incomplete")
        
        # Recommendations
        if not source_assessment["protocol_compliant"]:
            report["findings"]["recommendations"].append(
                "Archive all scraped sources using archive_source tool"
            )
        
        if tool_analysis["tool_errors"] > 0:
            report["findings"]["recommendations"].append(
                f"Fix {tool_analysis['tool_errors']} tool error(s) - check error handling"
            )
        
        if flow_analysis["efficiency"] == "low":
            report["findings"]["recommendations"].append(
                "Improve efficiency - too many LLM iterations. Consider better planning."
            )
        
        # Save report
        report_file = self.workspace_dir / "reports" / f"quality_report_{investigation_id}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def create_guidance(
        self,
        investigation_id: str,
        guidance_text: str,
        priority: str = "normal",
        specific_actions: Optional[List[str]] = None
    ) -> Dict:
        """
        Create guidance document for local LLM
        
        Aleksander provides:
        - Strategic direction
        - Corrections
        - Additional tasks
        - Quality feedback
        
        Args:
            investigation_id: Investigation to guide
            guidance_text: Guidance message
            priority: "low" | "normal" | "high" | "critical"
            specific_actions: List of specific actions to take
        
        Returns:
            Guidance document
        """
        guidance = {
            "investigation_id": investigation_id,
            "timestamp": datetime.now().isoformat(),
            "supervisor": "Aleksander",
            "priority": priority,
            "guidance": guidance_text,
            "specific_actions": specific_actions or [],
            "status": "pending_implementation"
        }
        
        # Save guidance
        guidance_dir = self.workspace_dir / "guidance"
        guidance_dir.mkdir(exist_ok=True)
        
        guidance_file = guidance_dir / f"guidance_{investigation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(guidance_file, 'w', encoding='utf-8') as f:
            json.dump(guidance, f, indent=2, ensure_ascii=False)
        
        return guidance
    
    def print_quality_report(self, report: Dict):
        """Print quality report in readable format"""
        print("\n" + "="*70)
        print("📊 SUPERVISOR QUALITY REPORT")
        print("="*70)
        print(f"Investigation ID: {report['investigation_id']}")
        print(f"Supervisor: {report['supervisor']}")
        print(f"Timestamp: {report['timestamp']}")
        print()
        
        # Overall grade
        overall = report['overall_assessment']
        grade = overall['overall_grade']
        ready = overall['ready_for_publication']
        
        print(f"{'='*70}")
        print(f"OVERALL GRADE: {grade}")
        print(f"Ready for Publication: {'✅ YES' if ready else '❌ NO'}")
        print(f"{'='*70}")
        print()
        
        # Execution metrics
        exec_metrics = report['execution_metrics']
        print("📈 Execution Metrics:")
        print(f"   Status: {exec_metrics['status']}")
        print(f"   Iterations: {exec_metrics['iterations']}")
        print(f"   LLM Calls: {exec_metrics['llm_calls']}")
        print(f"   Total Tokens: {exec_metrics['total_tokens']:,}")
        print(f"   Efficiency: {exec_metrics['efficiency'].upper()}")
        print()
        
        # Tool usage
        tool_usage = report['tool_usage']
        print("🔧 Tool Usage:")
        print(f"   Total Calls: {tool_usage['total_calls']}")
        print(f"   Tools: {tool_usage['tools_used']}")
        print(f"   Errors: {tool_usage['errors']}")
        print(f"   Assessment: {tool_usage['assessment'].upper()}")
        if tool_usage['patterns']:
            print("   Issues:")
            for pattern in tool_usage['patterns']:
                print(f"      - [{pattern['severity'].upper()}] {pattern['description']}")
        print()
        
        # Source quality
        source = report['source_quality']
        print("📚 Source Quality:")
        print(f"   Scraped: {source['scraped']}")
        print(f"   Archived: {source['archived']}")
        print(f"   Archive Ratio: {source['archive_ratio']:.1%}")
        print(f"   Compliance: {source['compliance'].upper()}")
        print(f"   Grade: {source['grade']}")
        print(f"   Protocol Compliant: {'✅' if source['protocol_compliant'] else '❌'}")
        print()
        
        # Findings
        findings = report['findings']
        
        if findings['strengths']:
            print("✅ Strengths:")
            for strength in findings['strengths']:
                print(f"   • {strength}")
            print()
        
        if findings['weaknesses']:
            print("⚠️  Weaknesses:")
            for weakness in findings['weaknesses']:
                print(f"   • {weakness}")
            print()
        
        if findings['recommendations']:
            print("💡 Recommendations:")
            for rec in findings['recommendations']:
                print(f"   • {rec}")
            print()
        
        print("="*70)


def main():
    """
    Example: Supervisor reviews local LLM investigation
    """
    print("🎯 SUPERVISOR INTERFACE - Quality Assurance")
    print("="*70)
    
    supervisor = SupervisorInterface()
    
    # List pending investigations
    pending = supervisor.list_pending_investigations()
    
    print(f"\n📋 Pending Investigations: {len(pending)}")
    
    if not pending:
        print("   (No investigations to review yet)")
        print()
        print("💡 Run local_orchestrator.py first to create investigations")
        return
    
    # Review each investigation
    for inv in pending:
        investigation_id = inv["investigation_id"]
        
        print(f"\n{'='*70}")
        print(f"🔍 Reviewing: {investigation_id}")
        print(f"{'='*70}")
        
        # Generate quality report
        report = supervisor.generate_quality_report(investigation_id)
        
        if "error" in report:
            print(f"❌ Error: {report['error']}")
            continue
        
        # Print report
        supervisor.print_quality_report(report)
        
        # Provide guidance if needed
        if not report['overall_assessment']['ready_for_publication']:
            guidance = supervisor.create_guidance(
                investigation_id=investigation_id,
                guidance_text="Investigation needs improvement before publication. See quality report for specific issues.",
                priority="high",
                specific_actions=report['findings']['recommendations']
            )
            
            print(f"\n📝 Guidance created for local LLM")
            print(f"   Priority: {guidance['priority']}")
            print(f"   Actions: {len(guidance['specific_actions'])}")


if __name__ == "__main__":
    main()
