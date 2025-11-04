-- ============================================================================
-- VERIFICATION MIXIN KNOWLEDGE PROPAGATION
-- Date: 2025-11-03
-- Executed by: Helena Kowalczyk (via Aleksander)
-- Purpose: Document verification_mixin tool and automated verification process
-- ============================================================================

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS team_tools (
    id SERIAL PRIMARY KEY,
    tool_name VARCHAR(255) NOT NULL,
    tool_type VARCHAR(100),
    file_path TEXT,
    purpose TEXT,
    created_date DATE,
    created_by VARCHAR(255),
    status VARCHAR(50),
    documentation_path TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_capabilities (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,
    team VARCHAR(50),
    capability TEXT NOT NULL,
    capability_type VARCHAR(100),
    proficiency_level VARCHAR(50),
    must_use_for TEXT,
    added_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS project_processes (
    id SERIAL PRIMARY KEY,
    process_name VARCHAR(255) NOT NULL,
    process_type VARCHAR(100),
    description TEXT,
    owner VARCHAR(255),
    required_for TEXT,
    implementation_date DATE,
    status VARCHAR(50),
    documentation_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tool_methods (
    id SERIAL PRIMARY KEY,
    tool_name VARCHAR(255) NOT NULL,
    method_name VARCHAR(255) NOT NULL,
    method_signature TEXT,
    purpose TEXT,
    returns TEXT,
    example_usage TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add verification_mixin as a team tool
INSERT INTO team_tools (
    tool_name,
    tool_type,
    file_path,
    purpose,
    created_date,
    created_by,
    status,
    documentation_path
) VALUES (
    'VerificationMixin',
    'Python Mixin Class',
    'agents/verification_mixin.py',
    'Enable agents to automatically verify their work completion with objective evidence',
    '2025-11-03',
    'Aleksander Nowak',
    'active',
    'VERIFICATION_INTEGRATION_GUIDE.md'
),
(
    'AutoVerifyMixin',
    'Python Mixin Class',
    'agents/verification_mixin.py',
    'Advanced automatic verification that runs on every task completion',
    '2025-11-03',
    'Aleksander Nowak',
    'active',
    'VERIFICATION_INTEGRATION_GUIDE.md'
)
ON CONFLICT DO NOTHING;

-- Update agent capabilities to include verification
INSERT INTO agent_capabilities (
    agent_name,
    team,
    capability,
    capability_type,
    proficiency_level,
    must_use_for,
    added_date
) VALUES
-- Helena MUST use verification AND is responsible for knowledge propagation
(
    'Helena Kowalczyk',
    'technical',
    'Automatic work verification',
    'process',
    'expert',
    'Database operations, Knowledge propagation, Documentation tasks',
    '2025-11-03'
),
(
    'Helena Kowalczyk',
    'technical',
    'Knowledge propagation to all databases',
    'core_responsibility',
    'expert',
    'ALL changes detected by Aleksander - code, processes, responsibilities, infrastructure',
    '2025-11-03'
),
(
    'Aleksander Nowak',
    'technical',
    'Continuous change monitoring',
    'core_responsibility',
    'expert',
    'Monitor ALL changes daily, document in structured format, assign propagation to Helena',
    '2025-11-03'
),
-- Piotr MUST use verification
(
    'Piotr Szymanski',
    'technical',
    'Deployment verification',
    'process',
    'expert',
    'Deployments, Infrastructure changes',
    '2025-11-03'
),
-- Anna MUST use verification
(
    'Anna Lewandowska',
    'technical',
    'Test result verification',
    'process',
    'expert',
    'Test execution, QA validation, Quality gates',
    '2025-11-03'
),
-- All agents CAN use verification
(
    'ALL_AGENTS',
    'both',
    'Self-verification capability',
    'process',
    'intermediate',
    'Critical tasks, Database operations, System changes',
    '2025-11-03'
)
ON CONFLICT DO NOTHING;

-- Document the automated verification process
INSERT INTO project_processes (
    process_name,
    process_type,
    description,
    owner,
    required_for,
    implementation_date,
    status,
    documentation_url
) VALUES (
    'Automated Task Verification',
    'Quality Assurance',
    'Agents automatically verify their work completion using verification_mixin before reporting tasks as complete. Provides objective evidence and maintains trust.',
    'Aleksander Nowak',
    'All critical tasks: database operations, deployments, system changes, knowledge propagation',
    '2025-11-03',
    'active',
    'VERIFICATION_INTEGRATION_GUIDE.md'
),
(
    'Loop Closure Protocol',
    'Accountability',
    'Every task must be verified with objective checks before being reported as complete. Solves the trust gap where agents claimed completion without evidence.',
    'Aleksander Nowak',
    'All agent task completions',
    '2025-11-03',
    'active',
    'LOOP_CLOSURE_VERIFICATION_SYSTEM.md'
),
(
    'Continuous Monitoring & Knowledge Propagation',
    'Knowledge Management',
    'Aleksander continuously monitors for ALL changes (code, processes, responsibilities, infrastructure). Every change is immediately documented and assigned to Helena for propagation to ALL databases (PostgreSQL, Neo4j, Qdrant, Redis). This ensures zero knowledge drift and maintains project soundness.',
    'Aleksander Nowak',
    'ALL changes in the project - this is the META-PROCESS that maintains all other processes',
    '2025-11-03',
    'active',
    'ALEKSANDER_CONTINUOUS_MONITORING_PROTOCOL.md'
)
ON CONFLICT DO NOTHING;

-- Document verification methods
INSERT INTO tool_methods (
    tool_name,
    method_name,
    method_signature,
    purpose,
    returns,
    example_usage
) VALUES
(
    'VerificationMixin',
    'verify_task_completion',
    'verify_task_completion(task_type: str, checks: List[str], verification_script: str) -> Dict',
    'Run verification for completed task and return detailed results',
    'Dict with success, passed, failed, warnings, evidence, report_path',
    'verification = self.verify_task_completion(task_type="database_population")'
),
(
    'VerificationMixin',
    'verify_database_state',
    'verify_database_state(database: str, checks: Dict) -> Dict',
    'Verify specific database state with custom checks',
    'Dict with success and check results',
    'result = self.verify_database_state("postgresql", {"table_exists": "agents"})'
),
(
    'VerificationMixin',
    'get_verification_summary',
    'get_verification_summary() -> str',
    'Get human-readable summary of last verification',
    'String summary like "Verification: 18/19 passed, 1 FAILED"',
    'summary = self.get_verification_summary()'
)
ON CONFLICT DO NOTHING;
