"""
Tests for destiny-memory command
Author: Anna Lewandowska (QA Engineer)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typer.testing import CliRunner
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from destiny_cli.commands.memory import app

runner = CliRunner()


class TestMemoryStats:
    """Test suite for 'destiny memory stats' command"""
    
    def test_stats_help(self):
        """Test stats command help"""
        result = runner.invoke(app, ["stats", "--help"])
        assert result.exit_code == 0
        assert "Show memory system statistics" in result.stdout
        assert "--project" in result.stdout
        assert "--verbose" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    @patch('psycopg2.connect')
    @patch('requests.get')
    def test_stats_basic(self, mock_requests, mock_pg, mock_helena):
        """Test basic stats command execution"""
        # Mock HelenaCore
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_core.postgres_conn = "test_conn"
        mock_core.qdrant_url = "http://localhost:6333"
        mock_helena.return_value = mock_core
        
        # Mock PostgreSQL
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (100,)
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pg.return_value = mock_conn
        
        # Mock Qdrant
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'points_count': 50,
                'vectors_count': 50
            }
        }
        mock_requests.return_value = mock_response
        
        result = runner.invoke(app, ["stats"])
        
        assert result.exit_code == 0
        assert "DESTINY MEMORY SYSTEM" in result.stdout
        assert "PostgreSQL" in result.stdout
        assert "Neo4j" in result.stdout
        assert "Qdrant" in result.stdout
        assert "Redis" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_stats_verbose(self, mock_helena):
        """Test stats with verbose flag"""
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_helena.return_value = mock_core
        
        result = runner.invoke(app, ["stats", "--verbose"])
        
        # Should show database architecture explanation
        assert result.exit_code == 0


class TestMemorySearch:
    """Test suite for 'destiny memory search' command"""
    
    def test_search_help(self):
        """Test search command help"""
        result = runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0
        assert "Search memories using semantic similarity" in result.stdout
        assert "--agent" in result.stdout
        assert "--limit" in result.stdout
        assert "--threshold" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_search_basic(self, mock_helena):
        """Test basic search execution"""
        mock_core = Mock()
        mock_core.load_context.return_value = {
            "memories": [
                {
                    "score": 0.92,
                    "made_by": "Tomasz",
                    "content": "Implemented authentication feature",
                    "event_type": "task",
                    "timestamp": "2025-11-02"
                },
                {
                    "score": 0.85,
                    "made_by": "Anna",
                    "content": "Tested authentication flow",
                    "event_type": "task",
                    "timestamp": "2025-11-02"
                }
            ]
        }
        mock_helena.return_value = mock_core
        
        result = runner.invoke(app, ["search", "authentication"])
        
        assert result.exit_code == 0
        assert "MEMORY SEARCH" in result.stdout
        assert "Found" in result.stdout
        assert "authentication" in result.stdout.lower()
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_search_with_agent_filter(self, mock_helena):
        """Test search with agent filter"""
        mock_core = Mock()
        mock_core.load_context.return_value = {
            "memories": [
                {
                    "score": 0.92,
                    "made_by": "Tomasz Kamiński",
                    "content": "Implemented feature",
                    "event_type": "task",
                    "timestamp": "2025-11-02"
                }
            ]
        }
        mock_helena.return_value = mock_core
        
        result = runner.invoke(app, ["search", "feature", "--agent", "tomasz"])
        
        assert result.exit_code == 0
        assert "Tomasz" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_search_no_results(self, mock_helena):
        """Test search with no results"""
        mock_core = Mock()
        mock_core.load_context.return_value = {"memories": []}
        mock_helena.return_value = mock_core
        
        result = runner.invoke(app, ["search", "nonexistent"])
        
        assert result.exit_code == 0
        assert "No memories found" in result.stdout


class TestMemoryAgent:
    """Test suite for 'destiny memory agent' command"""
    
    def test_agent_help(self):
        """Test agent command help"""
        result = runner.invoke(app, ["agent", "--help"])
        assert result.exit_code == 0
        assert "Show memories for a specific agent" in result.stdout
        assert "--last-days" in result.stdout
        assert "--limit" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    @patch('psycopg2.connect')
    def test_agent_basic(self, mock_pg, mock_helena):
        """Test basic agent command execution"""
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_core.postgres_conn = "test_conn"
        mock_helena.return_value = mock_core
        
        # Mock PostgreSQL results
        from datetime import datetime
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("task", "Implemented feature X", 0.9, datetime.now(), {}),
            ("decision", "Chose architecture Y", 0.85, datetime.now(), {})
        ]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pg.return_value = mock_conn
        
        result = runner.invoke(app, ["agent", "tomasz"])
        
        assert result.exit_code == 0
        assert "AGENT MEMORIES" in result.stdout
        assert "tomasz" in result.stdout.lower()
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    @patch('psycopg2.connect')
    def test_agent_custom_period(self, mock_pg, mock_helena):
        """Test agent with custom time period"""
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_core.postgres_conn = "test_conn"
        mock_helena.return_value = mock_core
        
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pg.return_value = mock_conn
        
        result = runner.invoke(app, ["agent", "anna", "--last-days", "7"])
        
        assert result.exit_code == 0
        assert "Last 7 days" in result.stdout


class TestMemoryRelationships:
    """Test suite for 'destiny memory relationships' command"""
    
    def test_relationships_help(self):
        """Test relationships command help"""
        result = runner.invoke(app, ["relationships", "--help"])
        assert result.exit_code == 0
        assert "collaboration relationships" in result.stdout.lower()
        assert "--agent" in result.stdout
        assert "--depth" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    @patch('subprocess.run')
    def test_relationships_basic(self, mock_subprocess, mock_helena):
        """Test basic relationships command"""
        mock_core = Mock()
        mock_core.neo4j_container = "test-neo4j"
        mock_helena.return_value = mock_core
        
        # Mock Neo4j response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
from | relationship | to | count
"Tomasz" | REVIEWED_BY | "Anna" | 10
"Tomasz" | COORDINATED_BY | "Aleksander" | 5
        """
        mock_subprocess.return_value = mock_result
        
        result = runner.invoke(app, ["relationships"])
        
        assert result.exit_code == 0
        assert "COLLABORATION NETWORK" in result.stdout


class TestMemoryHealth:
    """Test suite for 'destiny memory health' command"""
    
    def test_health_help(self):
        """Test health command help"""
        result = runner.invoke(app, ["health", "--help"])
        assert result.exit_code == 0
        assert "Check health" in result.stdout
        assert "--check-all" in result.stdout
        assert "--fix" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_health_basic(self, mock_helena):
        """Test basic health check"""
        mock_core = Mock()
        mock_core.postgres_conn = "test_conn"
        mock_core.neo4j_container = "test-neo4j"
        mock_core.redis_container = "test-redis"
        mock_core.qdrant_url = "http://localhost:6333"
        mock_helena.return_value = mock_core
        
        result = runner.invoke(app, ["health"])
        
        assert result.exit_code == 0
        assert "HEALTH CHECK" in result.stdout
        assert "PostgreSQL" in result.stdout
        assert "Neo4j" in result.stdout
        assert "Qdrant" in result.stdout
        assert "Redis" in result.stdout


class TestMemoryCleanup:
    """Test suite for 'destiny memory cleanup' command"""
    
    def test_cleanup_help(self):
        """Test cleanup command help"""
        result = runner.invoke(app, ["cleanup", "--help"])
        assert result.exit_code == 0
        assert "Clean up old memories" in result.stdout
        assert "--older-than" in result.stdout
        assert "--dry-run" in result.stdout
        assert "--confirm" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    @patch('psycopg2.connect')
    def test_cleanup_dry_run(self, mock_pg, mock_helena):
        """Test cleanup in dry-run mode"""
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_core.postgres_conn = "test_conn"
        mock_helena.return_value = mock_core
        
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (50,)  # 50 memories to clean
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pg.return_value = mock_conn
        
        result = runner.invoke(app, ["cleanup", "--dry-run", "--older-than", "90"])
        
        assert result.exit_code == 0
        assert "DRY RUN" in result.stdout
        assert "50" in result.stdout


class TestMemoryIntegration:
    """Integration tests for memory command"""
    
    def test_all_commands_accessible(self):
        """Test that all memory subcommands are accessible"""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "stats" in result.stdout
        assert "search" in result.stdout
        assert "agent" in result.stdout
        assert "relationships" in result.stdout
        assert "health" in result.stdout
        assert "cleanup" in result.stdout
    
    @patch('destiny_cli.commands.memory.get_helena_core')
    def test_helena_initialization(self, mock_helena):
        """Test that HelenaCore is properly initialized"""
        mock_core = Mock()
        mock_core.project_id = "test-project"
        mock_helena.return_value = mock_core
        
        from destiny_cli.commands.memory import get_helena_core
        helena = get_helena_core()
        
        assert helena is not None
        mock_helena.assert_called_once()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
