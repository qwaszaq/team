// ============================================
// Analytical Team - Neo4j Knowledge Graph
// ============================================
// Purpose: Create relationships and knowledge graph
// Author: Helena Kowalczyk
// Date: 2025-11-03
// ============================================

// Clean up existing analytical team nodes (if re-running)
MATCH (n) WHERE n.team = 'analytical' DETACH DELETE n;

// Create Analytical Team node
CREATE (analytical:Team {
    team_id: 'destiny-analytical-team',
    name: 'Destiny Analytical Team',
    type: 'analytical',
    size: 9,
    status: 'operational',
    created: datetime('2025-11-03T00:00:00Z'),
    llm_model: 'gpt-oss-20b',
    context_window: 44000,
    privacy_mode: 'LOCAL'
});

// Create all 9 analytical agents
CREATE (viktor:Agent:Orchestrator {
    name: 'Viktor Kovalenko',
    role: 'Investigation Director',
    team: 'analytical',
    specialization: 'Strategic planning, Intelligence synthesis',
    personality: 'Ex-intelligence officer, strategic, decisive'
});

CREATE (damian:Agent:Challenger {
    name: 'Damian Rousseau',
    role: 'Devil\'s Advocate',
    team: 'analytical',
    specialization: 'Contrarian analysis, Red team thinking',
    personality: 'Former academic, rigorous, provocative'
});

CREATE (elena:Agent:OSINT {
    name: 'Elena Volkov',
    role: 'OSINT Specialist',
    team: 'analytical',
    specialization: 'Digital intelligence, OSINT',
    toolkit: 'OSINTToolkit',
    tool_functions: 50
});

CREATE (marcus:Agent:Financial {
    name: 'Marcus Chen',
    role: 'Financial Analyst',
    team: 'analytical',
    specialization: 'Financial intelligence, Forensic accounting',
    toolkit: 'FinancialToolkit',
    tool_functions: 30
});

CREATE (sofia:Agent:Market {
    name: 'Sofia Martinez',
    role: 'Market Research Specialist',
    team: 'analytical',
    specialization: 'Market intelligence, Competitive analysis',
    toolkit: 'MarketResearchToolkit',
    tool_functions: 25
});

CREATE (adrian:Agent:Legal {
    name: 'Adrian Kowalski',
    role: 'Legal Analyst',
    team: 'analytical',
    specialization: 'Legal research, Compliance',
    toolkit: 'LegalToolkit',
    tool_functions: 20
});

CREATE (maya:Agent:Data {
    name: 'Maya Patel',
    role: 'Data Analyst',
    team: 'analytical',
    specialization: 'Statistical analysis, Data visualization',
    toolkit: 'DataAnalysisToolkit',
    tool_functions: 35
});

CREATE (lucas:Agent:Writer {
    name: 'Lucas Rivera',
    role: 'Report Synthesizer',
    team: 'analytical',
    specialization: 'Report writing, Executive summaries',
    toolkit: 'ReportToolkit',
    tool_functions: 25
});

CREATE (alex:Agent:Technical {
    name: 'Alex Morgan',
    role: 'Technical Liaison',
    team: 'analytical',
    specialization: 'Document parsing, Elasticsearch, Qdrant',
    toolkit: 'Elasticsearch+Qdrant',
    tool_functions: 40
});

// Create team relationships
MATCH (analytical:Team {team_id: 'destiny-analytical-team'})
MATCH (viktor:Agent {name: 'Viktor Kovalenko'})
MATCH (damian:Agent {name: 'Damian Rousseau'})
MATCH (elena:Agent {name: 'Elena Volkov'})
MATCH (marcus:Agent {name: 'Marcus Chen'})
MATCH (sofia:Agent {name: 'Sofia Martinez'})
MATCH (adrian:Agent {name: 'Adrian Kowalski'})
MATCH (maya:Agent {name: 'Maya Patel'})
MATCH (lucas:Agent {name: 'Lucas Rivera'})
MATCH (alex:Agent {name: 'Alex Morgan'})

CREATE (analytical)-[:HAS_MEMBER]->(viktor)
CREATE (analytical)-[:HAS_MEMBER]->(damian)
CREATE (analytical)-[:HAS_MEMBER]->(elena)
CREATE (analytical)-[:HAS_MEMBER]->(marcus)
CREATE (analytical)-[:HAS_MEMBER]->(sofia)
CREATE (analytical)-[:HAS_MEMBER]->(adrian)
CREATE (analytical)-[:HAS_MEMBER]->(maya)
CREATE (analytical)-[:HAS_MEMBER]->(lucas)
CREATE (analytical)-[:HAS_MEMBER]->(alex);

// Orchestration relationships
MATCH (viktor:Agent {name: 'Viktor Kovalenko'})
MATCH (elena:Agent {name: 'Elena Volkov'})
MATCH (marcus:Agent {name: 'Marcus Chen'})
MATCH (sofia:Agent {name: 'Sofia Martinez'})
MATCH (adrian:Agent {name: 'Adrian Kowalski'})
MATCH (maya:Agent {name: 'Maya Patel'})
MATCH (lucas:Agent {name: 'Lucas Rivera'})
MATCH (alex:Agent {name: 'Alex Morgan'})
MATCH (damian:Agent {name: 'Damian Rousseau'})

CREATE (viktor)-[:ORCHESTRATES]->(elena)
CREATE (viktor)-[:ORCHESTRATES]->(marcus)
CREATE (viktor)-[:ORCHESTRATES]->(sofia)
CREATE (viktor)-[:ORCHESTRATES]->(adrian)
CREATE (viktor)-[:ORCHESTRATES]->(maya)
CREATE (viktor)-[:ORCHESTRATES]->(lucas)
CREATE (viktor)-[:ORCHESTRATES]->(alex)
CREATE (viktor)-[:COORDINATES_WITH]->(damian);

// Collaboration patterns
MATCH (elena:Agent {name: 'Elena Volkov'})
MATCH (marcus:Agent {name: 'Marcus Chen'})
MATCH (sofia:Agent {name: 'Sofia Martinez'})
MATCH (adrian:Agent {name: 'Adrian Kowalski'})
MATCH (maya:Agent {name: 'Maya Patel'})
MATCH (lucas:Agent {name: 'Lucas Rivera'})
MATCH (damian:Agent {name: 'Damian Rousseau'})

CREATE (elena)-[:COLLABORATES_WITH]->(marcus)
CREATE (sofia)-[:COLLABORATES_WITH]->(maya)
CREATE (adrian)-[:COLLABORATES_WITH]->(marcus)
CREATE (lucas)-[:SYNTHESIZES_FROM]->(elena)
CREATE (lucas)-[:SYNTHESIZES_FROM]->(marcus)
CREATE (lucas)-[:SYNTHESIZES_FROM]->(sofia)
CREATE (lucas)-[:SYNTHESIZES_FROM]->(adrian)
CREATE (lucas)-[:SYNTHESIZES_FROM]->(maya)
CREATE (damian)-[:CHALLENGES]->(elena)
CREATE (damian)-[:CHALLENGES]->(marcus)
CREATE (damian)-[:CHALLENGES]->(sofia)
CREATE (damian)-[:CHALLENGES]->(adrian);

// Create capability nodes
CREATE (osint:Capability {name: 'OSINT Investigation', level: 'expert', category: 'intelligence'});
CREATE (financial:Capability {name: 'Financial Analysis', level: 'expert', category: 'analysis'});
CREATE (market:Capability {name: 'Market Research', level: 'expert', category: 'research'});
CREATE (legal:Capability {name: 'Legal Research', level: 'expert', category: 'legal'});
CREATE (data:Capability {name: 'Data Analysis', level: 'expert', category: 'data'});
CREATE (reporting:Capability {name: 'Professional Reporting', level: 'expert', category: 'communication'});

// Connect agents to capabilities
MATCH (elena:Agent {name: 'Elena Volkov'})
MATCH (osint:Capability {name: 'OSINT Investigation'})
CREATE (elena)-[:PROVIDES]->(osint);

MATCH (marcus:Agent {name: 'Marcus Chen'})
MATCH (financial:Capability {name: 'Financial Analysis'})
CREATE (marcus)-[:PROVIDES]->(financial);

MATCH (sofia:Agent {name: 'Sofia Martinez'})
MATCH (market:Capability {name: 'Market Research'})
CREATE (sofia)-[:PROVIDES]->(market);

MATCH (adrian:Agent {name: 'Adrian Kowalski'})
MATCH (legal:Capability {name: 'Legal Research'})
CREATE (adrian)-[:PROVIDES]->(legal);

MATCH (maya:Agent {name: 'Maya Patel'})
MATCH (data:Capability {name: 'Data Analysis'})
CREATE (maya)-[:PROVIDES]->(data);

MATCH (lucas:Agent {name: 'Lucas Rivera'})
MATCH (reporting:Capability {name: 'Professional Reporting'})
CREATE (lucas)-[:PROVIDES]->(reporting);

// Return summary
MATCH (a:Agent {team: 'analytical'}) RETURN count(a) as analytical_agents;
