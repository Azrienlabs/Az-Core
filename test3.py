"""
RL Test: Using TeamBuilder with built-in RL support

This demonstrates the NEW simplified API where TeamBuilder directly
supports RL without needing custom wrapper classes.

Author: Arc Framework
Date: 2025
"""

from arc.config import load_config
from arc.agents.team_builder import TeamBuilder
from arc.core.orchestrator import GraphOrchestrator
from arc.core.supervisor import MainSupervisor
from arc.nodes import ResponseGeneratorNode, PlannerNode, CoordinatorNode
from arc.rl import RLManager, HeuristicRewardCalculator
from langchain_core.tools import tool
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



@tool
def calculate_sum(numbers: str) -> str:
    """Calculate the sum of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        return f"The sum is {sum(nums)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def calculate_multiply(numbers: str) -> str:
    """Multiply comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        result = 1
        for n in nums:
            result *= n
        return f"The product is {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def calculate_average(numbers: str) -> str:
    """Calculate the average of comma-separated numbers."""
    try:
        nums = [float(n.strip()) for n in numbers.split(',')]
        return f"The average is {sum(nums) / len(nums)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def format_as_report(title_and_content: str) -> str:
    """Format content as a report. Format: 'title|content'."""
    try:
        parts = title_and_content.split('|', 1)
        if len(parts) != 2:
            return "Error: Use format 'title|content'"
        title, content = parts
        return f"\n=== {title.upper()} ===\n\n{content}\n\n" + "="*50
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def format_as_bullet_list(items: str) -> str:
    """Format comma-separated items as a bullet list."""
    try:
        item_list = [item.strip() for item in items.split(',')]
        result = "\n".join([f"• {item}" for item in item_list])
        return f"Formatted list:\n{result}"
    except Exception as e:
        return f"Error: {str(e)}"



def main():
    """Run RL-enabled hierarchical graph with simplified API.
    """
    # Load configuration
    logger.info("\nLoading configuration...")
    config = load_config("config.yml")
    llm = config.get_llm()
    

    logger.info("\nSetting up RL managers...")
    
    math_tools = [calculate_sum, calculate_multiply, calculate_average]
    math_rl = RLManager(
        tool_names=[t.name for t in math_tools],
        q_table_path="rl_data/math_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    math_reward = HeuristicRewardCalculator()
    
    report_tools = [format_as_report, format_as_bullet_list]
    report_rl = RLManager(
        tool_names=[t.name for t in report_tools],
        q_table_path="rl_data/report_q_table.pkl",
        exploration_rate=0.2,
        use_embeddings=False
    )
    report_reward = HeuristicRewardCalculator()
    
    logger.info("✓ RL managers created")
    

    logger.info("\nCreating RL-enabled teams with TeamBuilder...")
    
    math_team = (TeamBuilder("math_team")
        .with_llm(llm)
        .with_tools(math_tools)
        .with_prompt("You are a math specialist. Use the appropriate calculation tool.")
        .with_rl(math_rl, math_reward)  
        .with_description("Math calculations with RL-optimized tool selection")
    )
    
    logger.info("✓ Math team created with RL")
    
    report_team = (TeamBuilder("report_writer_team")
        .with_llm(llm)
        .with_tools(report_tools)
        .with_prompt("You are a report writer. Use the appropriate formatting tool.")
        .with_rl(report_rl, report_reward)  
        .with_description("Report formatting with RL-optimized tool selection")
    )
    
    logger.info("✓ Report team created with RL")
    

    logger.info("\nBuilding hierarchical graph...")
    
    supervisor = MainSupervisor(
        llm=llm,
        members=["math_team", "report_writer_team"]
    )
    
    orchestrator = GraphOrchestrator()
    graph = orchestrator.build_hierarchical_graph(
        coordinator=CoordinatorNode(llm=llm),
        planner=PlannerNode(llm=llm),
        supervisor=supervisor,
        teams=[math_team, report_team],  # RL-enabled teams work seamlessly!
        generator=ResponseGeneratorNode(llm=llm)
    )
    
    logger.info("✓ Graph built successfully with RL-enabled teams")
    

    logger.info("\nRunning test queries...")
    logger.info("=" * 80)
    
    test_queries = [
        "Calculate the sum of 10, 20, 30",
        "What's the average of 5, 10, 15?",
        "Format this as a report: Results|All tests passed successfully"
    ]
    
    configure = {"configurable": {"thread_id": "rl_simple_test"}}
    
    for i, query in enumerate(test_queries, 1):
        logger.info(f"\nQuery {i}: {query}")
        logger.info("-" * 80)
        
        try:
            result = graph.invoke({"messages": [("user", query)]}, configure)
            
            if result and "messages" in result:
                response = result["messages"][-1].content
                logger.info(f"Response: {response}")
            
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        
        logger.info("")
    

    logger.info("\n" + "=" * 80)
    logger.info("RL Statistics:")
    logger.info("=" * 80)
    
    logger.info("\nMath Team RL:")
    for key, value in math_rl.get_statistics().items():
        logger.info(f"  {key}: {value}")
    
    logger.info("\nReport Team RL:")
    for key, value in report_rl.get_statistics().items():
        logger.info(f"  {key}: {value}")
    
    # Export Q-tables
    logger.info("\nExporting Q-tables...")
    try:
        math_rl.export_readable("rl_data/math_q_table_readable.txt")
        report_rl.export_readable("rl_data/report_q_table_readable.txt")
        logger.info("✓ Q-tables exported")
    except Exception as e:
        logger.error(f"Export failed: {e}")
    



if __name__ == "__main__":
    main()
