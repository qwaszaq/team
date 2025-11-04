"""
Agent Verification Mixin
Purpose: Enable agents to automatically verify their work
Author: Aleksander Nowak
Usage: Mix into any agent class to add self-verification capability
"""

import subprocess
import json
import os
from typing import Dict, Optional, List


class VerificationMixin:
    """
    Mixin class that adds verification capabilities to agents.
    
    Usage:
        class MyAgent(BaseAgent, VerificationMixin):
            def execute_task(self, task):
                result = self._do_work(task)
                
                # Verify the work before reporting complete
                verification = self.verify_task_completion(
                    task_type="database_population",
                    checks=["postgresql", "redis", "neo4j"]
                )
                
                if verification["success"]:
                    return "Task complete - VERIFIED"
                else:
                    return f"Task incomplete: {verification['failures']}"
    """
    
    def verify_task_completion(
        self, 
        task_type: str = "general",
        checks: Optional[List[str]] = None,
        verification_script: Optional[str] = None
    ) -> Dict:
        """
        Run verification for completed task.
        
        Args:
            task_type: Type of task (e.g., "database_population", "code_deployment")
            checks: List of specific checks to run (e.g., ["postgresql", "redis"])
            verification_script: Path to custom verification script
            
        Returns:
            Dict with:
                - success: bool
                - passed: int
                - failed: int
                - warnings: int
                - evidence: dict
                - report_path: str
        """
        
        # Default to standard verification script
        if verification_script is None:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            verification_script = os.path.join(base_path, "scripts", "verify_task_completion.py")
        
        # Check if verification script exists
        if not os.path.exists(verification_script):
            return {
                "success": False,
                "error": f"Verification script not found: {verification_script}",
                "passed": 0,
                "failed": 1,
                "warnings": 0
            }
        
        # Run verification script
        try:
            result = subprocess.run(
                ["python3", verification_script],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes max
            )
            
            # Parse verification report
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            report_path = os.path.join(base_path, "VERIFICATION_REPORT.json")
            
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    report = json.load(f)
                
                # Count results
                passed = sum(1 for c in report["checks"] if c["status"] == "PASS")
                failed = sum(1 for c in report["checks"] if c["status"] == "FAIL")
                warned = sum(1 for c in report["checks"] if c["status"] == "WARN")
                
                # Collect failure details
                failures = [
                    {
                        "check": c["name"],
                        "evidence": c["evidence"]
                    }
                    for c in report["checks"] if c["status"] == "FAIL"
                ]
                
                return {
                    "success": failed == 0,
                    "passed": passed,
                    "failed": failed,
                    "warnings": warned,
                    "failures": failures,
                    "evidence": report["checks"],
                    "report_path": report_path,
                    "overall_status": report["overall_status"]
                }
            else:
                # Script ran but no report generated
                return {
                    "success": result.returncode == 0,
                    "passed": 0,
                    "failed": 0 if result.returncode == 0 else 1,
                    "warnings": 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Verification timeout (>2 minutes)",
                "passed": 0,
                "failed": 1,
                "warnings": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Verification failed: {str(e)}",
                "passed": 0,
                "failed": 1,
                "warnings": 0
            }
    
    def verify_database_state(self, database: str, checks: Dict) -> Dict:
        """
        Verify specific database state.
        
        Args:
            database: "postgresql", "redis", "neo4j", "qdrant"
            checks: Dict of checks to perform
                Example: {
                    "table_exists": "analytical_agents",
                    "row_count": {"table": "analytical_agents", "expected": 9}
                }
        
        Returns:
            Dict with verification results
        """
        results = []
        
        if database == "postgresql":
            for check_name, check_params in checks.items():
                if check_name == "table_exists":
                    cmd = f"docker exec sms-postgres psql -U user -d destiny -c '\\dt {check_params}' 2>/dev/null"
                elif check_name == "row_count":
                    table = check_params["table"]
                    cmd = f"docker exec sms-postgres psql -U user -d destiny -t -c 'SELECT COUNT(*) FROM {table};' 2>/dev/null"
                else:
                    continue
                
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                    results.append({
                        "check": check_name,
                        "success": result.returncode == 0 and len(result.stdout.strip()) > 0,
                        "output": result.stdout.strip()
                    })
                except:
                    results.append({
                        "check": check_name,
                        "success": False,
                        "output": "Check failed"
                    })
        
        all_passed = all(r["success"] for r in results)
        return {
            "success": all_passed,
            "checks": results
        }
    
    def get_verification_summary(self) -> str:
        """
        Get human-readable verification summary.
        
        Returns:
            String summary of last verification
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        report_path = os.path.join(base_path, "VERIFICATION_REPORT.json")
        
        if not os.path.exists(report_path):
            return "❌ No verification report found"
        
        try:
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            passed = sum(1 for c in report["checks"] if c["status"] == "PASS")
            failed = sum(1 for c in report["checks"] if c["status"] == "FAIL")
            warned = sum(1 for c in report["checks"] if c["status"] == "WARN")
            total = len(report["checks"])
            
            summary = f"Verification: {passed}/{total} passed"
            if failed > 0:
                summary += f", {failed} FAILED ❌"
            if warned > 0:
                summary += f", {warned} warnings ⚠️"
            
            return summary
        except:
            return "❌ Could not read verification report"


class AutoVerifyMixin(VerificationMixin):
    """
    Advanced mixin that automatically verifies on task completion.
    
    Usage:
        class MyAgent(BaseAgent, AutoVerifyMixin):
            AUTO_VERIFY = True  # Enable automatic verification
            
            def execute_task(self, task):
                result = self._do_work(task)
                # Verification happens automatically after this method
                return result
    """
    
    AUTO_VERIFY = False  # Override to True in agent class
    VERIFICATION_REQUIRED_FOR = []  # List of task types that require verification
    
    def complete_task(self, task, result):
        """
        Override complete_task to add automatic verification.
        
        This method is called when a task is marked as complete.
        If AUTO_VERIFY is True, it runs verification before confirming completion.
        """
        
        # Check if verification is required
        should_verify = (
            self.AUTO_VERIFY or 
            (hasattr(task, 'task_type') and task.task_type in self.VERIFICATION_REQUIRED_FOR)
        )
        
        if should_verify:
            print(f"\n🔍 Running automatic verification for task: {task.title if hasattr(task, 'title') else 'unknown'}")
            
            verification = self.verify_task_completion()
            
            if verification["success"]:
                print(f"✅ Verification passed: {verification['passed']}/{verification['passed'] + verification['failed']} checks")
                result["verification"] = "PASSED"
                result["verification_evidence"] = self.get_verification_summary()
            else:
                print(f"❌ Verification failed: {verification['failed']} checks failed")
                result["verification"] = "FAILED"
                result["verification_failures"] = verification.get("failures", [])
                
                # Optionally prevent task completion if verification fails
                if hasattr(self, 'BLOCK_ON_VERIFICATION_FAILURE') and self.BLOCK_ON_VERIFICATION_FAILURE:
                    result["status"] = "INCOMPLETE"
                    result["error"] = "Task verification failed"
        
        return result
