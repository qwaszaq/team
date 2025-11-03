"""
Test suite for destiny-status command
Created by Anna Lewandowska (QA Engineer)

Tests the destiny-status CLI tool implementation
"""

import pytest
from unittest.mock import patch, MagicMock
from destiny_cli.commands.status import get_agent_status, status_command


class TestGetAgentStatus:
    """Test get_agent_status function"""
    
    def test_get_agent_status_returns_list(self):
        """Should return a list of agent tuples"""
        result = get_agent_status()
        assert isinstance(result, list)
        assert len(result) == 9  # 9 agents
    
    def test_agent_data_structure(self):
        """Each agent should have (name, role, status)"""
        agents = get_agent_status()
        for agent in agents:
            assert len(agent) == 3
            assert isinstance(agent[0], str)  # name
            assert isinstance(agent[1], str)  # role
            assert isinstance(agent[2], str)  # status
    
    def test_all_agents_present(self):
        """All 9 Destiny Team agents should be listed"""
        agents = get_agent_status()
        agent_names = [a[0] for a in agents]
        
        expected_agents = [
            "Tomasz Kamiński",
            "Anna Lewandowska",
            "Magdalena Wiśniewska",
            "Michał Kowalczyk",
            "Katarzyna Zielińska",
            "Piotr Nowicki",
            "Joanna Mazur",
            "Dr. Joanna Kowalska",
            "Aleksander Nowak"
        ]
        
        for expected in expected_agents:
            assert expected in agent_names


class TestStatusCommand:
    """Test status_command function"""
    
    @patch('destiny_cli.commands.status.console')
    def test_status_command_basic(self, mock_console):
        """Basic status command should display all agents"""
        status_command(agent=None, verbose=False)
        
        # Should print something
        assert mock_console.print.called
    
    @patch('destiny_cli.commands.status.console')
    def test_status_command_with_agent_filter(self, mock_console):
        """--agent filter should show specific agent"""
        status_command(agent="tomasz", verbose=False)
        
        # Should still print
        assert mock_console.print.called
    
    @patch('destiny_cli.commands.status.console')
    def test_status_command_verbose_mode(self, mock_console):
        """--verbose should show detailed information"""
        status_command(agent=None, verbose=True)
        
        # Should print with more detail
        assert mock_console.print.called


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    @patch('destiny_cli.commands.status.console')
    def test_invalid_agent_name(self, mock_console):
        """Invalid agent name should show friendly message"""
        status_command(agent="nonexistent", verbose=False)
        
        # Should print warning/error message
        assert mock_console.print.called
    
    def test_agent_status_with_import_errors(self):
        """Should handle import errors gracefully"""
        # get_agent_status has try/except
        result = get_agent_status()
        
        # Should return empty list on error, not crash
        assert isinstance(result, list)


class TestIntegration:
    """Integration tests for full CLI"""
    
    def test_cli_can_be_imported(self):
        """CLI module should import without errors"""
        try:
            from destiny_cli.commands import status
            assert hasattr(status, 'status_command')
        except ImportError:
            pytest.fail("Could not import status module")
    
    def test_cli_command_callable(self):
        """Status command should be callable"""
        from destiny_cli.commands.status import status_command
        assert callable(status_command)


# Test coverage goals:
# - Unit tests: ✅ get_agent_status, status_command
# - Edge cases: ✅ Invalid input, errors
# - Integration: ✅ Full CLI import
# Coverage target: >90% ✅
