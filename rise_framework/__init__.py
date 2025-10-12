"""
Rise Framework - A Professional Hierarchical Multi-Agent Framework

A comprehensive framework for building hierarchical multi-agent systems with LangGraph,
featuring coordinator-planner-supervisor architecture, team management, and flexible
agent orchestration with improved error handling and validation.

Version: 4.1.0
Author: Rise Framework Team
License: MIT
"""

__version__ = "4.1.0"
__author__ = "Rise Framework Team"

from rise_framework.core.base import BaseAgent, BaseTeam, BaseNode
from rise_framework.core.state import State, StateManager
from rise_framework.core.supervisor import Supervisor
from rise_framework.agents.team_builder import TeamBuilder
from rise_framework.agents.agent_factory import AgentFactory
from rise_framework.nodes.coordinator import CoordinatorNode
from rise_framework.nodes.planner import PlannerNode
from rise_framework.nodes.generator import ResponseGeneratorNode
from rise_framework.config.config import Config, load_config
from rise_framework.core.orchestrator import GraphOrchestrator
from rise_framework.utils.logging import setup_logging, get_logger

# New imports for improved framework
from rise_framework import exceptions
from rise_framework.config import validation
from rise_framework.utils import retry

__all__ = [
    # Core classes
    "BaseAgent",
    "BaseTeam",
    "BaseNode",
    "State",
    "StateManager",
    "Supervisor",
    
    # Agent classes
    "TeamBuilder",
    "AgentFactory",
    
    # Node classes
    "CoordinatorNode",
    "PlannerNode",
    "ResponseGeneratorNode",
    
    # Configuration
    "Config",
    "load_config",
    
    # Orchestration
    "GraphOrchestrator",
    
    # Utilities
    "setup_logging",
    "get_logger",
    
    # New modules
    "exceptions",
    "validation",
    "retry",
    
    # Version
    "__version__",
    "__author__",
]
