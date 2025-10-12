"""
Arc Framework Workflows Module

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

from arc.workflows.sequential_workflow import SequentialWorkflow
from arc.workflows.concurrent_workflow import ConcurrentWorkflow
from arc.workflows.agent_rearrange import AgentRearrange
from arc.workflows.graph_workflow import GraphWorkflow
from arc.workflows.mixture_of_agents import MixtureOfAgents
from arc.workflows.group_chat import GroupChat
from arc.workflows.forest_swarm import ForestSwarm, AgentTree
from arc.workflows.hierarchical_swarm import HierarchicalSwarm
from arc.workflows.heavy_swarm import HeavySwarm
from arc.workflows.swarm_router import SwarmRouter

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
