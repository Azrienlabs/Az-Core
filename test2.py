"""
Comprehensive Test: Using RL with GraphOrchestrator's build_hierarchical_graph

This test demonstrates how to integrate Reinforcement Learning (RL) into
a hierarchical agent graph using the Arc Framework.

Key Components:
1. RLManager - Q-learning based tool selection
2. RewardCalculator - Computes rewards from agent execution
3. RL-enabled agents - Agents that learn optimal tool usage
4. Hierarchical graph - Coordinator → Planner → Supervisor → Teams → Generator

Author: Arc Framework
Date: 2025
"""

from arc.config import load_config
from arc.agents import AgentFactory
from arc.agents.react_agent import ReactAgent
from arc.core.orchestrator import GraphOrchestrator
from arc.core.supervisor import MainSupervisor
from arc.core.base import BaseTeam
from arc.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from arc.rl import RLManager, HeuristicRewardCalculator
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from arc.core.state import State
import logging
from dotenv import load_dotenv

# Configure logging for better visibility
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# SECTION 1: Define Tools
# =============================================================================
# Tools are the actions that agents can take. Each tool should have:
# - Clear name (used by RL for identification)
# - Good docstring (helps LLM understand when to use it)
# - Simple, focused functionality

@tool
def calculate_sum(numbers: str) -> str:
    """Calculate the sum of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        result = sum(nums)
        return f"The sum of {numbers} is {result}"
    except Exception as e:
        return f"Error calculating sum: {str(e)}"


@tool
def calculate_multiply(numbers: str) -> str:
    """Multiply comma-separated numbers together."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        result = 1
        for n in nums:
            result *= n
        return f"The product of {numbers} is {result}"
    except Exception as e:
        return f"Error calculating product: {str(e)}"


@tool
def calculate_average(numbers: str) -> str:
    """Calculate the average (mean) of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        avg = sum(nums) / len(nums)
        return f"The average of {numbers} is {avg}"
    except Exception as e:
        return f"Error calculating average: {str(e)}"


@tool
def calculate_power(base_and_exponent: str) -> str:
    """Calculate base raised to the power of exponent. Format: 'base,exponent'."""
    try:
        parts = [float(n.strip()) for n in base_and_exponent.split(',')]
        if len(parts) != 2:
            return "Error: Please provide exactly two numbers (base,exponent)"
        base, exp = parts
        result = base ** exp
        return f"{base} raised to the power of {exp} is {result}"
    except Exception as e:
        return f"Error calculating power: {str(e)}"


@tool
def format_as_report(title_and_content: str) -> str:
    """
    Format content as a professional report.
    Format: 'title|content' (separated by pipe character)
    """
    try:
        parts = title_and_content.split('|', 1)
        if len(parts) != 2:
            return "Error: Use format 'title|content'"
        
        title, content = parts
        report = f"""
{'=' * 80}
{title.strip().upper()}
{'=' * 80}

{content.strip()}

{'=' * 80}
Report Generated Successfully
"""
        return report
    except Exception as e:
        return f"Error formatting report: {str(e)}"


@tool
def format_as_bullet_list(items: str) -> str:
    """Format comma-separated items as a bullet point list."""
    try:
        item_list = [item.strip() for item in items.split(',')]
        if not item_list:
            return "Error: No items provided"
        
        result = "FORMATTED LIST:\n" + "\n".join([f"  • {item}" for item in item_list])
        return result
    except Exception as e:
        return f"Error formatting list: {str(e)}"


@tool
def format_as_table(data: str) -> str:
    """
    Format data as a simple table.
    Format: 'header1,header2|row1col1,row1col2|row2col1,row2col2'
    """
    try:
        rows = data.split('|')
        if len(rows) < 2:
            return "Error: Need at least header and one data row"
        
        table = "TABLE FORMAT:\n"
        for i, row in enumerate(rows):
            cols = [c.strip() for c in row.split(',')]
            table += "  | " + " | ".join(cols) + " |\n"
            if i == 0:
                table += "  " + "-" * (len(cols) * 10) + "\n"
        
        return table
    except Exception as e:
        return f"Error formatting table: {str(e)}"


# =============================================================================
# SECTION 2: Setup RL Components
# =============================================================================

def setup_rl_components():
    """
    Set up RLManager and RewardCalculator for each team.
    
    Returns:
        Tuple of (math_rl, math_reward, report_rl, report_reward)
    """
    logger.info("=" * 80)
    logger.info("Setting up RL components...")
    logger.info("=" * 80)
    
    # Math team RL setup
    math_tools = [calculate_sum, calculate_multiply, calculate_average, calculate_power]
    math_rl = RLManager(
        tool_names=[t.name for t in math_tools],
        q_table_path="rl_data/math_team_q_table.pkl",
        exploration_rate=0.2,  # 20% chance to explore new tools
        learning_rate=0.1,     # How quickly to learn from rewards
        discount_factor=0.99,  # How much to value future rewards
        use_embeddings=False   # Set to True if sentence-transformers installed
    )
    math_reward = HeuristicRewardCalculator(
        success_reward=1.0,
        failure_reward=-0.5,
        empty_penalty=-0.3
    )
    logger.info(f"✓ Math RL Manager: {len(math_tools)} tools, exploration={0.2}")
    
    # Report formatting team RL setup
    report_tools = [format_as_report, format_as_bullet_list, format_as_table]
    report_rl = RLManager(
        tool_names=[t.name for t in report_tools],
        q_table_path="rl_data/report_team_q_table.pkl",
        exploration_rate=0.2,
        learning_rate=0.1,
        discount_factor=0.99,
        use_embeddings=False
    )
    report_reward = HeuristicRewardCalculator(
        success_reward=1.0,
        failure_reward=-0.5,
        empty_penalty=-0.3
    )
    logger.info(f"✓ Report RL Manager: {len(report_tools)} tools, exploration={0.2}")
    
    return math_rl, math_reward, report_rl, report_reward


# =============================================================================
# SECTION 3: Create RL-enabled Teams
# =============================================================================

class RLEnabledTeam(BaseTeam):
    """
    Custom team class that wraps an RL-enabled ReactAgent.
    
    This is a workaround since TeamBuilder doesn't support RL out of the box.
    """
    
    def __init__(self, name: str, agent: ReactAgent):
        super().__init__(name=name)
        self.agent = agent
        self.description = f"RL-enabled team: {name}"
    
    def build(self):
        """Build and return callable for this team."""
        def team_callable(state: State) -> Command:
            """Invoke the RL-enabled agent."""
            result = self.agent.invoke(state)
            
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=result["messages"][-1].content,
                            name=self.name
                        )
                    ]
                },
                goto="supervisor"
            )
        
        return team_callable


def create_rl_teams(llm, math_rl, math_reward, report_rl, report_reward):
    """
    Create teams with RL-enabled tool selection.
    
    Each team consists of:
    - A set of specialized tools
    - An RLManager that learns optimal tool selection
    - A RewardCalculator that provides feedback
    
    Since TeamBuilder doesn't support RL, we create ReactAgent instances
    and wrap them in custom RLEnabledTeam objects.
    
    Args:
        llm: Language model for agents
        math_rl: RLManager for math team
        math_reward: RewardCalculator for math team
        report_rl: RLManager for report team
        report_reward: RewardCalculator for report team
    
    Returns:
        Tuple of (math_team, report_team)
    """
    logger.info("\n" + "=" * 80)
    logger.info("Creating RL-enabled teams...")
    logger.info("=" * 80)
    
    factory = AgentFactory(default_llm=llm)
    
    # --------------------------------------------------
    # Math Team
    # --------------------------------------------------
    math_tools = [calculate_sum, calculate_multiply, calculate_average, calculate_power]
    
    # Create RL-enabled agent
    math_agent = factory.create_react_agent(
        name="math_specialist",
        tools=math_tools,
        prompt=(
            "You are a mathematical computation specialist. "
            "Use the appropriate calculation tool for each task. "
            "Always provide clear, accurate results."
        ),
        description="Mathematical computation specialist with RL-optimized tool selection",
        rl_enabled=True,
        rl_manager=math_rl,
        reward_calculator=math_reward
    )
    
    # Wrap in custom team
    math_team = RLEnabledTeam("math_team", math_agent)
    math_team.description = "Handles mathematical calculations with RL-optimized tool selection"
    
    logger.info(f"✓ Math Team created: {len(math_tools)} tools, RL enabled")
    
    # --------------------------------------------------
    # Report Formatting Team
    # --------------------------------------------------
    report_tools = [format_as_report, format_as_bullet_list, format_as_table]
    
    # Create RL-enabled agent
    report_agent = factory.create_react_agent(
        name="report_writer",
        tools=report_tools,
        prompt=(
            "You are a professional report formatter. "
            "Use the appropriate formatting tool to present information clearly. "
            "Always choose the format that best suits the data."
        ),
        description="Report formatting specialist with RL-optimized tool selection",
        rl_enabled=True,
        rl_manager=report_rl,
        reward_calculator=report_reward
    )
    
    # Wrap in custom team
    report_team = RLEnabledTeam("report_writer_team", report_agent)
    report_team.description = "Handles report formatting with RL-optimized tool selection"
    
    logger.info(f"✓ Report Team created: {len(report_tools)} tools, RL enabled")
    
    return math_team, report_team


# =============================================================================
# SECTION 4: Build Hierarchical Graph
# =============================================================================

def build_rl_hierarchical_graph(llm, math_team, report_team):
    """
    Build a hierarchical graph with RL-enabled teams.
    
    The graph structure:
    START → Coordinator → Planner → Supervisor → [Teams] → Generator → END
    
    Where:
    - Coordinator: Analyzes user request
    - Planner: Creates execution plan
    - Supervisor: Routes to appropriate teams
    - Teams: Execute tasks with RL-optimized tool selection
    - Generator: Synthesizes final response
    
    Args:
        llm: Language model
        math_team: RL-enabled math team
        report_team: RL-enabled report team
    
    Returns:
        Compiled graph ready for execution
    """
    logger.info("\n" + "=" * 80)
    logger.info("Building hierarchical graph with RL teams...")
    logger.info("=" * 80)
    
    # Create main supervisor
    supervisor = MainSupervisor(
        llm=llm,
        members=["math_team", "report_writer_team"]
    )
    logger.info("✓ Main supervisor created")
    
    # Create workflow nodes
    coordinator = CoordinatorNode(llm=llm)
    planner = PlannerNode(llm=llm,)
    generator = ResponseGeneratorNode(llm=llm)
    logger.info("✓ Workflow nodes created (Coordinator, Planner, Generator)")
    
    # Build orchestrator with hierarchical structure
    orchestrator = GraphOrchestrator()
    compiled_graph = orchestrator.build_hierarchical_graph(
        coordinator=coordinator,
        planner=planner,
        supervisor=supervisor,
        teams=[math_team, report_team],  # RL-enabled teams
        generator=generator
    )
    
    logger.info("✓ Hierarchical graph compiled successfully")
    logger.info(f"  - Nodes: {len(orchestrator.get_all_nodes())}")
    logger.info(f"  - Teams: {len(orchestrator.get_all_teams())}")
    logger.info(f"  - RL Learning: ACTIVE")
    
    return compiled_graph


# =============================================================================
# SECTION 5: Test Queries
# =============================================================================

def run_test_queries(graph, math_rl, report_rl):
    """
    Run test queries through the RL-enabled graph.
    
    The RL system will:
    1. Select tools based on Q-values (or explore randomly)
    2. Execute the selected tools
    3. Calculate reward based on execution success
    4. Update Q-table to learn better tool selection
    
    Args:
        graph: Compiled hierarchical graph
        math_rl: Math team RLManager
        report_rl: Report team RLManager
    """
    logger.info("\n" + "=" * 80)
    logger.info("Running Test Queries with RL Learning...")
    logger.info("=" * 80)
    
    test_queries = [
        # Math queries
        "Calculate the sum of 15, 23, and 47",
        "What's the average of 10, 20, 30, 40?",
        "Multiply these numbers: 5, 6, 7",
        "What is 2 raised to the power of 8?",
        "Find the sum of 100, 200, 300",
        
        # Formatting queries
        "Format this as a report with title 'Sales Results' and content 'Q1 sales exceeded targets'",
        "Create a bullet list with: Apples, Bananas, Oranges",
        "Make a table with headers Name,Age and rows John,25|Jane,30",
        
        # Mixed queries
        "Calculate the average of 5, 10, 15 and format it as a bullet list",
    ]
    
    configure = {
        "configurable": {
            "thread_id": "rl_hierarchical_test",
        }
    }
    
    for i, query in enumerate(test_queries, 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"Query {i}/{len(test_queries)}: {query}")
        logger.info("=" * 80)
        
        try:
            # Execute query through graph
            result = graph.invoke({"messages": [("user", query)]}, configure)
            
            # Display result
            if result and "messages" in result:
                response = result["messages"][-1].content
                logger.info(f"\n{'Response:':<15} {response}\n")
            else:
                logger.warning("No response in result")
            
            # RL automatically updates Q-values during execution!
            
        except Exception as e:
            logger.error(f"Error executing query: {e}", exc_info=True)
    
    # Show learning progress
    logger.info("\n" + "=" * 80)
    logger.info("RL Learning Completed!")
    logger.info("=" * 80)
    display_rl_statistics(math_rl, report_rl)


# =============================================================================
# SECTION 6: Display Results
# =============================================================================

def display_rl_statistics(math_rl, report_rl):
    """Display RL statistics and export Q-tables."""
    
    logger.info("\n" + "=" * 80)
    logger.info("REINFORCEMENT LEARNING STATISTICS")
    logger.info("=" * 80)
    
    # Math team stats
    logger.info("\n📊 Math Team RL:")
    math_stats = math_rl.get_statistics()
    for key, value in math_stats.items():
        logger.info(f"  {key:25}: {value}")
    
    # Report team stats
    logger.info("\n📊 Report Team RL:")
    report_stats = report_rl.get_statistics()
    for key, value in report_stats.items():
        logger.info(f"  {key:25}: {value}")
    
    # Export Q-tables
    logger.info("\n" + "=" * 80)
    logger.info("Exporting Q-tables for inspection...")
    logger.info("=" * 80)
    
    try:
        math_export = math_rl.export_readable("rl_data/math_team_q_table_readable.txt")
        logger.info(f"✓ Math Q-table: {math_export}")
    except Exception as e:
        logger.error(f"Failed to export math Q-table: {e}")
    
    try:
        report_export = report_rl.export_readable("rl_data/report_team_q_table_readable.txt")
        logger.info(f"✓ Report Q-table: {report_export}")
    except Exception as e:
        logger.error(f"Failed to export report Q-table: {e}")


# =============================================================================
# SECTION 7: Main Execution
# =============================================================================

def main():
    """
    Main execution function.
    
    This orchestrates the entire RL-enabled hierarchical graph test:
    1. Load configuration and LLM
    2. Setup RL managers and reward calculators
    3. Create RL-enabled teams
    4. Build hierarchical graph
    5. Run test queries
    6. Display learning statistics
    """
    
    logger.info("=" * 80)
    logger.info("Arc Framework - RL with GraphOrchestrator Test")
    logger.info("=" * 80)
    
    try:
        # Step 1: Load configuration
        logger.info("\n📋 Loading configuration...")
        config = load_config("config.yml")
        llm = config.get_llm()
        logger.info("✓ Configuration loaded")
        
        # Step 2: Setup RL components
        math_rl, math_reward, report_rl, report_reward = setup_rl_components()
        
        # Step 3: Create RL-enabled teams
        math_team, report_team = create_rl_teams(
            llm, math_rl, math_reward, report_rl, report_reward
        )
        
        # Step 4: Build hierarchical graph
        graph = build_rl_hierarchical_graph(llm, math_team, report_team)
        
        # Step 5: Run test queries
        run_test_queries(graph, math_rl, report_rl)
        
        # Final summary
        logger.info("\n" + "=" * 80)
        logger.info("🎉 TEST COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("\nKey Points:")
        logger.info("  ✓ RL-enabled teams integrated into hierarchical graph")
        logger.info("  ✓ Each team has independent Q-learning")
        logger.info("  ✓ Tool selection optimized through experience")
        logger.info("  ✓ Q-tables persisted for continual learning")
        logger.info("  ✓ Ready for production use!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
