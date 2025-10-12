"""
RISE Framework Workflows Module

This module provides various workflow patterns for multi-agent orchestration:
- SequentialWorkflow: Linear chain execution
- ConcurrentWorkflow: Parallel execution
- AgentRearrange: Dynamic routing
- GraphWorkflow: DAG orchestration
- MixtureOfAgents: Expert synthesis
- GroupChat: Conversational collaboration
- ForestSwarm: Dynamic tree selection
- HierarchicalSwarm: Director-worker architecture
- HeavySwarm: Five-phase comprehensive analysis
- SwarmRouter: Universal workflow orchestrator
"""

from rise_framework.workflows.sequential_workflow import SequentialWorkflow
from rise_framework.workflows.concurrent_workflow import ConcurrentWorkflow
from rise_framework.workflows.agent_rearrange import AgentRearrange
from rise_framework.workflows.graph_workflow import GraphWorkflow
from rise_framework.workflows.mixture_of_agents import MixtureOfAgents
from rise_framework.workflows.group_chat import GroupChat
from rise_framework.workflows.forest_swarm import ForestSwarm, AgentTree
from rise_framework.workflows.hierarchical_swarm import HierarchicalSwarm
from rise_framework.workflows.heavy_swarm import HeavySwarm
from rise_framework.workflows.swarm_router import SwarmRouter

__all__ = [
    "SequentialWorkflow",
    "ConcurrentWorkflow",
    "AgentRearrange",
    "GraphWorkflow",
    "MixtureOfAgents",
    "GroupChat",
    "ForestSwarm",
    "AgentTree",
    "HierarchicalSwarm",
    "HeavySwarm",
    "SwarmRouter",
]
