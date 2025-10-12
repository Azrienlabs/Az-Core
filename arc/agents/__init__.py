"""
Agent components for the Arc Framework.

This module provides factories and builders for creating agents and teams,
along with advanced agent patterns for sophisticated reasoning and evaluation,
and agent routing/handoff capabilities.
"""

from arc.agents.team_builder import TeamBuilder
from arc.agents.mcp_team_builder import MCPTeamBuilder
from arc.agents.agent_factory import AgentFactory
from arc.agents.react_agent import ReactAgent

# Advanced Agent Patterns
from arc.agents.self_consistency_agent import SelfConsistencyAgent
from arc.agents.reflexion_agent import ReflexionAgent
from arc.agents.reasoning_duo_agent import ReasoningDuoAgent
from arc.agents.agent_judge import AgentJudge
from arc.agents.agent_pattern_router import (
    AgentPatternRouter,
    create_agent,
    AgentPattern,
)

# Agent Routing & Handoffs
from arc.agents.agent_router import AgentRouter, HandoffAgent

# Agent Registry (NEW)
from arc.agents.agent_registry import (
    AgentRegistry,
    AgentMetadata,
    get_global_registry,
    register_agent_globally,
    find_agent
)

__all__ = [
    # Core Agent Components
    "TeamBuilder",
    "MCPTeamBuilder",
    "AgentFactory",
    "ReactAgent",

    # Advanced Agent Patterns
    "SelfConsistencyAgent",
    "ReflexionAgent",
    "ReasoningDuoAgent",
    "AgentJudge",

    # Agent Pattern Router
    "AgentPatternRouter",
    "create_agent",
    "AgentPattern",

    # Agent Routing & Handoffs
    "AgentRouter",
    "HandoffAgent",
    
    # Agent Registry (NEW)
    "AgentRegistry",
    "AgentMetadata",
    "get_global_registry",
    "register_agent_globally",
    "find_agent",
]
