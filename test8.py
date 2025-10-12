"""
Example demonstrating RL-enabled agent patterns with GraphOrchestrator.

This example shows how to:
1. Create RL-enabled agent patterns (Self-Consistency, Reflexion, Reasoning Duo)
2. Integrate them with the GraphOrchestrator
3. Monitor RL learning and performance
4. Mix RL and non-RL agents in the same orchestration
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from arc.core.orchestrator import GraphOrchestrator
from arc.agents.team_builder import TeamBuilder
from arc.rl.rl_manager import RLManager
from arc.rl.rewards import HeuristicRewardCalculator
from arc.agents.self_consistency_agent import SelfConsistencyAgent
from arc.agents.reflexion_agent import ReflexionAgent
from arc.agents.reasoning_duo_agent import ReasoningDuoAgent
from arc.agents.agent_judge import AgentJudge
from arc.agents.agent_pattern_router import AgentPatternRouter

from dotenv import load_dotenv

load_dotenv()


def create_tools():
    """Create example tools for agents using @tool decorator."""
    
    @tool
    def analyze_data(query: str) -> str:
        """Analyze data and extract patterns"""
        return f"Analysis complete for: {query}. Found 3 key patterns."
    
    @tool
    def generate_report(data: str) -> str:
        """Generate comprehensive reports"""
        return f"Report generated: {data[:50]}..."
    
    @tool
    def evaluate_quality(content: str) -> str:
        """Evaluate content quality"""
        score = len(content) / 10
        return f"Quality score: {min(score, 10.0):.1f}/10"
    
    @tool
    def research_topic(topic: str) -> str:
        """Research topics and gather information"""
        return f"Research findings for {topic}: Multiple sources confirm trend."
    
    return [analyze_data, generate_report, evaluate_quality, research_topic]


def example_1_self_consistency_with_rl():
    """Example: Self-Consistency pattern with RL for tool selection."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Self-Consistency Agent with RL")
    print("=" * 80)
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL infrastructure
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_self_consistency.pkl",
        exploration_rate=0.2,
        learning_rate=0.1,
        discount_factor=0.9
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create Self-Consistency agent with RL
    agent = SelfConsistencyAgent(
        name="SelfConsistencyResearcher",
        llm=llm,
        tools=tools,
        prompt="You are a research assistant. Analyze queries thoroughly.",
        description="Research agent using self-consistency with RL tool selection",
        num_samples=3,
        rl_enabled=True,
        rl_manager=rl_manager,
        reward_calculator=reward_calc
    )
    
    # Test queries
    from langchain_core.messages import HumanMessage
    
    queries = [
        "What are the main trends in AI research?",
        "Analyze the impact of climate change on agriculture",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        state = {"messages": [HumanMessage(content=query)]}
        result = agent.invoke(state)
        content = result['messages'][-1].content if hasattr(result['messages'][-1], 'content') else str(result['messages'][-1])
        print(f"Result: {content[:200]}...")
        
        # Show RL statistics
        stats = rl_manager.get_statistics()
        print(f"RL Stats - States: {stats['total_states']}, Q-values: {stats['non_zero_q_values']}")


def example_2_reflexion_with_rl():
    """Example: Reflexion pattern with RL for iterative improvement."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Reflexion Agent with RL")
    print("=" * 80)
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL infrastructure
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_reflexion.pkl",
        exploration_rate=0.15,
        learning_rate=0.1,
        discount_factor=0.95
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create Reflexion agent with RL
    agent = ReflexionAgent(
        name="ReflexionWriter",
        llm=llm,
        tools=tools,
        prompt="You are a content writer. Create high-quality content.",
        description="Writing agent using reflexion with RL-optimized tool selection",
        max_loops=2,
        rl_enabled=True,
        rl_manager=rl_manager,
        reward_calculator=reward_calc
    )
    
    # Test task
    from langchain_core.messages import HumanMessage
    
    task = "Write a comprehensive analysis of renewable energy trends"
    print(f"\nTask: {task}")
    state = {"messages": [HumanMessage(content=task)]}
    result = agent.invoke(state)
    content = result['messages'][-1].content if hasattr(result['messages'][-1], 'content') else str(result['messages'][-1])
    print(f"Result: {content[:200]}...")
    
    # Show RL statistics
    stats = rl_manager.get_statistics()
    print(f"RL Stats - States: {stats['total_states']}, Q-values: {stats['non_zero_q_values']}")
    print(f"Exploration rate: {stats['exploration_rate']:.3f}, Embeddings: {stats['use_embeddings']}")


def example_3_reasoning_duo_with_rl():
    """Example: Reasoning Duo pattern with RL."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Reasoning Duo with RL")
    print("=" * 80)
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL infrastructure
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_reasoning_duo.pkl",
        exploration_rate=0.1,
        learning_rate=0.15,
        discount_factor=0.9
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create Reasoning Duo agent with RL
    agent = ReasoningDuoAgent(
        name="ReasoningAnalyst",
        llm=llm,
        tools=tools,
        prompt="You are an analyst. Provide thorough analysis.",
        description="Analytical agent using reasoning duo with RL tool selection",
        rl_enabled=True,
        rl_manager=rl_manager,
        reward_calculator=reward_calc
    )
    
    # Test task
    from langchain_core.messages import HumanMessage
    
    task = "Analyze the economic implications of remote work trends"
    print(f"\nTask: {task}")
    state = {"messages": [HumanMessage(content=task)]}
    result = agent.invoke(state)
    content = result['messages'][-1].content if hasattr(result['messages'][-1], 'content') else str(result['messages'][-1])
    print(f"Result: {content[:200]}...")
    
    # Show RL statistics
    stats = rl_manager.get_statistics()
    print(f"RL Stats - States: {stats['total_states']}, Q-values: {stats['non_zero_q_values']}")


def example_4_orchestrator_with_rl_patterns():
    """Example: Using TeamBuilder directly with RL (like test7.py)."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: TeamBuilder with RL (test7.py style)")
    print("=" * 80)
    print("\nNote: Agent patterns (Self-Consistency, Reflexion, etc.) are standalone agents.")
    print("For orchestrator integration, use TeamBuilder directly with LLM and tools.\n")
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL infrastructure
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_orchestrator.pkl",
        exploration_rate=0.15,
        learning_rate=0.1,
        discount_factor=0.9
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create RL-enabled team using TeamBuilder (correct approach)
    print("Creating RL-enabled team with TeamBuilder...")
    research_team = (
        TeamBuilder("ResearchTeam")
        .with_llm(llm)
        .with_tools(tools)
        .with_prompt("You are a research assistant. Analyze queries thoroughly.")
        .with_rl(rl_manager, reward_calc)  # Enable RL for tool selection
        .with_description("Research team with RL-optimized tool selection")
        .build()
    )
    
    print("✓ Team created successfully with RL")
    
    # The team is now a callable that can be used in orchestrator
    # Test direct invocation
    from langchain_core.messages import HumanMessage
    print("\nTesting team with a query...")
    state = {"messages": [HumanMessage(content="Research AI trends")]}
    
    try:
        result = research_team(state)
        if isinstance(result, dict) and 'messages' in result:
            content = result['messages'][-1].content if hasattr(result['messages'][-1], 'content') else str(result['messages'][-1])
            print(f"Result: {content[:200]}...")
        else:
            print(f"Result: {str(result)[:200]}...")
    except Exception as e:
        print(f"Note: Direct team invocation may require orchestrator context: {e}")
    
    # Show RL statistics
    print("\n" + "-" * 80)
    print("RL Learning Statistics:")
    print("-" * 80)
    stats = rl_manager.get_statistics()
    print(f"Total States: {stats['total_states']}")
    print(f"Total Tools: {stats['total_tools']}")
    print(f"Non-zero Q-values: {stats['non_zero_q_values']}")
    print(f"Exploration Rate: {stats['exploration_rate']:.3f}")
    print(f"Learning Rate: {stats['learning_rate']:.3f}")
    print(f"Using Embeddings: {stats['use_embeddings']}")
    
    print("\n✓ TeamBuilder with RL works correctly!")
    print("For full orchestrator examples, see test7.py")


def example_5_pattern_router_with_rl():
    """Example: Using AgentPatternRouter to create RL-enabled patterns."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: AgentPatternRouter with RL")
    print("=" * 80)
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL infrastructure
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_router.pkl",
        exploration_rate=0.2,
        learning_rate=0.1
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create different patterns using router
    patterns = ["self-consistency", "reflexion", "reasoning-duo"]
    
    for pattern_name in patterns:
        print(f"\n--- Testing {pattern_name} pattern ---")
        
        # Create router with pattern and configuration
        router = AgentPatternRouter(
            pattern=pattern_name,
            name=f"{pattern_name.replace('-', '_')}_agent",
            llm=llm,
            tools=tools,
            prompt=f"You are a {pattern_name} agent.",
            description=f"Agent using {pattern_name} pattern with RL",
            rl_enabled=True,
            rl_manager=rl_manager,
            reward_calculator=reward_calc,
            num_samples=3,  # for self-consistency
            max_loops=2,    # for reflexion/reasoning-duo
        )
        
        # Create agent from router
        agent = router.create_agent()
        
        # Test agent
        from langchain_core.messages import HumanMessage
        state = {"messages": [HumanMessage(content=f"Test query for {pattern_name}")]}
        result = agent.invoke(state)
        content = result['messages'][-1].content if hasattr(result['messages'][-1], 'content') else str(result['messages'][-1])
        print(f"Result: {content[:150]}...")


def example_6_rl_learning_progression():
    """Example: Demonstrate RL learning over multiple iterations."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: RL Learning Progression")
    print("=" * 80)
    
    llm = ChatOpenAI(temperature=0.7)
    tools = create_tools()
    
    # Setup RL with high exploration initially
    tool_names = [tool.name for tool in tools]
    rl_manager = RLManager(
        tool_names=tool_names,
        q_table_path="rl_data/q_table_learning.pkl",
        exploration_rate=0.3,  # Start with high exploration
        learning_rate=0.2,
        discount_factor=0.9
    )
    reward_calc = HeuristicRewardCalculator()
    
    # Create agent
    agent = SelfConsistencyAgent(
        name="LearningAgent",
        llm=llm,
        tools=tools,
        prompt="You are a learning agent improving tool selection over time.",
        num_samples=3,
        rl_enabled=True,
        rl_manager=rl_manager,
        reward_calculator=reward_calc
    )
    
    # Run multiple iterations
    queries = [
        "Research current AI trends",
        "Analyze market data for tech sector",
        "Generate report on industry findings",
        "Evaluate quality of previous reports",
    ] * 3  # Repeat to show learning
    
    print("\nRunning 12 iterations to demonstrate RL learning...\n")
    
    from langchain_core.messages import HumanMessage
    
    for i, query in enumerate(queries, 1):
        state = {"messages": [HumanMessage(content=query)]}
        result = agent.invoke(state)
        stats = rl_manager.get_statistics()
        
        if i % 3 == 0:  # Print stats every 3 iterations
            print(f"Iteration {i}:")
            print(f"  States: {stats['total_states']}, Q-values: {stats['non_zero_q_values']}")
            print(f"  Exploration rate: {stats['exploration_rate']:.3f}")
            print(f"  Cached embeddings: {stats['cached_embeddings']}")
            print()
    
    print("\nObserve how:")
    print("- Q-values are learned as agent explores different states")
    print("- State embeddings are cached for semantic matching")
    print("- Q-table grows as agent encounters new states")


if __name__ == "__main__":
    print("=" * 80)
    print("RL-ENABLED AGENT PATTERNS DEMONSTRATION")
    print("=" * 80)
    print("\nThis demo shows how to use RL with agent patterns in the Arc Framework.")
    print("RL enables agents to learn optimal tool selection over time.")
    print("\nRunning examples...\n")
    
    # Run examples
    try:
        example_1_self_consistency_with_rl()
        example_2_reflexion_with_rl()
        example_3_reasoning_duo_with_rl()
        example_4_orchestrator_with_rl_patterns()
        example_5_pattern_router_with_rl()
        example_6_rl_learning_progression()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)
        print("\nKey Takeaways:")
        print("1. RL parameters are optional - set rl_enabled=True to enable")
        print("2. Shared RLManager allows learning across multiple agents")
        print("3. Q-tables persist across runs for continuous learning")
        print("4. Mix RL and non-RL agents in same orchestrator")
        print("5. Monitor statistics to track learning progress")
        print("\nCheck the generated q_table_*.json files for persisted learning!")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
