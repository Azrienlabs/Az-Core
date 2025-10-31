"""
Azcore - A Professional Multi-Agent Framework

A comprehensive framework for building hierarchical multi-agent systems with LangGraph,
featuring coordinator-planner-supervisor architecture, team management, and flexible
agent orchestration with improved error handling and validation.

Version: 0.0.6
Author: Arc  Team
License: MIT
"""

# Suppress LangGraph deprecation warnings (internal library warnings)
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='langgraph')

__version__ = "0.0.6"
__author__ = "Arc Team"

from azcore.core.base import BaseAgent, BaseTeam, BaseNode
from azcore.core.state import State, StateManager
from azcore.core.supervisor import Supervisor
from azcore.agents.team_builder import TeamBuilder
from azcore.agents.agent_factory import AgentFactory
from azcore.nodes.coordinator import CoordinatorNode
from azcore.nodes.planner import PlannerNode
from azcore.nodes.generator import ResponseGeneratorNode

# Advanced Planning & Reasoning Features
from azcore.nodes.advanced_planner import (
    AdvancedPlannerNode,
    ExecutionPlan,
    PlanStep,
    StepStatus,
    PlanComplexity,
    create_advanced_planner
)
from azcore.nodes.plan_validator import (
    PlanValidatorNode,
    ValidationReport,
    ValidationIssue,
    ValidationSeverity,
    ValidationType,
    create_plan_validator
)
from azcore.nodes.adaptive_replanner import (
    AdaptiveReplannerNode,
    ReplanTrigger,
    ReplanStrategy,
    ReplanEvent,
    create_adaptive_replanner
)
from azcore.nodes.causal_reasoning import (
    CausalReasoningNode,
    CausalRelation,
    CausalChain,
    CausalGraph,
    CausalRelationType,
    CausalStrength,
    create_causal_reasoner
)
from azcore.nodes.counterfactual_reasoning import (
    CounterfactualReasoningNode,
    CounterfactualScenario,
    CounterfactualAnalysis,
    CounterfactualType,
    OutcomeComparison,
    create_counterfactual_reasoner
)

from azcore.config.config import Config, load_config
from azcore.core.orchestrator import GraphOrchestrator
from azcore.utils.logging import setup_logging, get_logger
from azcore.config import validation
from azcore.utils import retry
from azcore import exceptions

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
    
    # Node classes (Original)
    "CoordinatorNode",
    "PlannerNode",
    "ResponseGeneratorNode",
    
    # Advanced Planning Nodes
    "AdvancedPlannerNode",
    "create_advanced_planner",
    "ExecutionPlan",
    "PlanStep",
    "StepStatus",
    "PlanComplexity",
    
    # Plan Validation
    "PlanValidatorNode",
    "create_plan_validator",
    "ValidationReport",
    "ValidationIssue",
    "ValidationSeverity",
    "ValidationType",
    
    # Adaptive Re-planning
    "AdaptiveReplannerNode",
    "create_adaptive_replanner",
    "ReplanTrigger",
    "ReplanStrategy",
    "ReplanEvent",
    
    # Causal Reasoning
    "CausalReasoningNode",
    "create_causal_reasoner",
    "CausalRelation",
    "CausalChain",
    "CausalGraph",
    "CausalRelationType",
    "CausalStrength",
    
    # Counterfactual Reasoning
    "CounterfactualReasoningNode",
    "create_counterfactual_reasoner",
    "CounterfactualScenario",
    "CounterfactualAnalysis",
    "CounterfactualType",
    "OutcomeComparison",
    
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
