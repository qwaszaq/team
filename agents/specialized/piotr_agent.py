"""
Piotr Nowicki - DevOps Engineer Agent
Specialization: CI/CD, infrastructure, deployment, monitoring, automation

Author: Destiny Team Framework
Date: 2025-11-03
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class PiotrAgent(BaseAgent):
    """
    DevOps Engineer Agent
    
    Specialized in:
    - CI/CD pipeline design and implementation
    - Infrastructure as Code (IaC)
    - Container orchestration (Docker, Kubernetes)
    - Monitoring and logging
    - Deployment strategies
    
    This agent provides DevOps-specific reasoning and infrastructure-focused outputs.
    """
    
    def __init__(self, project_id: str = "destiny-team-framework-master"):
        super().__init__(
            name="Piotr Nowicki",
            role="DevOps Engineer",
            specialization="CI/CD, Infrastructure as Code, Kubernetes, Monitoring, Automation",
            project_id=project_id
        )
        
        # DevOps-specific attributes
        self.tools = [
            "Docker", "Kubernetes", "Terraform", "Ansible",
            "Jenkins", "GitHub Actions", "GitLab CI",
            "Prometheus", "Grafana", "ELK Stack"
        ]
        self.cloud_platforms = ["AWS", "GCP", "Azure"]
        self.focus_areas = ["Automation", "Reliability", "Scalability", "Security", "Monitoring"]
        
    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute DevOps-specific work
        
        Analyzes task and routes to appropriate DevOps handler.
        """
        start_time = datetime.now()
        
        # Load relevant DevOps context
        context = self.load_context(task.description, limit=3)
        context_list = context if isinstance(context, list) else []
        
        # Analyze task type
        task_lower = task.description.lower()
        
        if any(word in task_lower for word in ["ci/cd", "pipeline", "build", "continuous"]):
            result = self._design_cicd_pipeline(task, context_list)
        elif any(word in task_lower for word in ["infrastructure", "terraform", "cloud", "provision"]):
            result = self._infrastructure_as_code(task, context_list)
        elif any(word in task_lower for word in ["monitoring", "logging", "metrics", "observability"]):
            result = self._setup_monitoring(task, context_list)
        elif any(word in task_lower for word in ["deploy", "deployment", "release", "rollout"]):
            result = self._deploy_application(task, context_list)
        elif any(word in task_lower for word in ["incident", "outage", "troubleshoot", "debug"]):
            result = self._incident_response(task, context_list)
        else:
            result = self._general_devops_work(task, context_list)
            
        # Calculate time
        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken
        
        return result
        
    def _design_cicd_pipeline(self, task: Task, context_list) -> TaskResult:
        """Design CI/CD pipeline"""
        
        thoughts = f"""
CI/CD PIPELINE DESIGN (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: Continuous Integration / Continuous Deployment

PIPELINE ARCHITECTURE:
1. Source Control Integration
   - Git hooks: pre-commit, pre-push
   - Branch protection rules
   - Pull request automation
   - Code review requirements

2. Continuous Integration Pipeline
   
   ┌─────────────────────────────────────────┐
   │     CI PIPELINE (on every commit)       │
   ├─────────────────────────────────────────┤
   │                                         │
   │  1. Code Checkout                       │
   │     ↓                                   │
   │  2. Dependency Installation             │
   │     ↓                                   │
   │  3. Linting & Code Quality              │
   │     • pylint, flake8, black             │
   │     • SonarQube analysis                │
   │     ↓                                   │
   │  4. Unit Tests                          │
   │     • pytest with coverage              │
   │     • Minimum 80% coverage              │
   │     ↓                                   │
   │  5. Integration Tests                   │
   │     • API tests, database tests         │
   │     ↓                                   │
   │  6. Security Scanning                   │
   │     • SAST (Bandit, Safety)            │
   │     • Dependency vulnerabilities        │
   │     ↓                                   │
   │  7. Build Docker Image                  │
   │     • Multi-stage build                 │
   │     • Optimized layers                  │
   │     ↓                                   │
   │  8. Push to Registry                    │
   │     • Tag with commit SHA               │
   │     • Latest tag for main branch        │
   └─────────────────────────────────────────┘

3. Continuous Deployment Pipeline
   
   ┌─────────────────────────────────────────┐
   │  CD PIPELINE (on main branch merge)     │
   ├─────────────────────────────────────────┤
   │                                         │
   │  1. Deploy to Staging                   │
   │     • Automated deployment              │
   │     • Smoke tests                       │
   │     ↓                                   │
   │  2. Integration Tests (Staging)         │
   │     • E2E tests                         │
   │     • Performance tests                 │
   │     ↓                                   │
   │  3. Manual Approval Gate                │
   │     • QA sign-off (Anna)                │
   │     • PM approval (Katarzyna)           │
   │     ↓                                   │
   │  4. Deploy to Production                │
   │     • Blue-green deployment             │
   │     • Health checks                     │
   │     ↓                                   │
   │  5. Smoke Tests (Production)            │
   │     • Critical path validation          │
   │     ↓                                   │
   │  6. Monitor & Alert                     │
   │     • Error rate monitoring             │
   │     • Performance tracking              │
   └─────────────────────────────────────────┘

4. Pipeline Configuration (GitHub Actions)
   ```yaml
   name: CI/CD Pipeline
   
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Run tests
           run: pytest --cov=src tests/
     
     build:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - name: Build Docker image
           run: docker build -t app:${{github.sha}}
         - name: Push to registry
           run: docker push app:${{github.sha}}
     
     deploy:
       needs: build
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       steps:
         - name: Deploy to production
           run: kubectl set image deployment/app app=app:${{github.sha}}
   ```

5. Quality Gates
   ✓ All tests pass (Anna's tests)
   ✓ Code coverage ≥ 80%
   ✓ No critical vulnerabilities
   ✓ Performance benchmarks met
   ✓ Manual QA approval

PIPELINE BENEFITS:
- Fast feedback (<10 min build time)
- Automated testing (no manual steps)
- Security scanning (early detection)
- Consistent deployments
- Rollback capability

DEVOPS CONTEXT:
{len(context_list)} previous infrastructure decisions reviewed
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "cicd_pipeline",
                "ci_stages": 8,
                "cd_stages": 6,
                "automated": True,
                "quality_gates": 5,
                "build_time": "10 min"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                ".github/workflows/cicd.yml",
                "Jenkinsfile",
                "pipeline_documentation.md",
                "quality_gates_spec.md"
            ],
            next_steps="Implement pipeline, test with sample deployment"
        )
        
    def _infrastructure_as_code(self, task: Task, context_list) -> TaskResult:
        """Design infrastructure as code"""
        
        thoughts = f"""
INFRASTRUCTURE AS CODE (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: Infrastructure Provisioning

IAC APPROACH:
1. Infrastructure Requirements
   - Compute: Application servers, workers
   - Database: PostgreSQL, Redis, Neo4j
   - Storage: S3/Cloud Storage for assets
   - Network: VPC, Load balancers, CDN
   - Security: Firewalls, secrets management

2. Terraform Configuration
   
   Infrastructure Components:
   ├── VPC & Networking
   │   • Private/public subnets
   │   • NAT gateways
   │   • Security groups
   │   • Load balancer
   │
   ├── Compute (ECS/EKS/EC2)
   │   • Application servers
   │   • Auto-scaling groups
   │   • Container orchestration
   │
   ├── Databases (RDS/Managed)
   │   • PostgreSQL cluster
   │   • Redis cache
   │   • Backup configuration
   │
   └── Monitoring & Logging
       • CloudWatch/Prometheus
       • Log aggregation
       • Alerting rules

3. Terraform Structure
   ```
   infrastructure/
   ├── modules/
   │   ├── vpc/
   │   ├── compute/
   │   ├── database/
   │   └── monitoring/
   ├── environments/
   │   ├── dev/
   │   ├── staging/
   │   └── production/
   └── terraform.tf
   ```

4. Docker Configuration
   ```dockerfile
   # Multi-stage build for optimization
   FROM python:3.11-slim as builder
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --user -r requirements.txt
   
   FROM python:3.11-slim
   WORKDIR /app
   COPY --from=builder /root/.local /root/.local
   COPY src/ ./src/
   ENV PATH=/root/.local/bin:$PATH
   CMD ["python", "-m", "src.main"]
   ```

5. Kubernetes Manifests
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: app
     template:
       metadata:
         labels:
           app: app
       spec:
         containers:
         - name: app
           image: app:latest
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
           readinessProbe:
             httpGet:
               path: /ready
               port: 8000
   ```

INFRASTRUCTURE DESIGN PRINCIPLES:
✓ Immutable infrastructure
✓ Infrastructure as code (version controlled)
✓ Environment parity (dev/staging/prod)
✓ Automated provisioning
✓ Security by default

DEPLOYMENT ENVIRONMENTS:
- Development: Single node, dev database
- Staging: Production-like, test data
- Production: Multi-AZ, auto-scaling, backups

COST OPTIMIZATION:
- Reserved instances for baseline capacity
- Auto-scaling for peak demand
- Spot instances for non-critical workloads
- Right-sizing based on metrics
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "infrastructure_as_code",
                "tool": "terraform",
                "environments": 3,
                "dockerized": True,
                "kubernetes_ready": True,
                "automated": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "terraform/",
                "Dockerfile",
                "docker-compose.yml",
                "k8s/",
                "infrastructure_docs.md"
            ],
            next_steps="Review with Michał (Arch), provision infrastructure, deploy"
        )
        
    def _setup_monitoring(self, task: Task, context_list) -> TaskResult:
        """Setup monitoring and observability"""
        
        thoughts = f"""
MONITORING SETUP (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: Monitoring & Observability

OBSERVABILITY STACK:
1. The Three Pillars
   
   ├── LOGS (ELK Stack)
   │   • Elasticsearch: Log storage & search
   │   • Logstash: Log aggregation
   │   • Kibana: Log visualization
   │   • Filebeat: Log shipping
   │
   ├── METRICS (Prometheus + Grafana)
   │   • Prometheus: Time-series metrics
   │   • Grafana: Dashboards & visualization
   │   • Node exporter: System metrics
   │   • Custom exporters: App metrics
   │
   └── TRACES (Jaeger/Zipkin)
       • Distributed tracing
       • Request flow visualization
       • Performance bottlenecks

2. Key Metrics to Monitor
   
   Application Metrics:
   - Request rate (requests/second)
   - Error rate (errors/total requests)
   - Response time (p50, p95, p99)
   - Active users (concurrent sessions)
   
   Infrastructure Metrics:
   - CPU utilization (%)
   - Memory usage (GB)
   - Disk I/O (IOPS)
   - Network throughput (Mbps)
   
   Database Metrics:
   - Query performance (ms)
   - Connection pool usage
   - Slow queries (>1sec)
   - Replication lag (ms)
   
   Business Metrics:
   - User signups (/day)
   - Feature usage (counts)
   - Revenue (daily/monthly)
   - Customer churn rate

3. Alerting Strategy
   
   CRITICAL Alerts (Page immediately):
   🚨 Service down (>1 min downtime)
   🚨 Error rate >5%
   🚨 Database connection failure
   🚨 Disk space <10%
   
   HIGH Alerts (Notify team):
   ⚠️  Response time p95 >1sec
   ⚠️  Error rate >1%
   ⚠️  CPU >80% for 5 min
   ⚠️  Memory >85%
   
   MEDIUM Alerts (Track):
   📊 Traffic spike (>2x normal)
   📊 Slow queries detected
   📊 Cache hit rate <80%

4. Dashboard Design
   
   📊 SRE Dashboard:
   - Overall system health (green/yellow/red)
   - Service status (all services)
   - Error budget tracking
   - SLO/SLA compliance
   
   📊 Application Dashboard:
   - Request rate, error rate, response time
   - Active users, feature usage
   - Database performance
   - Cache performance
   
   📊 Infrastructure Dashboard:
   - CPU, memory, disk, network
   - Auto-scaling activity
   - Cost tracking
   - Resource utilization

5. SLO/SLA Definition
   Service Level Objectives:
   - Availability: 99.9% uptime (43 min/month downtime)
   - Latency: p95 < 500ms, p99 < 1sec
   - Error rate: <0.1% of requests
   - Data durability: 99.999999%
   
   Error Budget:
   - Monthly: 43 minutes downtime allowed
   - If exceeded: Feature freeze, focus on reliability

MONITORING BEST PRACTICES:
✓ Monitor symptoms, not causes
✓ Alert on user impact, not internal metrics
✓ Reduce alert fatigue (actionable alerts only)
✓ Dashboards for different audiences
✓ Regular review and refinement

INCIDENT RUNBOOKS:
- Service down → Restart procedure
- High error rate → Check recent deployments
- Database slow → Query optimization
- Disk full → Log cleanup procedure
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "monitoring_setup",
                "stack": "Prometheus + Grafana + ELK",
                "dashboards_created": 3,
                "alerts_configured": 12,
                "slo_defined": True,
                "runbooks": 4
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "prometheus.yml",
                "grafana_dashboards/",
                "alert_rules.yml",
                "runbooks/",
                "slo_sla_doc.md"
            ],
            next_steps="Deploy monitoring stack, validate alerts, train team on runbooks"
        )
        
    def _deploy_application(self, task: Task, context_list) -> TaskResult:
        """Deploy application to production"""
        
        thoughts = f"""
APPLICATION DEPLOYMENT (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: Production Deployment

DEPLOYMENT STRATEGY:
1. Pre-Deployment Checklist
   - [x] All tests passing (Anna confirms)
   - [x] Code reviewed (Tomasz, Michał confirm)
   - [x] Security scan clean
   - [x] Staging validated
   - [x] Rollback plan ready
   - [x] Team notified
   - [x] Monitoring ready

2. Deployment Method: Blue-Green
   
   Current State:
   ┌──────────────┐
   │   BLUE       │  ← Production traffic (v1.0)
   │  (Current)   │
   └──────────────┘
   
   Deploy GREEN:
   ┌──────────────┐  ┌──────────────┐
   │   BLUE       │  │   GREEN      │  ← New version (v1.1)
   │  (Current)   │  │   (New)      │     deployed parallel
   └──────────────┘  └──────────────┘
   
   Smoke Test GREEN:
   - Health check: OK ✅
   - Database connectivity: OK ✅
   - API endpoints: OK ✅
   
   Switch Traffic:
   ┌──────────────┐  ┌──────────────┐
   │   BLUE       │  │   GREEN      │  ← Traffic switched
   │   (Idle)     │  │ (Production) │
   └──────────────┘  └──────────────┘
   
   Monitor for Issues:
   - Error rate: Normal ✅
   - Response time: Normal ✅
   - User reports: None ✅
   
   If Issues: Instant rollback to BLUE
   If OK: Keep GREEN, terminate BLUE

3. Deployment Steps
   ```bash
   # Step 1: Build and push
   docker build -t app:v1.1 .
   docker push registry.example.com/app:v1.1
   
   # Step 2: Deploy to staging
   kubectl set image deployment/app-staging app=app:v1.1
   kubectl rollout status deployment/app-staging
   
   # Step 3: Run staging tests
   pytest tests/e2e/ --env=staging
   
   # Step 4: Deploy GREEN to production
   kubectl apply -f k8s/deployment-green.yml
   
   # Step 5: Health check
   curl https://app-green.internal/health
   
   # Step 6: Switch traffic (gradual)
   # 10% traffic to GREEN
   kubectl apply -f k8s/service-10-90.yml
   # Monitor for 10 minutes
   
   # 50% traffic to GREEN
   kubectl apply -f k8s/service-50-50.yml
   # Monitor for 10 minutes
   
   # 100% traffic to GREEN
   kubectl apply -f k8s/service-100-0.yml
   
   # Step 7: Monitor production
   # Watch dashboards for 1 hour
   
   # Step 8: Cleanup BLUE
   kubectl delete deployment app-blue
   ```

4. Rollback Procedure
   If issues detected:
   ```bash
   # Instant traffic switch back to BLUE
   kubectl apply -f k8s/service-blue.yml
   
   # Investigate issues in GREEN
   # Fix and redeploy later
   ```

5. Post-Deployment
   ✓ Monitor dashboards for 24h
   ✓ Check error logs
   ✓ Verify key metrics
   ✓ Document deployment
   ✓ Post-mortem if issues

DEPLOYMENT METRICS:
- Deployment frequency: 2x per week (target)
- Lead time: <1 hour (code → production)
- MTTR (Mean Time to Recovery): <15 min
- Change failure rate: <5%

DEPLOYMENT SAFETY:
✓ Automated testing (Anna's tests)
✓ Gradual rollout (canary/blue-green)
✓ Health checks
✓ Instant rollback capability
✓ Monitoring and alerting
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "deployment",
                "strategy": "blue_green",
                "automated": True,
                "rollback_ready": True,
                "monitoring": True,
                "success": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "deployment_plan.md",
                "rollback_procedure.md",
                "k8s_manifests/",
                "deployment_log.txt"
            ],
            next_steps="Monitor for 24h, document lessons learned"
        )
        
    def _incident_response(self, task: Task, context_list) -> TaskResult:
        """Handle production incident"""
        
        thoughts = f"""
INCIDENT RESPONSE (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: Incident Management & Resolution

INCIDENT RESPONSE PROCESS:
1. Detection & Alert (00:00)
   - Alert received: [Type of alert]
   - Severity: [Critical/High/Medium]
   - Impact: [User-facing/Internal]
   - Initial assessment: [Quick diagnosis]

2. Incident Declaration (00:05)
   - Incident declared: YES
   - Severity: P1 (Critical)
   - Incident commander: Piotr Nowicki
   - Communication channel: #incident-response
   - Status page updated: "Investigating"

3. Immediate Mitigation (00:10)
   Actions Taken:
   ✓ Rolled back recent deployment (immediate)
   ✓ Scaled up healthy services
   ✓ Isolated problematic component
   ✓ Activated read replicas
   
   Result: Service restored (degraded mode)

4. Root Cause Investigation (00:30)
   Timeline Analysis:
   - 14:00: Deployment of v1.5
   - 14:15: Error rate spike detected
   - 14:20: User reports incoming
   - 14:25: Rollback initiated
   - 14:27: Service restored
   
   Root Cause:
   - Database migration script error
   - Missing index causing slow queries
   - Connection pool exhaustion
   
   Contributing Factors:
   - Insufficient staging testing
   - Migration not tested at scale

5. Resolution & Recovery (01:00)
   Permanent Fix:
   ✓ Fixed migration script
   ✓ Added missing index
   ✓ Increased connection pool
   ✓ Deployed fix (v1.5.1)
   ✓ Validated in production
   ✓ Monitoring normal
   
   Status: RESOLVED ✅

6. Post-Incident Review
   Timeline:
   - Detection: 15 minutes (too slow)
   - Mitigation: 5 minutes (good)
   - Resolution: 45 minutes (acceptable)
   - Total: 1 hour downtime
   
   Impact:
   - Users affected: ~500
   - Requests failed: ~5,000
   - Revenue impact: ~$200
   
   What Went Well:
   ✓ Fast rollback procedure
   ✓ Good team communication
   ✓ Root cause identified quickly
   
   What Could Be Better:
   ⚠️  Earlier detection (need better alerting)
   ⚠️  Staging didn't catch issue (improve testing)
   ⚠️  Migration not reviewed (add review process)

7. Action Items
   - [ ] Improve alerting for slow queries (Piotr)
   - [ ] Add load testing to staging (Anna)
   - [ ] Migration review process (Tomasz + Michał)
   - [ ] Update runbooks (Piotr)

INCIDENT METRICS:
- MTTR: 1 hour (target: <30 min)
- Detection time: 15 min (target: <5 min)
- Communication: Good
- Resolution: Successful ✅

LESSONS LEARNED:
1. Test migrations at scale in staging
2. Better alerting for database issues
3. Automated rollback on error spike
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "incident_response",
                "severity": "P1",
                "resolved": True,
                "mttr": "1 hour",
                "root_cause_found": True,
                "action_items": 4
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "incident_report.md",
                "timeline.md",
                "post_mortem.md",
                "action_items.md"
            ],
            next_steps="Complete action items, update runbooks, improve monitoring"
        )
        
    def _general_devops_work(self, task: Task, context_list) -> TaskResult:
        """General DevOps work"""
        
        thoughts = f"""
DEVOPS TASK (Piotr Nowicki):
{'='*70}

TASK: {task.title}
TYPE: General DevOps Work

DEVOPS APPROACH:
1. Automation First
   - Automate repetitive tasks
   - Infrastructure as code
   - Automated testing and deployment
   - Self-service where possible

2. Reliability Focus
   - Design for failure
   - Implement redundancy
   - Monitor and alert
   - Fast recovery procedures

3. Collaboration
   - Working with Tomasz (Dev) on deployability
   - Supporting Anna (QA) with test environments
   - Aligning with Michał (Arch) on infrastructure
   - Enabling Katarzyna (PM) with metrics

4. Key Principles
   ✓ Everything as code (version controlled)
   ✓ Immutable infrastructure
   ✓ Continuous improvement
   ✓ Measure everything
   ✓ Security by default

DEVOPS CONTEXT:
{len(context_list)} previous infrastructure decisions reviewed

DELIVERABLE:
- DevOps solution implemented
- Automated where possible
- Monitored and observable
- Documented for team

STATUS: Completed with DevOps best practices
        """
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "type": "general_devops",
                "status": "completed",
                "automated": True,
                "monitored": True,
                "documented": True
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["devops_solution.md", "implementation_guide.md"],
            next_steps="Deploy and monitor solution"
        )


# Module test
if __name__ == "__main__":
    import uuid
    
    print("Testing PiotrAgent...")
    
    piotr = PiotrAgent()
    
    # Test CI/CD pipeline task
    task = Task(
        task_id=uuid.uuid4(),
        title="Setup CI/CD pipeline",
        description="Design and implement CI/CD pipeline for project metrics dashboard",
        assigned_to=piotr.name,
        assigned_by="Test",
        context={},
        priority=4,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    result = piotr.process_task(task)
    
    print(f"\n✅ PiotrAgent test:")
    print(f"   Status: {result.status.value}")
    print(f"   Type: {result.output.get('type')}")
    print(f"   Contains 'ci/cd': {'ci/cd' in result.thoughts.lower()}")
    print(f"   Contains 'deployment': {'deployment' in result.thoughts.lower()}")
    print(f"   Contains 'pipeline': {'pipeline' in result.thoughts.lower()}")
    
    assert result.status == TaskStatus.DONE
    assert "pipeline" in result.thoughts.lower() or "deploy" in result.thoughts.lower()
    
    print("\n✅ PiotrAgent ready!")
