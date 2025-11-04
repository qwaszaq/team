"""
Capabilities Registry - Dynamic System Capability Tracking

This registry tracks ALL capabilities available in the Destiny Team system.
Agents can query this to discover what tools and methods are available.

As system grows, this registry grows automatically.
"""

from datetime import datetime
from typing import Dict, List, Optional
import json


class CapabilitiesRegistry:
    """
    Central registry of all system capabilities
    
    Purpose:
    - Track all tools, methods, agents, databases available
    - Allow agents to discover capabilities dynamically
    - Version tracking (system evolves over time)
    - Experience tracking (what works, what doesn't)
    """
    
    def __init__(self):
        self.version = "2.0.0"  # Major update: OSINT toolkits added
        self.last_updated = datetime.now().isoformat()
        
        # Initialize capabilities
        self.capabilities = self._initialize_capabilities()
    
    def _initialize_capabilities(self) -> Dict:
        """Initialize complete capability map"""
        
        return {
            "version": self.version,
            "last_updated": self.last_updated,
            
            # ============================================
            # AGENTS
            # ============================================
            "agents": {
                "technical_team": [
                    {
                        "name": "Aleksander Nowak",
                        "role": "Orchestrator",
                        "specialization": "Coordination, routing, decisions",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Magdalena Kowalska",
                        "role": "Product Manager",
                        "specialization": "Requirements, user stories, prioritization",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Katarzyna Wiśniewska",
                        "role": "Architect",
                        "specialization": "System design, tech stack, architecture",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Tomasz Zieliński",
                        "role": "Developer",
                        "specialization": "Implementation, code quality, debugging",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Anna Nowakowska",
                        "role": "QA Engineer",
                        "specialization": "Testing, quality assurance, bug finding",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Piotr Szymański",
                        "role": "DevOps Engineer",
                        "specialization": "Deployment, CI/CD, infrastructure",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Michał Dąbrowski",
                        "role": "Security Specialist",
                        "specialization": "Security audits, vulnerability assessment",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Dr. Joanna Wójcik",
                        "role": "Data Scientist",
                        "specialization": "Data analysis, ML pipelines",
                        "status": "active",
                        "experience_level": "expert"
                    },
                    {
                        "name": "Dr. Helena Kowalczyk",
                        "role": "Knowledge Manager",
                        "specialization": "Documentation, summaries, knowledge organization",
                        "status": "active",
                        "experience_level": "expert"
                    }
                ],
                
                "analytical_team": [
                    {
                        "name": "Viktor Kovalenko",
                        "role": "Investigation Director",
                        "specialization": "Strategic planning, intelligence synthesis",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": None
                    },
                    {
                        "name": "Damian Rousseau",
                        "role": "Devil's Advocate / Critical Thinker",
                        "specialization": "Contrarian analysis, red team thinking, continuous learning",
                        "status": "active",
                        "experience_level": "growing",  # GROWS WITH EXPERIENCE!
                        "toolkit": "critical_thinking",
                        "learning_enabled": True,
                        "experience_points": 0
                    },
                    {
                        "name": "Elena Volkov",
                        "role": "OSINT Specialist",
                        "specialization": "Digital intelligence, social media analysis, geolocation",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "osint_toolkit"
                    },
                    {
                        "name": "Marcus Chen",
                        "role": "Financial Analyst",
                        "specialization": "Financial intelligence, forensic accounting",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "financial_toolkit"
                    },
                    {
                        "name": "Sofia Martinez",
                        "role": "Market Research Specialist",
                        "specialization": "Market intelligence, competitive analysis",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "market_research_toolkit"
                    },
                    {
                        "name": "Adrian Kowalski",
                        "role": "Legal Analyst",
                        "specialization": "Legal research, regulatory compliance",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "legal_toolkit"
                    },
                    {
                        "name": "Maya Patel",
                        "role": "Data Analyst",
                        "specialization": "Statistical analysis, data visualization",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "data_analysis_toolkit"
                    },
                    {
                        "name": "Lucas Rivera",
                        "role": "Report Synthesizer",
                        "specialization": "Report writing, executive summaries",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "report_toolkit"
                    },
                    {
                        "name": "Alex Morgan",
                        "role": "Technical Liaison",
                        "specialization": "Document parsing, Elasticsearch, Qdrant",
                        "status": "active",
                        "experience_level": "expert",
                        "toolkit": "elasticsearch_qdrant"
                    }
                ]
            },
            
            # ============================================
            # TOOLKITS (NEW!)
            # ============================================
            "toolkits": {
                "scraping_toolkit": {
                    "status": "active",
                    "version": "1.0.0",
                    "added": "2025-11-04",
                    "location": "agents/analytical/tools/scraping_toolkit.py",
                    "class": "ScrapingToolkit",
                    "description": "Web scraping, dynamic content, API access",
                    "capabilities": [
                        "fetch_page - Basic HTML fetching",
                        "parse_html - BeautifulSoup parsing",
                        "extract_links - Link extraction",
                        "extract_text - Text extraction",
                        "extract_metadata - Meta tags",
                        "extract_tables - Table parsing",
                        "extract_images - Image extraction",
                        "scrape_dynamic_page - JavaScript rendering (Playwright)",
                        "screenshot - Page screenshots",
                        "api_get / api_post - API client with rate limiting",
                        "archive_page - Content archiving"
                    ],
                    "dependencies": ["requests", "beautifulsoup4", "playwright (optional)"],
                    "primary_users": ["Elena", "Sofia", "Marcus", "Adrian", "Maya"],
                    "use_cases": [
                        "Collect evidence from websites",
                        "Archive content before deletion",
                        "Social media monitoring",
                        "API integration",
                        "Systematic data collection"
                    ]
                },
                
                "mathematical_toolkit": {
                    "status": "active",
                    "version": "1.0.0",
                    "added": "2025-11-04",
                    "location": "agents/analytical/tools/mathematical_toolkit.py",
                    "class": "MathematicalToolkit",
                    "description": "Statistics, calculations, data analysis",
                    "capabilities": [
                        "basic_stats - Mean, median, std, quartiles",
                        "correlation - Correlation coefficient",
                        "moving_average - Time series smoothing",
                        "normalize - Data normalization",
                        "detect_outliers - Z-score outlier detection",
                        "euclidean_distance - Distance calculation",
                        "distance_matrix - All-pairs distances",
                        "cosine_similarity - Vector similarity",
                        "angle_between_vectors - Angle calculation",
                        "bearing_between_points - Geographic bearing",
                        "statistical_test - T-test, Mann-Whitney",
                        "correlation_test - Significance testing",
                        "cluster_data - K-Means clustering",
                        "detect_anomalies_isolation - Isolation Forest"
                    ],
                    "dependencies": ["numpy", "scipy (optional)", "sklearn (optional)"],
                    "primary_users": ["Maya", "Elena", "Marcus", "Sofia", "Viktor", "Damian"],
                    "use_cases": [
                        "Statistical analysis of datasets",
                        "Geolocation calculations",
                        "Outlier and anomaly detection",
                        "Trend analysis",
                        "Pattern recognition",
                        "Hypothesis testing"
                    ]
                },
                
                "osint_toolkit": {
                    "status": "active",
                    "version": "1.0.0",
                    "location": "agents/analytical/tools/osint_toolkit.py",
                    "class": "OSINTToolkit",
                    "description": "Open source intelligence gathering",
                    "capabilities": [
                        "web_search - DuckDuckGo, SearX",
                        "wayback_machine - Archive lookup",
                        "domain_lookup - WHOIS data",
                        "dns_lookup - DNS records",
                        "ip_geolocation - IP location",
                        "social_media_search - Username search across platforms",
                        "email_format_guesser - Email generation",
                        "email_reputation_check - Email validation",
                        "company_search - Company information"
                    ],
                    "primary_users": ["Elena"],
                    "use_cases": ["OSINT investigations", "Digital footprint analysis"]
                },
                
                "image_intelligence_toolkit": {
                    "status": "planned",
                    "version": "0.0.0",
                    "planned_date": "2025-11-15",
                    "description": "Image analysis, geolocation, OCR",
                    "planned_capabilities": [
                        "extract_exif - EXIF metadata extraction",
                        "ocr_extract_text - OCR text extraction",
                        "detect_faces - Face detection",
                        "calculate_image_hash - Perceptual hashing",
                        "compare_images - Image similarity",
                        "analyze_colors - Dominant colors",
                        "reverse_image_search - Find image online"
                    ]
                },
                
                "geolocation_toolkit": {
                    "status": "planned",
                    "version": "0.0.0",
                    "planned_date": "2025-11-15",
                    "description": "Geographic intelligence, shadow analysis",
                    "planned_capabilities": [
                        "geocode - Address to coordinates",
                        "reverse_geocode - Coordinates to address",
                        "calculate_distance - Distance between points",
                        "get_timezone - Timezone from coordinates",
                        "calculate_sun_position - Sun azimuth/altitude (CRITICAL!)",
                        "estimate_time_from_shadow - Chronolocation (Bellingcat!)",
                        "create_map - Interactive map generation"
                    ]
                }
            },
            
            # ============================================
            # DATABASES
            # ============================================
            "databases": {
                "postgresql": {
                    "status": "active",
                    "host": "localhost",
                    "port": 5432,
                    "database": "destiny_team",
                    "purpose": "Structured metadata, relationships",
                    "tables": [
                        "documents", "agents", "tasks", "capabilities",
                        "team_tools", "agent_capabilities", "project_processes"
                    ]
                },
                
                "neo4j": {
                    "status": "active",
                    "host": "localhost",
                    "port": 7687,
                    "purpose": "Knowledge graph, entity relationships",
                    "node_types": [
                        "Agent", "Tool", "Capability", "Document",
                        "Investigation", "Entity", "Event"
                    ]
                },
                
                "qdrant": {
                    "status": "active",
                    "host": "localhost",
                    "port": 6333,
                    "collection": "destiny-team-framework-master",
                    "vector_dim": 1024,
                    "purpose": "Semantic search, document retrieval"
                },
                
                "redis": {
                    "status": "active",
                    "host": "localhost",
                    "port": 6379,
                    "purpose": "Hot cache, quick access",
                    "ttl": "24 hours"
                }
            },
            
            # ============================================
            # METHODOLOGIES
            # ============================================
            "methodologies": {
                "bellingcat_osint": {
                    "status": "documented",
                    "reference": "docs/research/BELLINGCAT_METHODOLOGY_ANALYSIS.md",
                    "techniques": [
                        "Geolocation (GPS-level precision)",
                        "Chronolocation (shadow analysis)",
                        "Multi-source verification (3+ sources)",
                        "Content archiving (immediate)",
                        "Reverse image search",
                        "Social media intelligence",
                        "Confidence scoring"
                    ],
                    "standard": "World-class investigative journalism"
                },
                
                "institutional_api_analysis": {
                    "status": "proven",
                    "reference": "docs/capabilities/INSTITUTIONAL_API_ANALYSIS.md",
                    "proof": "Sejm API - 197 meetings analyzed (2019-2023)",
                    "techniques": [
                        "API integration with rate limiting",
                        "Statistical analysis",
                        "Keyword extraction",
                        "Time series analysis",
                        "Report generation"
                    ]
                },
                
                "statistical_analysis": {
                    "status": "active",
                    "techniques": [
                        "Descriptive statistics",
                        "Hypothesis testing",
                        "Correlation analysis",
                        "Outlier detection",
                        "Clustering",
                        "Anomaly detection"
                    ]
                }
            },
            
            # ============================================
            # PROTOCOLS (MANDATORY)
            # ============================================
            "mandatory_protocols": {
                "source_attribution": {
                    "status": "mandatory",
                    "applies_to": "ALL investigative & research agents",
                    "document": "docs/protocols/SOURCE_ATTRIBUTION_PROTOCOL.md",
                    "quick_ref": "SOURCE_CITATION_QUICK_REFERENCE.md",
                    "rule": "NO SOURCE = NO CLAIM",
                    "requirements": [
                        "Every fact must have a source",
                        "Every source must be fully cited",
                        "Every online source must be archived",
                        "Key claims need 3+ independent sources",
                        "Source credibility must be assessed"
                    ],
                    "since": "2025-11-04",
                    "enforcement": "Work rejected if sources missing",
                    "review": "Damian verifies all sources before publication"
                }
            },
            
            # ============================================
            # SYSTEM CAPABILITIES
            # ============================================
            "system_capabilities": [
                {
                    "capability": "Institutional API Analysis",
                    "status": "proven",
                    "evidence": "Sejm API (197 meetings, 20+ page report)",
                    "since": "2025-11-04"
                },
                {
                    "capability": "Bellingcat-Level OSINT",
                    "status": "designed",
                    "implementation": "in_progress",
                    "target": "text + image (video later)"
                },
                {
                    "capability": "Automatic Knowledge Propagation",
                    "status": "active",
                    "agent": "Helena Kowalczyk",
                    "databases": ["PostgreSQL", "Neo4j", "Qdrant", "Redis"]
                },
                {
                    "capability": "Multi-Agent Collaboration",
                    "status": "active",
                    "teams": ["Technical (9 agents)", "Analytical (9 agents)"]
                },
                {
                    "capability": "Adaptive Learning",
                    "status": "active",
                    "description": "System learns from experience, grows smarter"
                }
            ],
            
            # ============================================
            # EXPERIENCE TRACKING (NEW!)
            # ============================================
            "experience": {
                "investigations_completed": 1,  # Sejm API analysis
                "tools_used": {
                    "api_client": 1,
                    "data_analysis": 1,
                    "statistical_analysis": 1
                },
                "techniques_mastered": [
                    "API integration",
                    "Statistical analysis",
                    "Report generation",
                    "Data export"
                ],
                "lessons_learned": [
                    "Rate limiting prevents API overload",
                    "HTML parsing requires care",
                    "Statistical analysis reveals insights",
                    "Cross-team collaboration works"
                ],
                "next_challenges": [
                    "Geolocation from images",
                    "Shadow analysis (chronolocation)",
                    "Multi-source verification",
                    "Large-scale scraping"
                ]
            }
        }
    
    # ============================================
    # QUERY METHODS
    # ============================================
    
    def get_all_agents(self) -> List[Dict]:
        """Get all agents (technical + analytical)"""
        return (self.capabilities["agents"]["technical_team"] + 
                self.capabilities["agents"]["analytical_team"])
    
    def get_agent(self, name: str) -> Optional[Dict]:
        """Get specific agent by name"""
        for agent in self.get_all_agents():
            if agent["name"].lower() == name.lower():
                return agent
        return None
    
    def get_all_toolkits(self) -> Dict:
        """Get all available toolkits"""
        return self.capabilities["toolkits"]
    
    def get_active_toolkits(self) -> Dict:
        """Get only active toolkits"""
        return {
            name: toolkit 
            for name, toolkit in self.capabilities["toolkits"].items()
            if toolkit.get("status") == "active"
        }
    
    def get_toolkit(self, name: str) -> Optional[Dict]:
        """Get specific toolkit"""
        return self.capabilities["toolkits"].get(name)
    
    def get_agent_toolkits(self, agent_name: str) -> List[str]:
        """Get toolkits available to specific agent"""
        toolkits = []
        for toolkit_name, toolkit in self.get_active_toolkits().items():
            if agent_name in toolkit.get("primary_users", []):
                toolkits.append(toolkit_name)
        return toolkits
    
    def get_capabilities_summary(self) -> Dict:
        """Get high-level capability summary"""
        return {
            "version": self.version,
            "last_updated": self.last_updated,
            "total_agents": len(self.get_all_agents()),
            "technical_team": len(self.capabilities["agents"]["technical_team"]),
            "analytical_team": len(self.capabilities["agents"]["analytical_team"]),
            "active_toolkits": len(self.get_active_toolkits()),
            "planned_toolkits": len([t for t in self.capabilities["toolkits"].values() 
                                    if t.get("status") == "planned"]),
            "databases": len(self.capabilities["databases"]),
            "methodologies": len(self.capabilities["methodologies"]),
            "investigations_completed": self.capabilities["experience"]["investigations_completed"]
        }
    
    def search_capabilities(self, query: str) -> List[Dict]:
        """Search for capabilities matching query"""
        results = []
        query_lower = query.lower()
        
        # Search in toolkits
        for toolkit_name, toolkit in self.capabilities["toolkits"].items():
            if query_lower in toolkit_name.lower() or \
               query_lower in toolkit.get("description", "").lower():
                results.append({
                    "type": "toolkit",
                    "name": toolkit_name,
                    "data": toolkit
                })
        
        # Search in methodologies
        for method_name, method in self.capabilities["methodologies"].items():
            if query_lower in method_name.lower():
                results.append({
                    "type": "methodology",
                    "name": method_name,
                    "data": method
                })
        
        return results
    
    # ============================================
    # UPDATE METHODS
    # ============================================
    
    def add_experience(self, category: str, item: str):
        """Add experience point"""
        if category in self.capabilities["experience"]["tools_used"]:
            self.capabilities["experience"]["tools_used"][category] += 1
        else:
            self.capabilities["experience"]["tools_used"][category] = 1
        
        self.last_updated = datetime.now().isoformat()
    
    def add_lesson_learned(self, lesson: str):
        """Add lesson to knowledge base"""
        if lesson not in self.capabilities["experience"]["lessons_learned"]:
            self.capabilities["experience"]["lessons_learned"].append(lesson)
            self.last_updated = datetime.now().isoformat()
    
    def complete_investigation(self):
        """Mark investigation as completed"""
        self.capabilities["experience"]["investigations_completed"] += 1
        self.last_updated = datetime.now().isoformat()
    
    def update_agent_experience(self, agent_name: str, experience_points: int):
        """Update agent experience level"""
        agent = self.get_agent(agent_name)
        if agent and "experience_points" in agent:
            agent["experience_points"] += experience_points
            
            # Update experience level based on points
            if agent["experience_points"] < 100:
                agent["experience_level"] = "novice"
            elif agent["experience_points"] < 500:
                agent["experience_level"] = "intermediate"
            elif agent["experience_points"] < 1000:
                agent["experience_level"] = "advanced"
            else:
                agent["experience_level"] = "expert"
            
            self.last_updated = datetime.now().isoformat()
    
    # ============================================
    # EXPORT METHODS
    # ============================================
    
    def to_json(self, indent: int = 2) -> str:
        """Export to JSON"""
        return json.dumps(self.capabilities, indent=indent)
    
    def save_to_file(self, filepath: str):
        """Save registry to file"""
        with open(filepath, 'w') as f:
            json.dump(self.capabilities, f, indent=2)
    
    def print_summary(self):
        """Print readable summary"""
        summary = self.get_capabilities_summary()
        
        print("=" * 60)
        print("DESTINY TEAM - CAPABILITIES REGISTRY")
        print("=" * 60)
        print(f"Version: {summary['version']}")
        print(f"Last Updated: {summary['last_updated']}")
        print()
        print("TEAM:")
        print(f"  - Technical Team: {summary['technical_team']} agents")
        print(f"  - Analytical Team: {summary['analytical_team']} agents")
        print(f"  - Total: {summary['total_agents']} agents")
        print()
        print("TOOLKITS:")
        print(f"  - Active: {summary['active_toolkits']}")
        print(f"  - Planned: {summary['planned_toolkits']}")
        print()
        print("INFRASTRUCTURE:")
        print(f"  - Databases: {summary['databases']}")
        print(f"  - Methodologies: {summary['methodologies']}")
        print()
        print("EXPERIENCE:")
        print(f"  - Investigations Completed: {summary['investigations_completed']}")
        print("=" * 60)


# Create global registry instance
registry = CapabilitiesRegistry()


# Test/Example usage
if __name__ == "__main__":
    print("🎯 Capabilities Registry Test\n")
    
    # Print summary
    registry.print_summary()
    
    print("\n--- Active Toolkits ---")
    for name, toolkit in registry.get_active_toolkits().items():
        print(f"\n{name}:")
        print(f"  Description: {toolkit['description']}")
        print(f"  Primary Users: {', '.join(toolkit['primary_users'])}")
    
    print("\n--- Elena's Toolkits ---")
    elena_toolkits = registry.get_agent_toolkits("Elena")
    print(f"Elena has access to: {', '.join(elena_toolkits)}")
    
    print("\n--- Search: 'geolocation' ---")
    results = registry.search_capabilities("geolocation")
    for result in results:
        print(f"  {result['type']}: {result['name']}")
    
    print("\n✅ Capabilities Registry works!")
