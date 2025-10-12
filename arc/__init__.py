"""
Arc Framework - A Professional Hierarchical Multi-Agent Framework

A comprehensive framework for building hierarchical multi-agent systems with LangGraph,
featuring coordinator-planner-supervisor architecture, team management, and flexible
agent orchestration with improved error handling and validation.

Version: 4.1.0
Author: Arc Framework Team
License: MIT
"""

__version__ = "4.1.0"
__author__ = "Arc Framework Team"

from arc.core.base import BaseAgent, BaseTeam, BaseNode
from arc.core.state import State, StateManager
from arc.core.supervisor import Supervisor
from arc.agents.team_builder import TeamBuilder
from arc.agents.agent_factory import AgentFactory
from arc.nodes.coordinator import CoordinatorNode
from arc.nodes.planner import PlannerNode
from arc.nodes.generator import ResponseGeneratorNode
from arc.config.config import Config, load_config
from arc.core.orchestrator import GraphOrchestrator
from arc.utils.logging import setup_logging, get_logger

# New imports for improved framework
from arc import exceptions
from arc.config import validation
from arc.utils import retry

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
