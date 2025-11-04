"""
Analytical Team Module

Complete analytical intelligence team with:
- 9 specialized agents
- Professional toolkits
- Local LLM integration (privacy-first)
- Database integration
- Task orchestration
"""

# Import analytical agents
from .viktor_agent import ViktorAgent
from .damian_agent import DamianAgent
from .elena_agent import ElenaAgent
from .marcus_agent import MarcusAgent
from .sofia_agent import SofiaAgent
from .adrian_agent import AdrianAgent
from .maya_agent import MayaAgent
from .lucas_agent import LucasAgent
from .alex_agent import AlexAgent

__all__ = [
    'ViktorAgent',
    'DamianAgent',
    'ElenaAgent',
    'MarcusAgent',
    'SofiaAgent',
    'AdrianAgent',
    'MayaAgent',
    'LucasAgent',
    'AlexAgent',
]
