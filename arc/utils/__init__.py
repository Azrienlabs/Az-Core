"""
Utilities and helper functions for the Arc Framework.

This module provides logging setup, prompt loading, decorators,
caching, conversation management, agent persistence, and other utility functions.
"""

from arc.utils.logging import setup_logging, get_logger
from arc.utils.prompts import PromptLoader, load_prompt
from arc.utils.decorators import async_to_sync, sync_to_async
from arc.utils.helpers import validate_state, clean_json
from arc.utils.caching import (
    LRUCache,
    TTLCache,
    SemanticCache,
    PersistentCache,
    cached,
    get_llm_cache,
    get_embedding_cache,
    get_state_cache,
    clear_all_caches,
    get_all_cache_stats
)
from arc.utils.cached_llm import CachedLLM, create_cached_llm, enable_llm_caching
from arc.utils.conversation import Conversation
from arc.utils.base_structure import BaseStructure
from arc.utils.agent_persistence import AgentPersistence
from arc.utils.output_formatter import (
    OutputType,
    history_output_formatter,
    format_conversation_history,
    format_agent_output,
    format_swarm_output,
    format_error_output,
    aggregate_outputs,
    format_to_json,
    format_execution_summary
)

__all__ = [
    # Logging
    "setup_logging",
    "get_logger",
    # Prompts
    "PromptLoader",
    "load_prompt",
    # Decorators
    "async_to_sync",
    "sync_to_async",
    # Helpers
    "validate_state",
    "clean_json",
    # Caching
    "LRUCache",
    "TTLCache",
    "SemanticCache",
    "PersistentCache",
    "cached",
    "get_llm_cache",
    "get_embedding_cache",
    "get_state_cache",
    "clear_all_caches",
    "get_all_cache_stats",
    # Cached LLM
    "CachedLLM",
    "create_cached_llm",
    "enable_llm_caching",
    # Conversation & Persistence
    "Conversation",
    "BaseStructure",
    "AgentPersistence",
    # Output Formatting (NEW)
    "OutputType",
    "history_output_formatter",
    "format_conversation_history",
    "format_agent_output",
    "format_swarm_output",
    "format_error_output",
    "aggregate_outputs",
    "format_to_json",
    "format_execution_summary",
]
