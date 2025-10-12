# Arc Framework v2.0 - Migration Guide

## Overview

This document guides you through migrating from the old framework structure to the new Arc Framework v2.0.

## What's New

### 🎯 Professional Package Structure
- Organized into logical modules: `core`, `agents`, `nodes`, `teams`, `config`, `utils`
- Proper `__init__.py` files with exports
- Clear separation of concerns

### 🏗️ Enhanced Core Classes

#### Base Classes
- **`BaseAgent`**: Abstract base for all agents with invoke/ainvoke methods
- **`BaseTeam`**: Abstract base for teams with build patterns
- **`BaseNode`**: Abstract base for workflow nodes

#### State Management
- **`State`**: Enhanced state with context and metadata
- **`StateManager`**: Utilities for state manipulation

#### Supervisor
- **`Supervisor`**: Professional supervisor with member management
- Dynamic routing based on LLM decisions
- Easy member addition/removal

#### Graph Orchestration
- **`GraphOrchestrator`**: High-level API for graph building
- Fluent interface for adding nodes and teams
- Built-in hierarchical graph construction

### 🤖 Agent Framework

#### TeamBuilder
- Fluent interface for building teams
- Method chaining: `.with_llm()`, `.with_tools()`, `.with_prompt()`
- Automatic sub-graph construction

#### AgentFactory
- Factory pattern for creating agents
- Support for custom agent types
- Default LLM and tools configuration

### 📦 Pre-Built Nodes
- **`CoordinatorNode`**: User interaction handling
- **`PlannerNode`**: Task decomposition
- **`ResponseGeneratorNode`**: Response synthesis

### ⚙️ Configuration Management
- **`Config`**: YAML and environment variable support
- Type-safe configuration
- Easy LLM and embeddings access

### 🛠️ Utilities
- **Logging**: Standardized logging setup
- **Prompts**: Prompt loading from files
- **Decorators**: Async/sync conversion, retry, caching
- **Helpers**: JSON cleaning, state validation, etc.

## Migration Steps

### Step 1: Update Imports

**Old:**
```python
from supervisor_class import Supervisor
from team_builder import TeamBuilder
from utils import State, llm
```

**New:**
```python
from arc import (
    Supervisor,
    TeamBuilder,
    Config,
    GraphOrchestrator,
)
from arc.core import State

# Load config
config = Config.from_yaml("config.yml")
llm = config.get_llm()
```

### Step 2: Update Team Creation

**Old:**
```python
class TeamBuilder:
    def _init_(self, name, description, llm, tools, prompt):
        self.name = name
        # ...
```

**New:**
```python
team = (TeamBuilder("team_name")
    .with_llm(llm)
    .with_tools([tool1, tool2])
    .with_prompt("System prompt...")
    .with_description("Team description")
    .build())
```

### Step 3: Update Supervisor Usage

**Old:**
```python
supervisor = Supervisor(llm)
supervisor.add_member("team1")
node = supervisor.node()
```

**New:**
```python
supervisor = Supervisor(llm, members=["team1", "team2"])
supervisor.add_member("team3")
supervisor_node = supervisor.create_node()
```

### Step 4: Use GraphOrchestrator

**Old:**
```python
from langgraph.graph import StateGraph, START

builder = StateGraph(State)
builder.add_node("coordinator", coordinator)
builder.add_node("team1", team1)
# ... manual edge management
graph = builder.compile()
```

**New:**
```python
from arc import GraphOrchestrator

orchestrator = GraphOrchestrator()
orchestrator.add_node("coordinator", coordinator)
orchestrator.add_team(team1_builder)
orchestrator.set_supervisor(supervisor)
orchestrator.set_entry_point("coordinator")
graph = orchestrator.compile()
```

### Step 5: Update Node Implementations

**Old:**
```python
def coordinator(state: State) -> Command:
    # Manual implementation
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    response = llm.invoke(messages)
    # ...
```

**New:**
```python
from arc.nodes import CoordinatorNode

coordinator = CoordinatorNode(
    llm=coordinator_llm,
    system_prompt="Custom prompt...",
    name="coordinator"
)
```

### Step 6: Use Configuration Management

**Old:**
```python
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

llm = ChatOpenAI(model=config['llm']['model'])
```

**New:**
```python
from arc import Config

config = Config.from_yaml("config.yml")
llm = config.get_llm()
fast_llm = config.get_llm("fast_llm")
embeddings = config.get_embeddings()
```

## Key Improvements

### 1. Type Safety
All classes have comprehensive type hints:
```python
def add_member(self, member_name: str) -> None:
    """Add a team member."""
    ...
```

### 2. Documentation
Every class and method has docstrings:
```python
class TeamBuilder(BaseTeam):
    """
    Builder for creating specialized agent teams.
    
    Example:
        >>> team = TeamBuilder("my_team").with_llm(llm).build()
    """
```

### 3. Error Handling
Proper validation and error messages:
```python
if not self._llm:
    raise ValueError("LLM not set. Use with_llm()")
```

### 4. Logging
Built-in logging throughout:
```python
self._logger.info(f"Built team '{self.name}'")
```

### 5. Async Support
Full async/sync support:
```python
async def ainvoke(self, state):
    """Async invocation."""
    ...
```

## Best Practices

### 1. Use the Orchestrator
Instead of manually building graphs, use `GraphOrchestrator`:
```python
orchestrator = GraphOrchestrator()
orchestrator.add_team(team1)
orchestrator.add_team(team2)
orchestrator.set_supervisor(supervisor)
graph = orchestrator.compile()
```

### 2. Use Pre-Built Nodes
Leverage the framework's nodes:
```python
from arc.nodes import (
    CoordinatorNode,
    PlannerNode,
    ResponseGeneratorNode
)
```

### 3. Follow the Builder Pattern
Use fluent interfaces for configuration:
```python
team = (TeamBuilder("name")
    .with_llm(llm)
    .with_tools(tools)
    .build())
```

### 4. Centralize Configuration
Use the Config class:
```python
config = Config.from_yaml("config.yml")
llm = config.get_llm()
```

### 5. Add Logging
Use the logging utilities:
```python
from arc.utils import setup_logging

setup_logging(level="INFO", log_file="app.log")
```

## Example: Complete Migration

**Before:**
```python
from supervisor_class import Supervisor
from team_builder import TeamBuilder
from utils import State, llm

# Manual setup
supervisor = Supervisor(llm)
team1 = TeamBuilder(name="team1", llm=llm, tools=tools, prompt=prompt)
# ... lots of manual wiring
```

**After:**
```python
from arc import (
    Config,
    GraphOrchestrator,
    Supervisor,
    TeamBuilder,
)

# Clean, organized setup
config = Config.from_yaml("config.yml")
llm = config.get_llm()

team1 = TeamBuilder("team1").with_llm(llm).with_tools(tools).build()
supervisor = Supervisor(llm)

orchestrator = GraphOrchestrator()
orchestrator.add_team(team1)
orchestrator.set_supervisor(supervisor)
graph = orchestrator.compile()
```

## Support

For questions or issues:
- Check the examples in `examples/`
- Review the README.md
- Read inline documentation
- Open an issue on GitHub

---

Welcome to Arc Framework v2.0! 🚀
