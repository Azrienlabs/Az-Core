# Rise Framework v2.0 - Architecture Documentation

## System Architecture

### High-Level Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                         Rise Framework v2.0                         │
│                   Hierarchical Multi-Agent System                   │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                    (External Applications)                          │
└────────────────┬───────────────────────────────────────────────────┘
                 │
                 │ Input Messages
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                      COORDINATOR LAYER                              │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              CoordinatorNode                                  │ │
│  │  • Initial user interaction                                   │ │
│  │  • Simple query handling                                      │ │
│  │  • Routing decision: [END | Planner]                         │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────────────────────┘
                 │
                 │ Complex Tasks
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                       PLANNING LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                PlannerNode                                    │ │
│  │  • Task decomposition                                         │ │
│  │  • Team assignment                                            │ │
│  │  • Execution plan generation (JSON)                          │ │
│  │  • Routing: [END | Supervisor]                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────────────────────┘
                 │
                 │ Execution Plan
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                     SUPERVISION LAYER                               │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                  Supervisor                                   │ │
│  │  • Team routing                                               │ │
│  │  • Workflow coordination                                      │ │
│  │  • Dynamic member management                                  │ │
│  │  • Routing: [Team1 | Team2 | ... | TeamN | Generator]       │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────┬────────┬────────┬────────┬────────┬───────────────────────┘
         │        │        │        │        │
    ┌────▼───┐┌───▼───┐┌──▼───┐┌───▼───┐┌───▼───┐
    │ Team 1 ││Team 2 ││Team 3││Team 4 ││Team N │
    │        ││       ││      ││       ││       │
    └────┬───┘└───┬───┘└──┬───┘└───┬───┘└───┬───┘
         │        │        │        │        │
         └────────┴────────┴────────┴────────┘
                         │
                         │ Team Outputs
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                    GENERATION LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │            ResponseGeneratorNode                              │ │
│  │  • Output synthesis                                           │ │
│  │  • Response formatting                                        │ │
│  │  • Quality assurance                                          │ │
│  │  • Routing: [END]                                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────────────────────────┘
                 │
                 │ Final Response
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                         (Response Output)                           │
└────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Core Module Structure

```
rise_framework/
│
├── core/                          # Core Framework Components
│   ├── base.py                   # Abstract Base Classes
│   │   ├── BaseAgent             # Agent interface
│   │   ├── BaseTeam              # Team interface
│   │   └── BaseNode              # Node interface
│   │
│   ├── state.py                  # State Management
│   │   ├── State                 # Enhanced state class
│   │   └── StateManager          # State manipulation utilities
│   │
│   ├── supervisor.py             # Supervisor Implementation
│   │   └── Supervisor            # LLM-based routing supervisor
│   │
│   └── orchestrator.py           # Graph Orchestration
│       └── GraphOrchestrator     # High-level graph builder
│
├── agents/                        # Agent Framework
│   ├── team_builder.py           # Team Building
│   │   └── TeamBuilder           # Fluent team builder
│   │
│   ├── agent_factory.py          # Agent Creation
│   │   ├── AgentFactory          # Factory pattern
│   │   └── ReactAgent            # ReAct agent
│   │
│   └── react_agent.py            # Convenience export
│
├── nodes/                         # Pre-Built Nodes
│   ├── coordinator.py            # User Interaction
│   │   └── CoordinatorNode       # Coordinator implementation
│   │
│   ├── planner.py                # Task Planning
│   │   └── PlannerNode           # Planner implementation
│   │
│   └── generator.py              # Response Generation
│       └── ResponseGeneratorNode # Generator implementation
│
├── teams/                         # Example Teams
│   ├── security_team.py          # Security monitoring
│   │   └── SecurityTeam          # Camera management
│   │
│   └── water_management_team.py  # Water systems
│       └── WaterManagementTeam   # MCP integration
│
├── config/                        # Configuration Management
│   ├── config.py                 # Config Loading
│   │   ├── Config                # Main config class
│   │   └── load_config()         # Convenience loader
│   │
│   └── settings.py               # Settings Classes
│       ├── LLMConfig             # LLM configuration
│       └── Settings              # Complete settings
│
└── utils/                         # Utilities
    ├── logging.py                # Logging Setup
    │   ├── setup_logging()       # Log configuration
    │   └── get_logger()          # Logger factory
    │
    ├── prompts.py                # Prompt Management
    │   ├── PromptLoader          # Prompt file loader
    │   └── load_prompt()         # Convenience loader
    │
    ├── decorators.py             # Helper Decorators
    │   ├── async_to_sync()       # Async conversion
    │   ├── sync_to_async()       # Sync conversion
    │   ├── log_execution()       # Execution logging
    │   └── retry()               # Retry logic
    │
    └── helpers.py                # Helper Functions
        ├── validate_state()      # State validation
        ├── clean_json()          # JSON cleaning
        └── parse_json_safe()     # Safe JSON parsing
```

## Data Flow Architecture

### Message Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Initial Message                                          │
│    {"role": "user", "content": "User query"}               │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. State Formation                                          │
│    {                                                        │
│      "messages": [...],                                     │
│      "next": "",                                            │
│      "full_plan": "",                                       │
│      "context": {},                                         │
│      "metadata": {}                                         │
│    }                                                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Coordinator Processing                                   │
│    • Analyzes message                                       │
│    • Simple query → Direct response                         │
│    • Complex query → Handoff to planner                     │
│    Updates: {"messages": [...coordinator_response]}        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Planner Processing (if needed)                          │
│    • Decomposes task                                        │
│    • Creates execution plan (JSON)                          │
│    • Identifies required teams                              │
│    Updates: {                                               │
│      "messages": [...plan],                                 │
│      "full_plan": "JSON plan"                               │
│    }                                                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Supervisor Routing                                       │
│    • Reads plan                                             │
│    • Routes to appropriate team                             │
│    • Manages workflow                                       │
│    Updates: {"next": "team_name"}                           │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Team Execution                                           │
│    • Receives relevant messages                             │
│    • Uses tools to complete task                            │
│    • Returns results                                        │
│    Updates: {"messages": [...team_response]}                │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼ (Repeat 5-6 for multiple teams)
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Response Generation                                      │
│    • Synthesizes all team outputs                           │
│    • Formats final response                                 │
│    • Ensures completeness                                   │
│    Updates: {"messages": [...final_response]}               │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Final State                                              │
│    {                                                        │
│      "messages": [                                          │
│        user_message,                                        │
│        coordinator_response,                                │
│        planner_plan,                                        │
│        team1_response,                                      │
│        team2_response,                                      │
│        final_response                                       │
│      ],                                                     │
│      "next": "__end__",                                     │
│      "full_plan": "...",                                    │
│      "context": {...},                                      │
│      "metadata": {...}                                      │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

## Team Architecture

### Team Internal Structure

```
┌─────────────────────────────────────────────────────────────┐
│                         Team                                 │
│                    (e.g., SecurityTeam)                     │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Team Supervisor                        │   │
│  │  • Routes within team                              │   │
│  │  • Manages agent execution                         │   │
│  └──────────┬─────────────────────────────────────────┘   │
│             │                                              │
│             ▼                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Team Agent                             │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │         ReAct Agent                        │   │   │
│  │  │  • Reasoning loop                          │   │   │
│  │  │  • Tool selection                          │   │   │
│  │  │  • Action execution                        │   │   │
│  │  └────────────────────────────────────────────┘   │   │
│  │                                                     │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │            Tool Suite                      │   │   │
│  │  │  • tool_1()                                │   │   │
│  │  │  • tool_2()                                │   │   │
│  │  │  • tool_n()                                │   │   │
│  │  └────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Configuration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Configuration Sources                      │
└─────┬───────────────────────────────────────────────────┬───┘
      │                                                   │
┌─────▼──────┐                                    ┌──────▼─────┐
│ config.yml │                                    │    .env    │
│            │                                    │            │
│ llm:       │                                    │ OPENAI_... │
│   model:   │                                    │ LLM_MODEL  │
│   temp:    │                                    │ LLM_TEMP   │
└─────┬──────┘                                    └──────┬─────┘
      │                                                   │
      └───────────────────────┬───────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Config Object   │
                    │                  │
                    │  • get_llm()     │
                    │  • get_embed()   │
                    │  • get()         │
                    │  • set()         │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
    │   LLM   │         │Fast LLM │        │Embeddings│
    │         │         │         │        │         │
    └─────────┘         └─────────┘        └─────────┘
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Production Environment                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐                                         │
│  │ Load Balancer  │                                         │
│  └───────┬────────┘                                         │
│          │                                                  │
│    ┌─────┴─────┬─────────┬─────────┐                      │
│    │           │         │         │                      │
│  ┌─▼──┐      ┌─▼──┐    ┌─▼──┐   ┌─▼──┐                  │
│  │App │      │App │    │App │   │App │  (Multiple        │
│  │Inst│      │Inst│    │Inst│   │Inst│   instances)      │
│  │ 1  │      │ 2  │    │ 3  │   │ N  │                   │
│  └─┬──┘      └─┬──┘    └─┬──┘   └─┬──┘                  │
│    │           │         │         │                      │
│    └───────────┴─────────┴─────────┘                      │
│                    │                                       │
│                    │                                       │
│  ┌─────────────────▼──────────────────┐                  │
│  │     Shared Services                │                  │
│  │                                     │                  │
│  │  ┌────────────┐  ┌──────────────┐ │                  │
│  │  │LLM Provider│  │Vector Store  │ │                  │
│  │  │ (OpenAI)   │  │ (if needed)  │ │                  │
│  │  └────────────┘  └──────────────┘ │                  │
│  │                                     │                  │
│  │  ┌────────────┐  ┌──────────────┐ │                  │
│  │  │Config Store│  │  Monitoring  │ │                  │
│  │  │            │  │   & Logging  │ │                  │
│  │  └────────────┘  └──────────────┘ │                  │
│  └─────────────────────────────────────┘                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Summary

Rise Framework v2.0 provides:

- **Hierarchical Architecture**: Clear separation of concerns
- **Modular Design**: Pluggable components
- **Scalable Structure**: Easy to extend and maintain
- **Type-Safe**: Comprehensive type hints
- **Well-Documented**: Extensive documentation
- **Production-Ready**: Error handling, logging, monitoring

This architecture supports:
- ✅ Complex multi-agent workflows
- ✅ Dynamic team composition
- ✅ Flexible routing strategies
- ✅ State management
- ✅ Configuration flexibility
- ✅ Easy deployment

---

**Rise Framework v2.0** - Professional Hierarchical Multi-Agent System
