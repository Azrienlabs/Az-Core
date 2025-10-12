# Arc Framework - Complete Architecture Documentation

## Overview

The Arc Framework is a sophisticated multi-agent orchestration system built on LangGraph, featuring:
- **Hierarchical Agent Teams** with specialized roles
- **Reinforcement Learning** (Q-learning) for intelligent tool selection
- **Model Context Protocol (MCP)** integration for external tool servers
- **LLM Response Caching** for performance optimization
- **Flexible Graph Orchestration** with coordinators, planners, and supervisors

---

## 1. High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        USER[User Input]
    end
    
    subgraph "Orchestration Layer"
        ORCH[GraphOrchestrator]
        COORD[Coordinator Node]
        PLAN[Planner Node]
        SUPER[MainSupervisor]
        GEN[Response Generator]
    end
    
    subgraph "Agent Layer"
        subgraph "Teams"
            TEAM1[Team 1<br/>TeamBuilder]
            TEAM2[Team 2<br/>TeamBuilder]
            TEAM3[MCP Team<br/>MCPTeamBuilder]
        end
        
        subgraph "Team Internals"
            AGENT[ReactAgent]
            TSUP[Team Supervisor]
        end
    end
    
    subgraph "Intelligence Layer"
        subgraph "RL System"
            RLMGR[RLManager<br/>Q-Learning]
            REWARD[RewardCalculator]
        end
        
        subgraph "Caching System"
            LLMCACHE[LLM Cache]
            EMBCACHE[Embedding Cache]
        end
    end
    
    subgraph "Tool Layer"
        TOOLS[Standard Tools]
        MCPSERV[MCP Servers]
        MCPTOOLS[MCP Tools]
    end
    
    subgraph "Foundation"
        STATE[State Management]
        BASE[Base Classes]
        EXCEPT[Exception Handling]
    end
    
    USER --> COORD
    COORD --> PLAN
    PLAN --> SUPER
    SUPER --> TEAM1
    SUPER --> TEAM2
    SUPER --> TEAM3
    TEAM1 --> GEN
    TEAM2 --> GEN
    TEAM3 --> GEN
    GEN --> USER
    
    TEAM1 --> TSUP
    TEAM2 --> TSUP
    TEAM3 --> TSUP
    TSUP --> AGENT
    
    AGENT --> RLMGR
    AGENT --> TOOLS
    AGENT --> MCPTOOLS
    
    RLMGR --> REWARD
    RLMGR --> EMBCACHE
    
    AGENT --> LLMCACHE
    
    TEAM3 --> MCPSERV
    MCPSERV --> MCPTOOLS
    
    ORCH --> STATE
    ORCH --> BASE
    ORCH --> EXCEPT
    
    classDef orchestration fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef intelligence fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef tool fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef foundation fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class ORCH,COORD,PLAN,SUPER,GEN orchestration
    class TEAM1,TEAM2,TEAM3,AGENT,TSUP agent
    class RLMGR,REWARD,LLMCACHE,EMBCACHE intelligence
    class TOOLS,MCPSERV,MCPTOOLS tool
    class STATE,BASE,EXCEPT foundation
```

---

## 2. Core Class Hierarchy

```mermaid
classDiagram
    class BaseNode {
        <<abstract>>
        +String name
        +String description
        +execute(state) Command*
        +__call__(state) Command
    }
    
    class BaseAgent {
        <<abstract>>
        +String name
        +BaseChatModel llm
        +List~BaseTool~ tools
        +String prompt
        +invoke(state) Dict*
        +ainvoke(state) Dict*
        +add_tool(tool)
        +remove_tool(tool_name)
    }
    
    class BaseTeam {
        <<abstract>>
        +String name
        +String description
        +List~BaseAgent~ agents
        +Supervisor supervisor
        +build() Callable*
        +add_agent(agent)
        +remove_agent(name)
        +get_agent(name)
    }
    
    class CoordinatorNode {
        +BaseChatModel llm
        +String system_prompt
        +String handoff_keyword
        +execute(state) Command
        +set_prompt(prompt)
        +set_handoff_keyword(keyword)
    }
    
    class PlannerNode {
        +BaseChatModel llm
        +String system_prompt
        +execute(state) Command
        +set_prompt(prompt)
    }
    
    class GeneratorNode {
        +BaseChatModel llm
        +String system_prompt
        +execute(state) Command
    }
    
    class ReactAgent {
        +bool rl_enabled
        +RLManager rl_manager
        +RewardCalculator reward_calculator
        +bool enable_caching
        +invoke(state) Dict
        +ainvoke(state) Dict
        +stream(state)
        +astream(state)
        -_apply_rl_tool_selection(state)
        -_apply_rl_reward(state, result)
    }
    
    class TeamBuilder {
        -BaseChatModel _llm
        -List~BaseTool~ _tools
        -String _prompt
        -bool _rl_enabled
        -RLManager _rl_manager
        -RewardCalculator _reward_calculator
        +with_llm(llm) TeamBuilder
        +with_tools(tools) TeamBuilder
        +with_prompt(prompt) TeamBuilder
        +with_rl(rl_manager, reward_calc) TeamBuilder
        +build() Callable
    }
    
    class MCPTeamBuilder {
        -List~Dict~ _mcp_servers
        -List _mcp_sessions
        -List~BaseTool~ _mcp_tools
        -bool _mcp_enabled
        +with_mcp_server(command, args, env) MCPTeamBuilder
        +get_mcp_tool_names() List~String~
        +get_mcp_server_count() int
        -_connect_to_mcp_servers() void
    }
    
    class Supervisor {
        +BaseChatModel llm
        +List~String~ members
        +String system_prompt
        +add_member(name)
        +remove_member(name)
        +create_node() Callable
        -_make_supervisor_node() Callable
    }
    
    class MainSupervisor {
        +BaseChatModel llm
        +List~String~ members
        +String system_prompt
        +add_member(name)
        +create_node() Callable
    }
    
    class GraphOrchestrator {
        +Type state_class
        +StateGraph graph_builder
        +int max_iterations
        +bool enable_cycle_detection
        -Dict~String,Callable~ _nodes
        -Dict~String,BaseTeam~ _teams
        -Supervisor _supervisor
        +add_node(name, node) GraphOrchestrator
        +add_team(team) GraphOrchestrator
        +set_supervisor(supervisor) GraphOrchestrator
        +add_edge(from, to) GraphOrchestrator
        +compile() CompiledGraph
        +build_hierarchical_graph() CompiledGraph
        -_has_cycle() bool
        +validate_graph()
    }
    
    class AgentFactory {
        +BaseChatModel default_llm
        +List~BaseTool~ default_tools
        +create_react_agent() ReactAgent
        +create_custom_agent() BaseAgent
        +set_default_llm(llm)
        +add_default_tool(tool)
    }
    
    BaseNode <|-- CoordinatorNode
    BaseNode <|-- PlannerNode
    BaseNode <|-- GeneratorNode
    BaseAgent <|-- ReactAgent
    BaseTeam <|-- TeamBuilder
    TeamBuilder <|-- MCPTeamBuilder
    
    GraphOrchestrator --> BaseNode
    GraphOrchestrator --> BaseTeam
    GraphOrchestrator --> Supervisor
    GraphOrchestrator --> MainSupervisor
    
    TeamBuilder --> ReactAgent
    TeamBuilder --> Supervisor
    MCPTeamBuilder --> ReactAgent
    MCPTeamBuilder --> Supervisor
    
    AgentFactory --> ReactAgent
    ReactAgent --> RLManager
    ReactAgent --> RewardCalculator
```

---

## 3. Reinforcement Learning System

```mermaid
graph TB
    subgraph "RL Core"
        RLMGR[RLManager<br/>Q-Learning Engine]
        QTABLE[(Q-Table<br/>State-Action Values)]
        EMBEDSTORE[(State Embeddings<br/>Semantic Matching)]
    end
    
    subgraph "Reward System"
        REWARDCALC{RewardCalculator<br/>Abstract}
        HEURISTIC[HeuristicRewardCalculator<br/>Rule-based]
        LLMREWARD[LLMRewardCalculator<br/>LLM-based Scoring]
        USERFEED[UserFeedbackRewardCalculator<br/>Human Feedback]
        COMPOSITE[CompositeRewardCalculator<br/>Weighted Combination]
    end
    
    subgraph "Agent Integration"
        AGENT[ReactAgent]
        TOOLS[Tool Execution]
        RESULT[Execution Result]
    end
    
    subgraph "Learning Process"
        EXPLORE[Exploration<br/>Random Selection]
        EXPLOIT[Exploitation<br/>Best Q-Values]
        UPDATE[Q-Value Update<br/>α, γ, reward]
    end
    
    AGENT -->|1. Query| RLMGR
    RLMGR --> QTABLE
    RLMGR --> EMBEDSTORE
    RLMGR -->|State Matching| EMBEDSTORE
    
    RLMGR -->|2a. Explore?| EXPLORE
    RLMGR -->|2b. Exploit?| EXPLOIT
    
    EXPLORE -->|Random Tools| AGENT
    EXPLOIT -->|Top Q-Value Tools| AGENT
    
    AGENT --> TOOLS
    TOOLS --> RESULT
    
    RESULT -->|3. Calculate Reward| REWARDCALC
    
    REWARDCALC -.-> HEURISTIC
    REWARDCALC -.-> LLMREWARD
    REWARDCALC -.-> USERFEED
    REWARDCALC -.-> COMPOSITE
    
    HEURISTIC -->|Reward Signal| UPDATE
    LLMREWARD -->|Reward Signal| UPDATE
    USERFEED -->|Reward Signal| UPDATE
    COMPOSITE -->|Reward Signal| UPDATE
    
    UPDATE -->|4. Update Q-Values| QTABLE
    UPDATE -->|Q(s,a) = Q(s,a) + α[r + γmax(Q(s',a')) - Q(s,a)]| QTABLE
    
    QTABLE -->|Persist| DISK[(Disk Storage<br/>*.pkl)]
    
    classDef rl fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef reward fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef agent fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef storage fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class RLMGR,QTABLE,EMBEDSTORE,EXPLORE,EXPLOIT,UPDATE rl
    class REWARDCALC,HEURISTIC,LLMREWARD,USERFEED,COMPOSITE reward
    class AGENT,TOOLS,RESULT agent
    class DISK storage
```

---

## 4. Caching System Architecture

```mermaid
graph TB
    subgraph "LLM Caching Layer"
        CACHEDLLM[CachedLLM Wrapper]
        EXACTCACHE[Exact Match Cache<br/>SHA-256 Hash]
        SEMCACHE[Semantic Cache<br/>Cosine Similarity]
    end
    
    subgraph "Cache Storage"
        LRUCACHE[LRU Cache<br/>Size-Limited]
        GLOBALCACHE[Global LLM Cache<br/>Singleton]
        EMBCACHE[Embedding Cache<br/>Vector Storage]
    end
    
    subgraph "LLM Operations"
        LLM[Base LLM<br/>ChatOpenAI/etc]
        INVOKE[invoke/ainvoke]
        BATCH[Batch Calls]
        STRUCT[Structured Output]
    end
    
    subgraph "Embedding System"
        EMBMODEL[SentenceTransformer<br/>all-MiniLM-L6-v2]
        VECTOR[Vector Embedding<br/>768-dim]
        COSSIM[Cosine Similarity<br/>Threshold: 0.7]
    end
    
    USER[User/Agent Request] --> CACHEDLLM
    
    CACHEDLLM -->|Check Cache| EXACTCACHE
    CACHEDLLM -->|Check Cache| SEMCACHE
    
    EXACTCACHE -->|Cache Hit| RETURN[Return Cached Response]
    SEMCACHE -->|Cache Hit| RETURN
    
    EXACTCACHE -->|Cache Miss| LLM
    SEMCACHE -->|Cache Miss| LLM
    
    LLM --> INVOKE
    INVOKE -->|Store| EXACTCACHE
    INVOKE -->|Store| SEMCACHE
    INVOKE --> RETURN
    
    EXACTCACHE --> LRUCACHE
    SEMCACHE --> LRUCACHE
    
    LRUCACHE --> GLOBALCACHE
    
    SEMCACHE --> EMBMODEL
    EMBMODEL --> VECTOR
    VECTOR --> COSSIM
    COSSIM --> EMBCACHE
    
    RETURN --> USER
    
    classDef cache fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef llm fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef embedding fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef user fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class CACHEDLLM,EXACTCACHE,SEMCACHE,LRUCACHE,GLOBALCACHE cache
    class LLM,INVOKE,BATCH,STRUCT llm
    class EMBMODEL,VECTOR,COSSIM,EMBCACHE embedding
    class USER,RETURN user
```

---

## 5. MCP (Model Context Protocol) Integration

```mermaid
sequenceDiagram
    participant User
    participant MCPTeamBuilder
    participant MCPServer as MCP Server Process
    participant StdioClient as Stdio Client
    participant Session as Client Session
    participant Adapter as MCP→LangChain Adapter
    participant ReactAgent
    participant MCPTools as MCP Tools
    
    User->>MCPTeamBuilder: Create MCP Team
    MCPTeamBuilder->>MCPTeamBuilder: with_mcp_server(cmd, args)
    
    Note over MCPTeamBuilder: Build Phase
    MCPTeamBuilder->>MCPServer: Start server process
    MCPTeamBuilder->>StdioClient: stdio_client(server_params)
    StdioClient->>Session: Create ClientSession
    Session->>MCPServer: Initialize connection
    
    MCPServer-->>Session: Server capabilities
    Session->>Adapter: convert_mcp_to_langchain_tools()
    
    Adapter->>Adapter: Discover MCP tools
    Adapter->>Adapter: Convert to LangChain format
    Adapter-->>MCPTeamBuilder: LangChain tools
    
    MCPTeamBuilder->>ReactAgent: Create agent with MCP tools
    MCPTeamBuilder-->>User: Team callable
    
    Note over User,MCPTools: Execution Phase
    User->>ReactAgent: Invoke with query
    
    opt RL Enabled
        ReactAgent->>ReactAgent: Select tools via RL
    end
    
    ReactAgent->>MCPTools: Execute MCP tool
    MCPTools->>MCPServer: Tool invocation
    MCPServer->>MCPServer: Execute on server
    MCPServer-->>MCPTools: Tool result
    MCPTools-->>ReactAgent: Result
    
    opt RL Enabled
        ReactAgent->>ReactAgent: Calculate reward
        ReactAgent->>ReactAgent: Update Q-table
    end
    
    ReactAgent-->>User: Response with MCP tool results
```

---

## 6. Complete Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Coordinator
    participant Planner
    participant MainSupervisor
    participant Team1
    participant Team2
    participant MCPTeam
    participant TeamSupervisor
    participant ReactAgent
    participant RLManager
    participant Tools
    participant Generator
    
    User->>Coordinator: Send query
    
    Note over Coordinator: Triage Request
    Coordinator->>Coordinator: Analyze query
    
    alt Simple Query
        Coordinator-->>User: Direct response
    else Complex Query
        Coordinator->>Planner: handoff_to_planner
    end
    
    Note over Planner: Create Plan
    Planner->>Planner: Generate task plan
    Planner->>MainSupervisor: Route with plan
    
    Note over MainSupervisor: Team Selection
    MainSupervisor->>MainSupervisor: Analyze plan
    MainSupervisor->>MainSupervisor: Select best team
    
    alt Route to Team1
        MainSupervisor->>Team1: Delegate task
        Team1->>TeamSupervisor: Internal routing
        TeamSupervisor->>ReactAgent: Execute
    else Route to Team2
        MainSupervisor->>Team2: Delegate task
        Team2->>TeamSupervisor: Internal routing
        TeamSupervisor->>ReactAgent: Execute
    else Route to MCP Team
        MainSupervisor->>MCPTeam: Delegate task
        MCPTeam->>TeamSupervisor: Internal routing
        TeamSupervisor->>ReactAgent: Execute with MCP tools
    end
    
    Note over ReactAgent,Tools: Tool Selection & Execution
    
    opt RL Enabled
        ReactAgent->>RLManager: select_tools(query)
        RLManager->>RLManager: Q-learning policy
        RLManager-->>ReactAgent: Selected tools
    end
    
    ReactAgent->>Tools: Execute tools
    Tools-->>ReactAgent: Tool results
    
    opt RL Enabled
        ReactAgent->>RLManager: update(state, action, reward)
        RLManager->>RLManager: Update Q-values
    end
    
    ReactAgent-->>TeamSupervisor: Agent result
    TeamSupervisor-->>MainSupervisor: Team result
    
    MainSupervisor->>MainSupervisor: Check if done
    
    alt More teams needed
        MainSupervisor->>Team2: Route to next team
        Team2-->>MainSupervisor: Result
    else Task complete
        MainSupervisor->>Generator: Generate response
    end
    
    Generator->>Generator: Format final response
    Generator-->>User: Final answer
```

---

## 7. State Management Flow

```mermaid
stateDiagram-v2
    [*] --> Initialized: Create Graph
    
    Initialized --> CoordinatorState: User Input
    
    CoordinatorState --> PlannerState: handoff_to_planner
    CoordinatorState --> [*]: Direct Response
    
    PlannerState --> SupervisorState: Plan Created
    
    SupervisorState --> TeamExecutionState: Route to Team
    
    state TeamExecutionState {
        [*] --> TeamSupervisor
        TeamSupervisor --> AgentExecution
        
        state AgentExecution {
            [*] --> ToolSelection
            ToolSelection --> RLExploration: Explore
            ToolSelection --> RLExploitation: Exploit
            RLExploration --> ToolExecution
            RLExploitation --> ToolExecution
            ToolExecution --> RewardCalculation
            RewardCalculation --> QValueUpdate
            QValueUpdate --> [*]
        }
        
        AgentExecution --> TeamSupervisor: Result
        TeamSupervisor --> [*]: Team Complete
    }
    
    TeamExecutionState --> SupervisorState: Check Next Step
    TeamExecutionState --> GeneratorState: All Teams Done
    
    SupervisorState --> TeamExecutionState: More Teams Needed
    SupervisorState --> GeneratorState: Task Complete
    
    GeneratorState --> [*]: Return Response
    
    note right of AgentExecution
        RL-enabled tool selection
        Q-learning updates
        Reward feedback
    end note
    
    note right of TeamExecutionState
        Each team has internal
        supervisor + agent(s)
    end note
```

---

## 8. Error Handling & Exceptions

```mermaid
graph TB
    subgraph "Exception Hierarchy"
        BASE[RiseFrameworkError<br/>Base Exception]
        
        GRAPH[GraphError]
        CYCLE[GraphCycleError]
        MAXITER[MaxIterationsExceededError]
        
        VALID[ValidationError]
        
        NODE[NodeExecutionError]
        
        SUPER[SupervisorError]
        
        LLM[LLMError]
        
        TOOL[ToolExecutionError]
    end
    
    subgraph "Error Handling Mechanisms"
        RETRY[Retry Decorator<br/>@retry_with_timeout]
        TIMEOUT[Timeout Handling]
        FALLBACK[Fallback Strategies]
        LOGGING[Comprehensive Logging]
    end
    
    subgraph "Recovery Actions"
        DFLT[Default Values]
        ROUTE[Alternative Routing]
        CACHE[Cache Fallback]
        USER[User Notification]
    end
    
    BASE --> GRAPH
    BASE --> VALID
    BASE --> NODE
    BASE --> SUPER
    BASE --> LLM
    BASE --> TOOL
    
    GRAPH --> CYCLE
    GRAPH --> MAXITER
    
    NODE --> RETRY
    SUPER --> RETRY
    LLM --> RETRY
    
    RETRY --> TIMEOUT
    TIMEOUT --> FALLBACK
    
    FALLBACK --> DFLT
    FALLBACK --> ROUTE
    FALLBACK --> CACHE
    FALLBACK --> USER
    
    LOGGING --> BASE
    
    classDef exception fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef mechanism fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef recovery fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class BASE,GRAPH,CYCLE,MAXITER,VALID,NODE,SUPER,LLM,TOOL exception
    class RETRY,TIMEOUT,FALLBACK,LOGGING mechanism
    class DFLT,ROUTE,CACHE,USER recovery
```

---

## 9. Configuration & Settings

```mermaid
graph LR
    subgraph "Configuration Sources"
        YAML[config.yml<br/>YAML File]
        ENV[Environment Variables]
        CODE[Programmatic Config]
        DEFAULT[Default Values]
    end
    
    subgraph "Configuration Manager"
        CFGMGR[ConfigManager]
        SETTINGS[Settings]
        VALIDATION[Validation]
    end
    
    subgraph "Configuration Categories"
        LLM_CFG[LLM Config<br/>Model, Temperature, etc.]
        RL_CFG[RL Config<br/>Learning Rate, Exploration, etc.]
        CACHE_CFG[Cache Config<br/>Size, Type, Threshold]
        MCP_CFG[MCP Config<br/>Servers, Commands, Env]
        GRAPH_CFG[Graph Config<br/>Max Iterations, Cycles]
        LOG_CFG[Logging Config<br/>Level, Format, Output]
    end
    
    subgraph "Runtime Application"
        ORCH[GraphOrchestrator]
        TEAMS[Team Builders]
        RL[RLManager]
        CACHE[Cache Systems]
    end
    
    YAML --> CFGMGR
    ENV --> CFGMGR
    CODE --> CFGMGR
    DEFAULT --> CFGMGR
    
    CFGMGR --> SETTINGS
    CFGMGR --> VALIDATION
    
    SETTINGS --> LLM_CFG
    SETTINGS --> RL_CFG
    SETTINGS --> CACHE_CFG
    SETTINGS --> MCP_CFG
    SETTINGS --> GRAPH_CFG
    SETTINGS --> LOG_CFG
    
    LLM_CFG --> ORCH
    LLM_CFG --> TEAMS
    
    RL_CFG --> RL
    CACHE_CFG --> CACHE
    MCP_CFG --> TEAMS
    GRAPH_CFG --> ORCH
    LOG_CFG --> ORCH
    
    classDef source fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef manager fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef category fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef runtime fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class YAML,ENV,CODE,DEFAULT source
    class CFGMGR,SETTINGS,VALIDATION manager
    class LLM_CFG,RL_CFG,CACHE_CFG,MCP_CFG,GRAPH_CFG,LOG_CFG category
    class ORCH,TEAMS,RL,CACHE runtime
```

---

## 10. Complete Module Structure

```mermaid
graph TB
    subgraph "arc Package"
        subgraph "core/"
            BASE_PY[base.py<br/>BaseNode, BaseAgent, BaseTeam]
            STATE_PY[state.py<br/>State TypedDict]
            ORCH_PY[orchestrator.py<br/>GraphOrchestrator]
            SUPER_PY[supervisor.py<br/>Supervisor, MainSupervisor]
            EXEC_PY[agent_executor.py<br/>create_thinkat_agent]
        end
        
        subgraph "agents/"
            FACTORY_PY[agent_factory.py<br/>AgentFactory, ReactAgent]
            TEAM_PY[team_builder.py<br/>TeamBuilder]
            MCP_PY[mcp_team_builder.py<br/>MCPTeamBuilder]
            REACT_PY[react_agent.py<br/>Re-export]
        end
        
        subgraph "nodes/"
            COORD_PY[coordinator.py<br/>CoordinatorNode]
            PLAN_PY[planner.py<br/>PlannerNode]
            GEN_PY[generator.py<br/>GeneratorNode]
        end
        
        subgraph "rl/"
            RLMGR_PY[rl_manager.py<br/>RLManager]
            REWARD_PY[rewards.py<br/>RewardCalculator variants]
        end
        
        subgraph "utils/"
            CACHE_PY[caching.py<br/>LRUCache, SemanticCache]
            CACHED_LLM_PY[cached_llm.py<br/>CachedLLM]
            RETRY_PY[retry.py<br/>@retry_with_timeout]
            LOG_PY[logging.py<br/>Logging setup]
            HELPER_PY[helpers.py<br/>Utility functions]
            DECOR_PY[decorators.py<br/>Decorators]
        end
        
        subgraph "config/"
            CFG_PY[config.py<br/>ConfigManager]
            SETTINGS_PY[settings.py<br/>Settings]
            VALID_PY[validation.py<br/>Validators]
        end
        
        EXCEPT_PY[exceptions.py<br/>Custom Exceptions]
        INIT_PY[__init__.py<br/>Package Exports]
    end
    
    subgraph "External Dependencies"
        LANGGRAPH[LangGraph<br/>StateGraph, Command]
        LANGCHAIN[LangChain<br/>BaseChatModel, Tools]
        MCP_LIB[langchain-mcp-adapters<br/>MCP Integration]
        SENTENCE[sentence-transformers<br/>Embeddings]
    end
    
    BASE_PY --> ORCH_PY
    BASE_PY --> SUPER_PY
    BASE_PY --> COORD_PY
    BASE_PY --> PLAN_PY
    BASE_PY --> GEN_PY
    BASE_PY --> FACTORY_PY
    BASE_PY --> TEAM_PY
    
    STATE_PY --> ORCH_PY
    STATE_PY --> TEAM_PY
    
    EXEC_PY --> FACTORY_PY
    EXEC_PY --> TEAM_PY
    
    SUPER_PY --> ORCH_PY
    SUPER_PY --> TEAM_PY
    
    FACTORY_PY --> TEAM_PY
    TEAM_PY --> MCP_PY
    
    RLMGR_PY --> FACTORY_PY
    REWARD_PY --> FACTORY_PY
    
    CACHE_PY --> CACHED_LLM_PY
    CACHE_PY --> RLMGR_PY
    CACHED_LLM_PY --> FACTORY_PY
    
    RETRY_PY --> COORD_PY
    RETRY_PY --> PLAN_PY
    RETRY_PY --> SUPER_PY
    
    CFG_PY --> SETTINGS_PY
    VALID_PY --> CFG_PY
    
    EXCEPT_PY --> ORCH_PY
    EXCEPT_PY --> SUPER_PY
    EXCEPT_PY --> COORD_PY
    
    LANGGRAPH --> ORCH_PY
    LANGGRAPH --> SUPER_PY
    LANGGRAPH --> TEAM_PY
    
    LANGCHAIN --> BASE_PY
    LANGCHAIN --> FACTORY_PY
    
    MCP_LIB --> MCP_PY
    SENTENCE --> RLMGR_PY
    SENTENCE --> CACHE_PY
    
    classDef core fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef node fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef intelligence fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef util fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef config fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef external fill:#f5f5f5,stroke:#424242,stroke-width:2px
    
    class BASE_PY,STATE_PY,ORCH_PY,SUPER_PY,EXEC_PY core
    class FACTORY_PY,TEAM_PY,MCP_PY,REACT_PY agent
    class COORD_PY,PLAN_PY,GEN_PY node
    class RLMGR_PY,REWARD_PY intelligence
    class CACHE_PY,CACHED_LLM_PY,RETRY_PY,LOG_PY,HELPER_PY,DECOR_PY util
    class CFG_PY,SETTINGS_PY,VALID_PY config
    class LANGGRAPH,LANGCHAIN,MCP_LIB,SENTENCE external
```

---

## Summary

The Arc Framework provides a comprehensive, production-ready system for building sophisticated multi-agent applications with:

1. **Modular Architecture**: Clean separation of concerns across layers
2. **Intelligent Optimization**: RL-based tool selection with Q-learning
3. **Performance**: Multi-level caching (LLM responses, embeddings)
4. **Extensibility**: MCP integration for external tool servers
5. **Robustness**: Comprehensive error handling and retry mechanisms
6. **Flexibility**: Fluent builder patterns and hierarchical composition

The framework scales from simple single-agent tasks to complex multi-team orchestrations with automatic learning and optimization.
