"""
Agent components for the Rise Framework.

This module provides factories and builders for creating agents and teams,
along with advanced agent patterns for sophisticated reasoning and evaluation,
and agent routing/handoff capabilities.
"""

from rise_framework.agents.team_builder import TeamBuilder
from rise_framework.agents.mcp_team_builder import MCPTeamBuilder
from rise_framework.agents.agent_factory import AgentFactory
from rise_framework.agents.react_agent import ReactAgent

# Advanced Agent Patterns
from rise_framework.agents.self_consistency_agent import SelfConsistencyAgent
from rise_framework.agents.reflexion_agent import ReflexionAgent
from rise_framework.agents.reasoning_duo_agent import ReasoningDuoAgent
from rise_framework.agents.agent_judge import AgentJudge
from rise_framework.agents.agent_pattern_router import (
    AgentPatternRouter,
    create_agent,
    AgentPattern,
)

# Agent Routing & Handoffs
from rise_framework.agents.agent_router import AgentRouter, HandoffAgent

# Agent Registry (NEW)
from rise_framework.agents.agent_registry import (
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
