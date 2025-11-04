-- ============================================
-- Analytical Team - PostgreSQL Setup
-- ============================================
-- Purpose: Store analytical team knowledge in structured format
-- Author: Helena Kowalczyk (Knowledge Manager)
-- Orchestrated by: Aleksander Nowak
-- Date: 2025-11-03
-- 
-- DOCKER EXECUTION:
-- docker exec -it sms-postgres psql -U user -d destiny -f /path/to/analytical_team_setup.sql
-- OR from host:
-- psql -h localhost -p 5432 -U user -d destiny -f sql/analytical_team_setup.sql
-- ============================================

-- 1. ANALYTICAL TEAM DOCUMENTATION
-- ============================================

CREATE TABLE IF NOT EXISTS analytical_team_docs (
    doc_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    file_path TEXT,
    summary TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    indexed_by VARCHAR(100) DEFAULT 'Helena Kowalczyk'
);

-- Insert all documentation
INSERT INTO analytical_team_docs (doc_id, title, category, file_path, summary, tags) VALUES
('announcement', 'Analytical Team Announcement', 'announcement', 
 'ANALYTICAL_TEAM_ANNOUNCEMENT.md', 
 'Official launch announcement of 9-agent analytical intelligence team with complete integration', 
 ARRAY['critical', 'team', 'launch', 'analytical']),

('team-profile', 'Analytical Team Profile', 'overview',
 'agents/analytical/TEAM_PROFILE.md',
 'Complete profile: 9 agents, capabilities, roster, personalities, use cases',
 ARRAY['agents', 'capabilities', 'roster', 'profiles']),

('privacy-architecture', 'Privacy Architecture', 'architecture',
 'agents/analytical/PRIVACY_ARCHITECTURE.md',
 'Privacy-first design: Local LLM (gpt-oss-20b), no external API calls, sensitive data protection',
 ARRAY['privacy', 'security', 'local-llm', 'gdpr']),

('integration-status', 'Integration Status', 'technical',
 'agents/analytical/INTEGRATION_STATUS.md',
 'Database integration status: PostgreSQL, Neo4j, Qdrant, Redis, Elasticsearch - all operational',
 ARRAY['integration', 'databases', 'infrastructure', 'status']),

('cross-team-integration', 'Cross-Team Integration Guide', 'collaboration',
 'agents/analytical/CROSS_TEAM_INTEGRATION.md',
 'Complete guide for Technical ↔️ Analytical team collaboration with examples and patterns',
 ARRAY['collaboration', 'cross-team', 'workflows', 'patterns']),

('jina-embeddings', 'Jina Embeddings v4 Guide', 'technical',
 'agents/analytical/JINA_EMBEDDINGS_GUIDE.md',
 'Jina v4 configuration: 8192 tokens, table-aware, optimized for analytical documents',
 ARRAY['embeddings', 'jina', 'documents', 'semantic-search']),

('model-config', 'LLM Model Configuration', 'configuration',
 'agents/analytical/MODEL_CONFIG.md',
 'gpt-oss-20b configuration: 20B parameters, 44K context window, local processing',
 ARRAY['llm', 'gpt-oss-20b', 'configuration', 'lm-studio']),

('44k-context', '44K Context Window Advantages', 'capabilities',
 'agents/analytical/44K_CONTEXT_ADVANTAGES.md',
 'Benefits of 44K context: entire documents, multi-document analysis, superior insights',
 ARRAY['context-window', 'capabilities', 'advantages', 'analytical-power'])

ON CONFLICT (doc_id) DO UPDATE SET
    title = EXCLUDED.title,
    summary = EXCLUDED.summary,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- 2. ANALYTICAL AGENTS REGISTRY
-- ============================================

CREATE TABLE IF NOT EXISTS analytical_agents (
    agent_name VARCHAR(100) PRIMARY KEY,
    role VARCHAR(150),
    specialization TEXT,
    toolkit VARCHAR(100),
    toolkit_functions INTEGER,
    team VARCHAR(50) DEFAULT 'analytical',
    status VARCHAR(20) DEFAULT 'available',
    personality TEXT,
    when_to_use TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert all 9 agents
INSERT INTO analytical_agents (agent_name, role, specialization, toolkit, toolkit_functions, personality, when_to_use) VALUES

('Viktor Kovalenko', 'Investigation Director / Orchestrator', 
 'Strategic planning, Task delegation, Intelligence synthesis, Decision-making',
 NULL, 0,
 'Ex-intelligence officer (FSB background), strategic thinker, decisive leader, 20+ years experience',
 'Complex investigations, strategic decisions, team coordination, intelligence synthesis'),

('Damian Rousseau', 'Devil''s Advocate / Critical Challenger',
 'Contrarian analysis, Red team thinking, Assumption challenging, Blind spot identification',
 NULL, 0,
 'Former academic philosopher, rigorous thinker, provocative questioner, enjoys intellectual combat',
 'Critical reviews, risk identification, alternative perspectives, challenging assumptions'),

('Elena Volkov', 'OSINT Specialist',
 'Digital intelligence, Social media analysis, Public records, Information verification',
 'OSINTToolkit', 50,
 'Ex-investigative journalist, naturally curious, thorough researcher, excellent at connecting dots',
 'Background investigations, competitive intelligence, digital forensics, social media analysis'),

('Marcus Chen', 'Financial Analyst / Forensic Accountant',
 'Financial intelligence, Forensic accounting, Fraud detection, Investment analysis',
 'FinancialToolkit', 30,
 'Former Big 4 forensic accountant, detail-oriented, skeptical by nature, follows the money',
 'Financial due diligence, fraud investigations, investment analysis, money trail tracking'),

('Sofia Martinez', 'Market Research Specialist',
 'Market intelligence, Competitive analysis, Consumer insights, Industry research',
 'MarketResearchToolkit', 25,
 'Former strategy consultant (McKinsey background), data-driven, strategic, excellent at synthesis',
 'Market research, competitive positioning, opportunity assessment, consumer insights'),

('Adrian Kowalski', 'Legal Analyst',
 'Legal research, Regulatory compliance, Contract analysis, Risk assessment',
 'LegalToolkit', 20,
 'Corporate lawyer (M&A background), precise, risk-aware, detail-focused',
 'Legal research, compliance assessment, contract reviews, jurisdiction analysis'),

('Maya Patel', 'Data Analyst',
 'Statistical analysis, Data visualization, Predictive analytics, Data quality',
 'DataAnalysisToolkit', 35,
 'Data scientist (PhD Statistics), analytical, visualization expert, loves finding patterns',
 'Data analysis, statistical validation, dashboards, predictive modeling'),

('Lucas Rivera', 'Report Synthesizer',
 'Report writing, Executive summaries, Professional documentation, Presentations',
 'ReportToolkit', 25,
 'Former business journalist, clear communicator, excellent synthesizer, storyteller',
 'Final reports, executive summaries, client deliverables, presentations'),

('Alex Morgan', 'Technical Liaison / Data Engineer',
 'Document parsing, Elasticsearch, Qdrant, ETL pipelines, Technical coordination',
 'Elasticsearch+Qdrant', 40,
 'Data engineer, bridge-builder, automation expert, technical translator for analysts',
 'Document processing, data pipelines, search setup, technical coordination with tech team')

ON CONFLICT (agent_name) DO UPDATE SET
    role = EXCLUDED.role,
    specialization = EXCLUDED.specialization,
    toolkit = EXCLUDED.toolkit,
    toolkit_functions = EXCLUDED.toolkit_functions,
    personality = EXCLUDED.personality,
    when_to_use = EXCLUDED.when_to_use;

-- 3. TEAM CAPABILITIES MATRIX
-- ============================================

CREATE TABLE IF NOT EXISTS team_capabilities (
    id SERIAL PRIMARY KEY,
    team VARCHAR(50),
    capability VARCHAR(100),
    level VARCHAR(20),
    agent_name VARCHAR(100),
    description TEXT,
    FOREIGN KEY (agent_name) REFERENCES analytical_agents(agent_name)
);

-- Insert all capabilities
INSERT INTO team_capabilities (team, capability, level, agent_name, description) VALUES
('analytical', 'OSINT Investigation', 'expert', 'Elena Volkov', 'Web search, domain research, social media intelligence, background checks'),
('analytical', 'Social Media Intelligence', 'expert', 'Elena Volkov', 'Twitter, LinkedIn, Facebook analysis, sentiment tracking'),
('analytical', 'Digital Forensics', 'expert', 'Elena Volkov', 'Digital footprint analysis, metadata extraction'),

('analytical', 'Financial Analysis', 'expert', 'Marcus Chen', 'Statement analysis, ratio analysis, valuation'),
('analytical', 'Forensic Accounting', 'expert', 'Marcus Chen', 'Fraud detection, money trail, anomaly detection'),
('analytical', 'Investment Analysis', 'expert', 'Marcus Chen', 'Due diligence, ROI analysis, risk assessment'),

('analytical', 'Market Research', 'expert', 'Sofia Martinez', 'Trends, segmentation, sizing (TAM/SAM/SOM)'),
('analytical', 'Competitive Intelligence', 'expert', 'Sofia Martinez', 'SWOT, competitor analysis, positioning'),
('analytical', 'Consumer Insights', 'expert', 'Sofia Martinez', 'Sentiment analysis, surveys, journey mapping'),

('analytical', 'Legal Research', 'expert', 'Adrian Kowalski', 'Case law, precedents, legal memo writing'),
('analytical', 'Compliance Assessment', 'expert', 'Adrian Kowalski', 'GDPR, CCPA, HIPAA, SOX, industry regulations'),
('analytical', 'Contract Review', 'expert', 'Adrian Kowalski', 'Risk assessment, negotiation strategy, redlining'),

('analytical', 'Statistical Analysis', 'expert', 'Maya Patel', 'Descriptive stats, hypothesis testing, correlation'),
('analytical', 'Data Visualization', 'expert', 'Maya Patel', 'Charts, dashboards, interactive reports'),
('analytical', 'Predictive Analytics', 'expert', 'Maya Patel', 'ML models, forecasting, time series'),

('analytical', 'Report Writing', 'expert', 'Lucas Rivera', 'Investigation reports, market research reports'),
('analytical', 'Executive Summaries', 'expert', 'Lucas Rivera', 'C-level summaries, board presentations'),
('analytical', 'Presentation Creation', 'expert', 'Lucas Rivera', 'PowerPoint, slides, speaker notes'),

('analytical', 'Document Processing', 'expert', 'Alex Morgan', 'PDF, DOCX, XLSX, PPTX parsing and extraction'),
('analytical', 'Elasticsearch Management', 'expert', 'Alex Morgan', 'Indexing, search, aggregations'),
('analytical', 'Qdrant Management', 'expert', 'Alex Morgan', 'Embeddings, semantic search, hybrid search'),

('analytical', 'Investigation Orchestration', 'expert', 'Viktor Kovalenko', 'Planning, coordination, synthesis, decisions'),
('analytical', 'Critical Analysis', 'expert', 'Damian Rousseau', 'Challenging assumptions, alternative perspectives, risk identification');

-- 4. CROSS-TEAM ROUTING
-- ============================================

CREATE TABLE IF NOT EXISTS cross_team_routing (
    id SERIAL PRIMARY KEY,
    request_type VARCHAR(100),
    from_team VARCHAR(50),
    to_team VARCHAR(50),
    recommended_agent VARCHAR(100),
    use_case TEXT,
    FOREIGN KEY (recommended_agent) REFERENCES analytical_agents(agent_name)
);

-- Insert routing rules
INSERT INTO cross_team_routing (request_type, from_team, to_team, recommended_agent, use_case) VALUES
-- Technical → Analytical
('Market Research', 'technical', 'analytical', 'Sofia Martinez', 'Researching market before building feature'),
('Financial Analysis', 'technical', 'analytical', 'Marcus Chen', 'Cost-benefit analysis, ROI calculation'),
('Legal Review', 'technical', 'analytical', 'Adrian Kowalski', 'License compliance, contract review'),
('OSINT Investigation', 'technical', 'analytical', 'Elena Volkov', 'Competitive intelligence, background checks'),
('Data Analysis', 'technical', 'analytical', 'Maya Patel', 'User behavior analysis, metrics dashboards'),
('Report Writing', 'technical', 'analytical', 'Lucas Rivera', 'Executive summaries, professional reports'),
('Document Processing', 'technical', 'analytical', 'Alex Morgan', 'PDF parsing, document indexing'),

-- Analytical → Technical  
('Web Development', 'analytical', 'technical', 'Tomasz Kamiński', 'Building tools, dashboards, automation'),
('Database Design', 'analytical', 'technical', 'Maria Wiśniewska', 'Schema design, queries, optimization'),
('UI/UX Design', 'analytical', 'technical', 'Joanna Mazur', 'Dashboard design, user interfaces'),
('DevOps/Infrastructure', 'analytical', 'technical', 'Piotr Szymański', 'Scaling, deployment, automation'),
('QA Testing', 'analytical', 'technical', 'Anna Lewandowska', 'Tool testing, validation'),
('Documentation', 'analytical', 'technical', 'Helena Kowalczyk', 'Technical writing, knowledge management');

-- 5. INFRASTRUCTURE REGISTRY
-- ============================================

CREATE TABLE IF NOT EXISTS analytical_infrastructure (
    component VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50),
    url TEXT,
    status VARCHAR(20),
    purpose TEXT,
    configuration JSONB,
    managed_by VARCHAR(100)
);

-- Insert infrastructure components
INSERT INTO analytical_infrastructure (component, type, url, status, purpose, configuration, managed_by) VALUES
('Elasticsearch', 'document_search', 'http://localhost:9200', 'operational',
 'Full-text document search, keyword search, aggregations',
 '{"cluster": "hercules-cluster", "ram": "16GB", "index": "analytical-documents"}'::jsonb,
 'Alex Morgan'),

('Qdrant', 'vector_database', 'http://localhost:6333', 'operational',
 'Semantic search, document embeddings, similarity search',
 '{"collection": "analytical-team", "embedding_model": "jinaai/jina-embeddings-v4-text-retrieval", "dimensions": 768}'::jsonb,
 'Alex Morgan'),

('LM Studio', 'local_llm', 'http://localhost:1234/v1', 'operational',
 'Local AI processing for privacy, chat completions and embeddings',
 '{"model": "gpt-oss-20b", "parameters": "20B", "context_window": 44000, "privacy": "100% local"}'::jsonb,
 'System'),

('PostgreSQL', 'relational_database', 'localhost:5432', 'shared',
 'Structured data: tasks, agents, results, history',
 '{"project_id": "destiny-analytical-team"}'::jsonb,
 'Shared'),

('Neo4j', 'graph_database', 'http://localhost:7474', 'shared',
 'Knowledge graph: relationships, collaboration paths, capabilities',
 '{"project_id": "destiny-analytical-team"}'::jsonb,
 'Helena Kowalczyk'),

('Redis', 'cache', 'localhost:6379', 'shared',
 'Hot cache for team status, capabilities, routing',
 '{"project_id": "destiny-analytical-team"}'::jsonb,
 'Shared')

ON CONFLICT (component) DO UPDATE SET
    status = EXCLUDED.status,
    configuration = EXCLUDED.configuration,
    managed_by = EXCLUDED.managed_by;

-- 6. QUERIES FOR TEAM ACCESS
-- ============================================

-- Query: Get all analytical agents
-- SELECT * FROM analytical_agents ORDER BY agent_name;

-- Query: Find agent by capability
-- SELECT aa.agent_name, aa.role 
-- FROM analytical_agents aa
-- JOIN team_capabilities tc ON aa.agent_name = tc.agent_name
-- WHERE tc.capability ILIKE '%financial%';

-- Query: Cross-team routing
-- SELECT * FROM cross_team_routing WHERE from_team = 'technical';

-- Query: Find documentation by tag
-- SELECT title, file_path, summary 
-- FROM analytical_team_docs 
-- WHERE 'privacy' = ANY(tags);

-- ============================================
-- VERIFICATION
-- ============================================

-- Verify agent count
SELECT COUNT(*) as agent_count FROM analytical_agents;
-- Expected: 9

-- Verify documentation count
SELECT COUNT(*) as doc_count FROM analytical_team_docs;
-- Expected: 8

-- Verify capabilities count
SELECT COUNT(*) as capability_count FROM team_capabilities;
-- Expected: 21

-- Verify infrastructure components
SELECT COUNT(*) as infrastructure_count FROM analytical_infrastructure;
-- Expected: 6

-- ============================================
-- SUCCESS MESSAGE
-- ============================================

SELECT 
    'Analytical Team PostgreSQL Setup Complete!' as status,
    (SELECT COUNT(*) FROM analytical_agents) as agents,
    (SELECT COUNT(*) FROM team_capabilities) as capabilities,
    (SELECT COUNT(*) FROM analytical_team_docs) as documents,
    NOW() as completed_at;
